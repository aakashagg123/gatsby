"""The same Fernpay pipeline on Pinecone. NOT EXECUTED in this repo's checks.

It needs a Pinecone account, an API key and network access, so test_examples.py does not run it.
Written against the Pinecone Python SDK 10.0.0 (released 2026-09-03) and its document API:
an index declares a schema, and you read and write it through index.documents.
Check the SDK docs for your version before you run it; v10 changed the create and search calls.

    pip install "pinecone>=10,<11"
    export PINECONE_API_KEY=...
    python3 pinecone_example.py
"""
from pinecone import DenseVectorQuery, Pinecone, TextQuery

from mini_rag import CUSTOMER, DIM, build_chunks, embed

INDEX = "fernpay-help"
TENANT = "fernpay"          # one namespace per tenant keeps tenants apart


def create_index(pc):
    # Only searched fields go in the schema. Metadata used for filters is indexed on write.
    pc.indexes.create(
        name=INDEX,
        schema={"fields": {
            "embedding": {"type": "dense_vector", "dimension": DIM, "metric": "cosine"},
            "body": {"type": "string", "full_text_search": {"language": "en"}},
        }},
        deployment={"deployment_type": "managed", "cloud": "aws", "region": "us-east-1"},
    )


def load(index):
    docs = [{"_id": c["id"], "embedding": embed(c["text"]), "body": c["text"],
             "doc": c["doc"], "title": c["title"], "status": c["status"], "audience": c["audience"], "updated": c["updated"]}
            for c in build_chunks()]
    index.documents.upsert(namespace=TENANT, documents=docs)   # applied asynchronously


def search(index, question, k=3):
    flt = {"status": {"$eq": CUSTOMER["status"]}, "audience": {"$eq": CUSTOMER["audience"]}}
    # A dense-vector clause must run alone, so hybrid search is two searches plus fusion.
    dense = index.documents.search(namespace=TENANT, top_k=20, filter=flt,
                                   score_by=[DenseVectorQuery(field="embedding", values=embed(question))])
    text = index.documents.search(namespace=TENANT, top_k=20, filter=flt,
                                  score_by=[TextQuery(query=question, fields=["body"])])
    votes = {}
    for ranked in (dense.matches, text.matches):
        for rank, doc in enumerate(ranked, start=1):
            votes[doc.id] = votes.get(doc.id, 0) + 1 / (60 + rank)
    return sorted(votes.items(), key=lambda x: -x[1])[:k]


def retract(index, doc_id):
    # Freshness: when a document is withdrawn, delete its chunks by metadata filter.
    index.documents.delete(namespace=TENANT, filter={"doc": {"$eq": doc_id}})


if __name__ == "__main__":
    pc = Pinecone()                       # reads PINECONE_API_KEY
    create_index(pc)                      # blocks until the index is ready
    idx = pc.index(INDEX)
    load(idx)
    print(search(idx, "what does E-4021 mean"))
