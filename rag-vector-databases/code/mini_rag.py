"""A whole RAG pipeline in the Python standard library: chunk, embed, index, retrieve,
filter, fuse, cite and measure. No account, no API key, no install.

The embedding is a toy. A small hand-made table maps words to 22 concepts, and every other
word is hashed into 8 spare slots, for 30 numbers in all. A real embedding model learns its own map from
billions of sentences. The toy is just enough to show what an embedding does well
(paraphrase) and badly (exact codes).

Run: python3 mini_rag.py
"""
import math
import re
import zlib
from collections import Counter

from corpus import DOCS, EVAL

STOP = set("""a an the is are was be to of in on for and or it its my i you your we our me do does
how what when where which can at by as with from this that these there not no if then than so
get keep kept am has have had will would per each any all""".split())

# The toy embedding's "meaning map". A real model learns this. Here it is written by hand.
CONCEPTS = {
    "cancel": "cancel stop end ending ends quit terminate leave",
    "pay": "pay paying paid payment payments charge charged billing bill money cost costs price prices dollars",
    "refund": "refund refunded refunds back",
    "year": "annual yearly year",
    "month": "monthly month months every",
    "bank": "bank feed feeds connection connections reconnect login password",
    "slow": "timed timeout timing slow",
    "fail": "error errors fails failing rejected problem fix",
    "invoice": "invoice invoices",
    "client": "client clients customer customers",
    "auto": "automatic automatically recurring schedule reminder reminders nudge hand",
    "late": "overdue late unpaid",
    "where": "stored region residency kept frankfurt virginia germany eu",
    "data": "data workspace workspaces",
    "export": "export download csv spreadsheet file",
    "api": "api requests calls key keys developers",
    "limit": "limit limits minute rate",
    "tax": "tax vat sales reverse",
    "plan": "plan plans starter team subscription",
    "users": "users seats",
    "approve": "approval approve finance",
    "credit": "credit goodwill",
}
WORD2CONCEPT = {w: c for c, ws in CONCEPTS.items() for w in ws.split()}
CONCEPT_IDS = {c: i for i, c in enumerate(CONCEPTS)}
HASH_SLOTS = 8          # every other word lands in one of these spare slots
HASH_WEIGHT = 0.3
DIM = len(CONCEPTS) + HASH_SLOTS


def tokens(text):
    """Lower-case words. Codes such as e-4021 stay one token."""
    return [t for t in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text.lower()) if t not in STOP]


# ---------------------------------------------------------------- chunking
def chunk_by_section(doc):
    """One chunk per '## ' section. The section heading travels with the chunk."""
    parts = [p.strip() for p in doc["text"].split("\n## ") if p.strip()]
    out = []
    for n, part in enumerate(parts):
        heading, _, body = part.lstrip("# ").partition("\n")
        out.append(dict(id=f"{doc['id']}#{n}", doc=doc["id"], title=doc["title"], section=heading.strip(),
                        text=f"{doc['title']}. {heading.strip()}. {body.strip()}",
                        status=doc["status"], audience=doc["audience"], updated=doc["updated"]))
    return out


def chunk_fixed(doc, size=120, overlap=0):
    """Blind fixed-size chunks by character count, the common naive default."""
    body = re.sub(r"\s*## [^\n]*\n", " ", doc["text"]).strip()
    step, out, start = size - overlap, [], 0
    while start < len(body):
        out.append(dict(id=f"{doc['id']}~{len(out)}", doc=doc["id"], title=doc["title"], section="",
                        text=body[start:start + size], status=doc["status"],
                        audience=doc["audience"], updated=doc["updated"]))
        start += step
    return out


def build_chunks(chunker=chunk_by_section, **kw):
    return [c for d in DOCS for c in chunker(d, **kw)]


# ---------------------------------------------------------------- embedding
def embed(text):
    """Text -> unit-length vector of DIM numbers."""
    v = [0.0] * DIM
    for t in tokens(text):
        if t in WORD2CONCEPT:
            v[CONCEPT_IDS[WORD2CONCEPT[t]]] += 1.0
        else:
            v[len(CONCEPTS) + zlib.crc32(t.encode()) % HASH_SLOTS] += HASH_WEIGHT
    norm = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / norm for x in v]


def cosine(a, b):
    """Both vectors are unit length, so the dot product is the cosine similarity."""
    return sum(x * y for x, y in zip(a, b))


# ---------------------------------------------------------------- index and search
class Index:
    def __init__(self, chunks):
        self.chunks = chunks
        self.vectors = [embed(c["text"]) for c in chunks]
        # BM25 statistics for keyword search
        self.tf = [Counter(tokens(c["text"])) for c in chunks]
        self.lens = [sum(tf.values()) for tf in self.tf]
        self.avg_len = sum(self.lens) / len(self.lens)
        df = Counter(t for tf in self.tf for t in tf)
        n = len(chunks)
        self.idf = {t: math.log(1 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}

    def allowed(self, i, where):
        c = self.chunks[i]
        return all(c[k] in v if isinstance(v, (set, tuple, list)) else c[k] == v for k, v in where.items())

    def vector_search(self, query, k=5, where=None):
        q = embed(query)
        scored = [(cosine(q, v), i) for i, v in enumerate(self.vectors) if not where or self.allowed(i, where)]
        return [(round(s, 3), self.chunks[i]["id"]) for s, i in sorted(scored, reverse=True)[:k]]

    def bm25(self, query, k=5, where=None, k1=1.5, b=0.75):
        q = tokens(query)
        scored = []
        for i, tf in enumerate(self.tf):
            if where and not self.allowed(i, where):
                continue
            s = sum(self.idf.get(t, 0) * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * self.lens[i] / self.avg_len))
                    for t in q if t in tf)
            if s > 0:
                scored.append((s, i))
        return [(round(s, 3), self.chunks[i]["id"]) for s, i in sorted(scored, reverse=True)[:k]]

    def hybrid(self, query, k=5, where=None, depth=20, c=60):
        """Reciprocal rank fusion: each list votes 1 / (c + rank) for each chunk it returned."""
        votes = Counter()
        for ranked in (self.vector_search(query, depth, where), self.bm25(query, depth, where)):
            for rank, (_, cid) in enumerate(ranked, start=1):
                votes[cid] += 1 / (c + rank)
        return [(round(s, 4), cid) for cid, s in sorted(votes.items(), key=lambda x: (-x[1], x[0]))[:k]]

    def get(self, cid):
        return next(c for c in self.chunks if c["id"] == cid)


