"""Chunking decides what can be found. The same questions, the same search, three ways to cut.

A question counts as answered when one of the top 3 chunks contains the whole answer fact.
Run: python3 chunking_demo.py
"""
from corpus import EVAL
from mini_rag import CUSTOMER, Index, build_chunks, chunk_by_section, chunk_fixed


def answered(index, method, k=3):
    """How many questions get their fact in the top k, and the average words handed to the model."""
    hits = words = 0
    for e in EVAL:
        top = getattr(index, method)(e["q"], k, CUSTOMER)
        hits += any(e["fact"] in index.get(cid)["text"] for _, cid in top)
        words += sum(len(index.get(cid)["text"].split()) for _, cid in top)
    return hits, round(words / len(EVAL))


def split_facts(chunks):
    """Facts that no single chunk contains whole, so no search can return them intact."""
    return [e["fact"] for e in EVAL if not any(e["fact"] in c["text"] for c in chunks)]


def main():
    plans = {
        "by section": build_chunks(chunk_by_section),
        "fixed 80 chars": build_chunks(chunk_fixed, size=80),
        "fixed 80, overlap 30": build_chunks(chunk_fixed, size=80, overlap=30),
        "fixed 200 chars": build_chunks(chunk_fixed, size=200),
    }
    out = {}
    for name, chunks in plans.items():
        index = Index(chunks)
        hits, words = answered(index, "hybrid")
        out[name] = dict(chunks=len(chunks), split=split_facts(chunks), hybrid=hits, words=words)
    return out


if __name__ == "__main__":
    r = main()
    for name, v in r.items():
        print(f"{name:22s} {v['chunks']:3d} chunks  answered@3 (hybrid) {v['hybrid']}/{len(EVAL)}  "
              f"{v['words']} words sent per question  facts split across chunks: {v['split']}")
    sec, fixed, over, big = (r[k] for k in ("by section", "fixed 80 chars", "fixed 80, overlap 30", "fixed 200 chars"))
    assert sec["split"] == [] and len(fixed["split"]) == 2          # blind cuts slice two answers in half
    assert over["split"] == [] and over["chunks"] > fixed["chunks"]  # overlap rescues them, with more chunks
    assert sec["hybrid"] > over["hybrid"] > fixed["hybrid"]
    assert big["hybrid"] >= sec["hybrid"] and big["words"] > 1.3 * sec["words"]   # big chunks: found, but a third more to read
    print("chunking ok")
