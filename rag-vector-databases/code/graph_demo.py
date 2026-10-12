"""Where flat retrieval runs out: a multi-hop question and a counting question.

The facts are invented. Each fact is one short chunk, the way an ingestion pipeline would store
it. Flat retrieval returns the top chunks for the question. A graph walk follows the links.
Run: python3 graph_demo.py
"""
from mini_rag import Index

# (subject, relation, object): suppliers make parts, parts go into products, customers buy products.
FACTS = [
    ("Kestrel Metals", "makes", "hinge H-7"), ("Kestrel Metals", "makes", "bracket B-2"),
    ("Orrin Plastics", "makes", "casing C-1"), ("Orrin Plastics", "makes", "clip K-4"),
    ("hinge H-7", "goes into", "Atlas desk"), ("bracket B-2", "goes into", "Atlas shelf"),
    ("casing C-1", "goes into", "Vega lamp"), ("clip K-4", "goes into", "Atlas desk"),
    ("Brightwell Hotels", "buys", "Atlas desk"), ("Northgate School", "buys", "Atlas shelf"),
    ("Pine & Co", "buys", "Vega lamp"), ("Harbor Clinic", "buys", "Vega lamp"),
    ("Harbor Clinic", "buys", "Atlas desk"),
]
RENEWALS = [("Brightwell Hotels", "Q3"), ("Northgate School", "Q1"), ("Pine & Co", "Q3"),
            ("Harbor Clinic", "Q3"), ("Lumen Labs", "Q3"), ("Oak Dental", "Q2"), ("Ridge Farms", "Q3")]


def chunks():
    out = [dict(id=f"fact#{n}", text=f"{s} {r} {o}.", status="current", audience="customer", title="", section="")
           for n, (s, r, o) in enumerate(FACTS)]
    out += [dict(id=f"renewal#{n}", text=f"The contract with {c} renews in {q}.", status="current",
                 audience="customer", title="", section="") for n, (c, q) in enumerate(RENEWALS)]
    return out


def walk(start):
    """Follow makes -> goes into -> bought by. Returns the customers and the path used."""
    parts = {o for s, r, o in FACTS if s == start and r == "makes"}
    products = {o for s, r, o in FACTS if s in parts and r == "goes into"}
    customers = {s for s, r, o in FACTS if o in products and r == "buys"}
    return customers, (parts, products)


def main(k=5):
    index = Index(chunks())
    q = "Which customers are exposed to the recall at Kestrel Metals?"
    flat = [index.get(cid)["text"] for _, cid in index.hybrid(q, k)]
    truth, path = walk("Kestrel Metals")
    named = {c for c in truth if any(c in t for t in flat)}
    count_q = "How many contracts renew in Q3?"
    count_flat = [index.get(cid)["text"] for _, cid in index.hybrid(count_q, 3)]
    true_count = sum(1 for _, q3 in RENEWALS if q3 == "Q3")
    return dict(flat=flat, truth=truth, path=path, named=named,
                count_flat=sum("Q3" in t for t in count_flat), true_count=true_count)


if __name__ == "__main__":
    r = main()
    print("flat retrieval, top 5 chunks:")
    for t in r["flat"]:
        print("   ", t)
    print(f"customers named in those chunks: {sorted(r['named']) or 'none'}")
    print(f"graph walk: parts {sorted(r['path'][0])} -> products {sorted(r['path'][1])} -> customers {sorted(r['truth'])}")
    print(f"'How many contracts renew in Q3?' top-3 chunks show {r['count_flat']}; a count over the table gives {r['true_count']}")
    assert r["truth"] == {"Brightwell Hotels", "Northgate School", "Harbor Clinic"}
    assert len(r["named"]) < len(r["truth"])            # similarity finds the supplier, not the chain
    assert r["count_flat"] < r["true_count"] == 5       # top-k can never count past k
    print("graph ok")
