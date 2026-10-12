"""What an embedding does well and badly, measured on the Fernpay corpus.

1. Paraphrase: a question that shares no keyword with its answer still lands near it.
2. Similar is not correct: the retracted policy sits almost on top of the current one.
3. Model mismatch: query vectors from a different model make the index useless.
Run: python3 embeddings_demo.py
"""
import random

from corpus import EVAL
from mini_rag import CUSTOMER, DIM, Index, build_chunks, cosine, embed, tokens


def other_model(text, seed=7):
    """A stand-in for a different embedding model: same text, different coordinates."""
    order = list(range(DIM))
    random.Random(seed).shuffle(order)
    v = embed(text)
    return [v[i] for i in order]


def recall_with(index, query_embed, k=3):
    hits = 0
    for e in EVAL:
        q = query_embed(e["q"])
        scored = sorted(((cosine(q, v), i) for i, v in enumerate(index.vectors)
                         if index.allowed(i, CUSTOMER)), reverse=True)[:k]
        hits += e["gold"] in [index.chunks[i]["id"] for _, i in scored]
    return round(hits / len(EVAL), 3)


def main():
    index = Index(build_chunks())
    q = "how do I stop paying for fernpay"
    cancel = index.get("cancel#0")["text"]
    shared = set(tokens(q)) & set(tokens(cancel))
    v2, v1 = index.get("refunds-v2#0")["text"], index.get("refunds-v1#0")["text"]
    refund_q = embed("can I get my money back on a yearly plan")
    return dict(
        shared_words=shared, paraphrase_sim=round(cosine(embed(q), embed(cancel)), 3),
        v2_sim=round(cosine(refund_q, embed(v2)), 3), v1_sim=round(cosine(refund_q, embed(v1)), 3),
        v1_v2_sim=round(cosine(embed(v1), embed(v2)), 3),
        same_model=recall_with(index, embed), mixed_models=recall_with(index, other_model),
    )


if __name__ == "__main__":
    r = main()
    print(f"paraphrase: shared words {r['shared_words'] or 'none'}, cosine {r['paraphrase_sim']}")
    print(f"refund question vs current policy {r['v2_sim']}, vs retracted policy {r['v1_sim']}; "
          f"the two policies vs each other {r['v1_v2_sim']}")
    print(f"recall@3: query and index from the same model {r['same_model']}, from different models {r['mixed_models']}")
    assert not r["shared_words"] and r["paraphrase_sim"] > 0.5
    assert r["v2_sim"] - r["v1_sim"] < 0.02 and r["v1_v2_sim"] > 0.95
    assert r["same_model"] > 0.8 and r["mixed_models"] < 0.3
    print("embeddings ok")
