"""When to use RAG, as code. An ordered decision tree, a RAG signal score, and a cost sketch.

The six requests are invented. The $3 price is an assumption for the arithmetic, not a quote.
Cache reads are billed at a fraction of the base input price. Anthropic's docs (2026-10) give
0.1x on most models and 0.05x on Claude Opus 5.5 and Sonnet 5.5, so the sketch shows both.
Run: python3 decide.py
"""

# Signals that push toward retrieval. Each one is a reason a plain prompt is not enough.
RAG_SIGNALS = ("private", "changes_often", "too_big_for_prompt", "needs_citations", "per_user_access")


def too_big(req, limit=200_000):
    """Anthropic's contextual-retrieval post (2024) suggests that a knowledge base under about
    200,000 tokens can go in the prompt whole. Above that, retrieve."""
    return req["corpus_tokens"] > limit


def signals(req):
    found = {s for s in RAG_SIGNALS if s != "too_big_for_prompt" and req.get(s)}
    if too_big(req):
        found.add("too_big_for_prompt")
    return found


def decide(req):
    """Return (verdict, reason). The order matters: the first rule that fits wins."""
    need = req["need"]
    if need == "behaviour":
        return "prompt or fine-tune", "it changes how the model writes, not what it knows"
    if need in ("count", "aggregate") or req.get("data") == "table":
        return "query the system of record", "the answer is computed from rows, so SQL or a tool call gives the exact number"
    if need == "exact_key":
        return "look it up directly", "a key such as an order number needs an exact match, not a similar one"
    if need == "whole_document":
        return "long context", "the task needs the whole document, and retrieval would hand over pieces"
    s = signals(req)
    if not s & {"too_big_for_prompt", "changes_often", "per_user_access"}:
        return "put it in the prompt, with prompt caching", "small and stable knowledge is cheaper to send than to retrieve"
    if need == "connections":
        return "RAG plus structure", "the answer joins facts across documents, so add a graph or SQL to retrieval"
    return "RAG", "signals: " + ", ".join(sorted(s))


REQUESTS = [
    dict(name="Support assistant over the help centre and past tickets", need="passage",
         corpus_tokens=6_000_000, private=True, changes_often=True, needs_citations=True, per_user_access=True),
    dict(name="'How many invoices are overdue this month?' in the app", need="count",
         corpus_tokens=0, private=True, changes_often=True, data="table"),
    dict(name="Summarize the contract the user just uploaded", need="whole_document",
         corpus_tokens=30_000, private=True),
    dict(name="Write marketing emails in our brand voice", need="behaviour", corpus_tokens=8_000),
    dict(name="HR policy helper over a 60-page handbook", need="passage",
         corpus_tokens=35_000, private=True, needs_citations=True),
    dict(name="Security questionnaire answers from past responses and product docs", need="passage",
         corpus_tokens=2_500_000, private=True, changes_often=True, needs_citations=True),
]


def cost_per_query(input_tokens, price_per_mtok, cached_tokens=0, cache_read_multiplier=0.1):
    """Input cost only. Cached tokens are billed at a fraction of the base input price."""
    fresh = input_tokens - cached_tokens
    return (fresh + cached_tokens * cache_read_multiplier) * price_per_mtok / 1_000_000


def scale_costs(corpus_tokens, questions=10_000, price=3.0, window=1_000_000, question=50, retrieved=2_000):
    """Input cost of answering `questions` questions, by approach, for one corpus size.
    None means the corpus does not fit in the context window at all."""
    fits = corpus_tokens + question <= window
    return dict(
        stuff=round(questions * cost_per_query(corpus_tokens + question, price), 2) if fits else None,
        stuff_cached=round(questions * cost_per_query(corpus_tokens + question, price, corpus_tokens), 2) if fits else None,
        stuff_cached_05=round(questions * cost_per_query(corpus_tokens + question, price, corpus_tokens, 0.05), 2) if fits else None,
        rag=round(questions * cost_per_query(retrieved + question, price), 2),
    )


def main(price=3.0):
    verdicts = [(r["name"], *decide(r), len(signals(r))) for r in REQUESTS]
    handbook, question = 35_000, 50
    retrieved = 5 * 400                     # five chunks of about 400 tokens
    costs = dict(
        stuff=cost_per_query(handbook + question, price),
        stuff_cached=cost_per_query(handbook + question, price, cached_tokens=handbook),
        stuff_cached_05=cost_per_query(handbook + question, price, handbook, cache_read_multiplier=0.05),
        rag=cost_per_query(retrieved + question, price),
    )
    scales = {n: scale_costs(n) for n in (35_000, 400_000, 2_500_000)}
    return verdicts, costs, scales


if __name__ == "__main__":
    verdicts, costs, scales = main()
    for name, verdict, reason, n in verdicts:
        print(f"- {name}\n    -> {verdict} ({n} RAG signals): {reason}")
    per_10k = {k: round(v * 10_000, 2) for k, v in costs.items()}
    print(f"\ninput cost per 10,000 questions at an assumed $3 per million input tokens: {per_10k}")
    v = {name: verdict for name, verdict, _, _ in verdicts}
    assert list(v.values()) == ["RAG", "query the system of record", "long context", "prompt or fine-tune",
                                "put it in the prompt, with prompt caching", "RAG"]
    assert sum(1 for x in v.values() if x == "RAG") == 2
    assert costs["rag"] < costs["stuff_cached"] < costs["stuff"]
    assert costs["stuff_cached_05"] < costs["rag"]                # at 0.05x the cached handbook beats RAG
    assert per_10k["stuff_cached_05"] == 54.0
    assert round(costs["stuff"] / costs["stuff_cached"], 1) == 9.9      # caching cuts the stuffed prompt about 10x
    assert round(per_10k["stuff"]) == 1052 and per_10k["rag"] == 61.5
    for n, c in scales.items():
        print(f"corpus of {n:>9,} tokens, 10,000 questions: {c}")
    assert scales[400_000] == dict(stuff=12001.5, stuff_cached=1201.5, stuff_cached_05=601.5, rag=61.5)
    assert scales[2_500_000]["stuff"] is None                   # bigger than a 1M-token window
    print("decide ok")
