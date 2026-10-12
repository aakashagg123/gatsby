"""Run the Fernpay corpus through Postgres + pgvector and compare with mini_rag.py.

Needs a Postgres server with the pgvector extension and the psql client. It uses the
standard PG* variables (PGHOST, PGPORT, PGUSER, PGDATABASE). Quick start with Docker:

    docker run -d --name rag-pg -e POSTGRES_PASSWORD=pw -p 5432:5432 pgvector/pgvector:0.8.1-pg16
    PGHOST=localhost PGUSER=postgres PGPASSWORD=pw python3 pgvector_demo.py

With no server it prints a skip message and exits 0, so the test runner stays green.
Run: python3 pgvector_demo.py
"""
import os
import re
import shutil
import subprocess

from mini_rag import CUSTOMER, Index, build_chunks, embed

HERE = os.path.dirname(os.path.abspath(__file__))


def sections():
    text = open(os.path.join(HERE, "pgvector_demo.sql")).read()
    parts = re.split(r"^-- name: (\w+)\n", text, flags=re.M)
    return {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}


def psql(script):
    out = subprocess.run(["psql", "-X", "-q", "-A", "-t", "-F", "|", "-v", "ON_ERROR_STOP=1"],
                         input=script, capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip())
    return [line.split("|") for line in out.stdout.strip().splitlines() if line]


def literal(s):
    return "'" + s.replace("'", "''") + "'"


def vec(v):
    return "[" + ",".join(f"{x:.6f}" for x in v) + "]"


def run_query(sql, name, query):
    head = f"\\set qvec {literal(vec(embed(query)))}\n\\set qtext {literal(query)}\n"
    return psql(head + sql[name])


def main():
    if not shutil.which("psql"):
        return None
    try:
        psql("SELECT 1;")
    except Exception:
        return None
    sql = sections()
    chunks = build_chunks()
    rows = ",\n".join(
        "(" + ", ".join(literal(c[k]) for k in ("id", "doc", "title", "section", "text", "status", "audience", "updated"))
        + f", {literal(vec(embed(c['text'])))})" for c in chunks)
    psql(sql["schema"] + sql["indexes"]
         + f"INSERT INTO chunks (id, doc, title, section, body, status, audience, updated, embedding) VALUES\n{rows};\n")
    version = psql("SELECT extversion FROM pg_extension WHERE extname = 'vector';")[0][0]
    q_refund = "can I get my money back on a yearly plan"
    q_code = "what does E-4021 mean"
    out = dict(
        version=version, count=int(psql("SELECT count(*) FROM chunks;")[0][0]),
        vector=run_query(sql, "vector_top3", q_refund),
        vector_filtered=run_query(sql, "vector_top3_filtered", q_refund),
        keyword_code=run_query(sql, "keyword_top3", q_code),
        vector_code=run_query(sql, "vector_top3_filtered", q_code),
        hybrid_code=run_query(sql, "hybrid_top3", q_code),
        plan=" ".join(r[0].strip() for r in run_query(sql, "plan", q_refund)),
    )
    index = Index(chunks)
    out["python_vector"] = index.vector_search(q_refund, 3)
    out["python_vector_filtered"] = index.vector_search(q_refund, 3, CUSTOMER)
    return out


if __name__ == "__main__":
    r = main()
    if r is None:
        print("pgvector demo skipped: no reachable Postgres (set PGHOST etc.; see the docstring)")
        raise SystemExit(0)
    print(f"pgvector {r['version']}, {r['count']} chunks loaded")
    for k in ("vector", "vector_filtered", "keyword_code", "vector_code", "hybrid_code"):
        print(f"{k:16s}", r[k])
    print("plan:", r["plan"])
    ids = lambda rows: [row[0] for row in rows]
    assert ids(r["vector"]) == [cid for _, cid in r["python_vector"]]                 # same ranking as the Python index
    assert ids(r["vector_filtered"]) == [cid for _, cid in r["python_vector_filtered"]]
    assert abs(float(r["vector"][0][1]) - r["python_vector"][0][0]) < 0.001          # same cosine similarity
    assert "refunds-v1#0" in ids(r["vector"]) and "refunds-v1#0" not in ids(r["vector_filtered"])
    assert ids(r["keyword_code"])[0] == "errors#0" and "errors#0" not in ids(r["vector_code"])
    assert ids(r["hybrid_code"])[0] == "errors#0"
    assert "chunks_embedding_hnsw" in r["plan"]
    print("pgvector demo ok")