# ---------------------------------------------------------------- generation side
def has_evidence(index, question, where=None, min_cosine=0.35):
    """A blunt gate before generation. Answer only if the keyword leg finds a match,
    or the vector leg finds a close one. Otherwise the feature says it does not know."""
    top = index.vector_search(question, 1, where)
    return bool(index.bm25(question, 1, where)) or bool(top and top[0][0] >= min_cosine)


def build_prompt(index, question, hits):
    """Assemble the grounded prompt: an instruction, numbered sources, then the question."""
    lines = ["Answer only from the sources below. Cite each claim as [n].",
             "If the sources do not contain the answer, say you do not know.", ""]
    for n, (_, cid) in enumerate(hits, start=1):
        c = index.get(cid)
        lines.append(f"[{n}] {c['title']} > {c['section']} (updated {c['updated']}): {c['text']}")
    lines += ["", f"Question: {question}"]
    return "\n".join(lines)


# ---------------------------------------------------------------- evaluation
def recall_at_k(results, gold):
    return 1.0 if gold in [cid for _, cid in results] else 0.0


def reciprocal_rank(results, gold):
    for rank, (_, cid) in enumerate(results, start=1):
        if cid == gold:
            return 1 / rank
    return 0.0


def evaluate(index, method, k=3, where=None, questions=EVAL):
    rows = [(e, getattr(index, method)(e["q"], k, where)) for e in questions]
    recall = sum(recall_at_k(r, e["gold"]) for e, r in rows) / len(rows)
    mrr = sum(reciprocal_rank(r, e["gold"]) for e, r in rows) / len(rows)
    return round(recall, 3), round(mrr, 3), rows


CUSTOMER = dict(status="current", audience="customer")


def main():
    index = Index(build_chunks())
    report = {}
    for method in ("bm25", "vector_search", "hybrid"):
        recall, mrr, rows = evaluate(index, method, k=3, where=CUSTOMER)
        by_kind = {}
        for e, r in rows:
            by_kind.setdefault(e["kind"], []).append(recall_at_k(r, e["gold"]))
        report[method] = dict(recall=recall, mrr=mrr,
                              kinds={k: round(sum(v) / len(v), 2) for k, v in by_kind.items()},
                              misses=[e["q"] for e, r in rows if not recall_at_k(r, e["gold"])])
    q = "can I get my money back on a yearly plan"
    unfiltered = index.vector_search(q, 3)
    filtered = index.vector_search(q, 3, CUSTOMER)
    prompt = build_prompt(index, q, index.vector_search(q, 2, CUSTOMER))
    off_topic = "what is the weather in Lisbon tomorrow"
    gate = {x: has_evidence(index, x, CUSTOMER) for x in (q, off_topic, "what does E-4021 mean")}
    return dict(index=index, report=report, unfiltered=unfiltered, filtered=filtered, prompt=prompt,
                gate=gate, off_topic_top=index.vector_search(off_topic, 1, CUSTOMER),
                code_top=index.vector_search("what does E-4021 mean", 1, CUSTOMER))


if __name__ == "__main__":
    r = main()
    idx = r["index"]
    print(f"{len(idx.chunks)} chunks from {len(DOCS)} documents, {DIM}-number vectors, {len(EVAL)} eval questions")
    for m, v in r["report"].items():
        print(f"{m:14s} recall@3 {v['recall']:.3f}  MRR {v['mrr']:.3f}  by kind {v['kinds']}  misses {v['misses']}")
    print("no filter :", r["unfiltered"])
    print("filtered  :", r["filtered"])
    print("vector top hit, off-topic question:", r["off_topic_top"], "| code question:", r["code_top"])
    print("evidence gate:", r["gate"])
    print("\n" + r["prompt"])
    rep = r["report"]
    assert rep["hybrid"]["recall"] >= max(rep["bm25"]["recall"], rep["vector_search"]["recall"])
    assert rep["vector_search"]["kinds"]["paraphrase"] > rep["bm25"]["kinds"]["paraphrase"]
    assert rep["bm25"]["kinds"]["exact"] > rep["vector_search"]["kinds"]["exact"]
    assert any(cid.startswith("refunds-v1") for _, cid in r["unfiltered"])        # the retracted policy competes
    assert not any(cid.startswith("refunds-v1") for _, cid in r["filtered"])      # the filter removes it
    assert r["off_topic_top"][0][0] > r["code_top"][0][0]     # a cosine threshold alone cannot separate them
    assert r["gate"] == {"can I get my money back on a yearly plan": True,
                         "what is the weather in Lisbon tomorrow": False, "what does E-4021 mean": True}
    assert "[1]" in r["prompt"] and "refunds-v2#0" == r["filtered"][0][1]
    print("\nmini_rag ok")
