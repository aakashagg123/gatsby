-- RAG on Postgres with pgvector. The schema and the four queries that lesson 9 walks through.
-- pgvector_demo.py fills the table with the invented Fernpay corpus and runs each query.
-- The vector size is 30 because the toy embedding in mini_rag.py has 30 numbers.
-- A real embedding model has hundreds or thousands: change vector(30) to match it.

-- name: schema
CREATE EXTENSION IF NOT EXISTS vector;
DROP TABLE IF EXISTS chunks;
CREATE TABLE chunks (
    id        text PRIMARY KEY,          -- 'refunds-v2#0': document id + section number
    doc       text NOT NULL,
    title     text NOT NULL,
    section   text NOT NULL,
    body      text NOT NULL,
    status    text NOT NULL,             -- 'current' or 'retracted'
    audience  text NOT NULL,             -- 'customer' or 'internal'
    updated   text NOT NULL,
    embedding vector(30) NOT NULL,
    -- keyword search: a full-text column Postgres keeps up to date by itself
    fts       tsvector GENERATED ALWAYS AS (to_tsvector('english', title || ' ' || body)) STORED
);

-- name: indexes
-- HNSW is the approximate nearest-neighbour index. The operator class must match the
-- distance the queries use: vector_cosine_ops for <=> (cosine distance).
CREATE INDEX chunks_embedding_hnsw ON chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX chunks_fts_gin ON chunks USING gin (fts);
CREATE INDEX chunks_filter ON chunks (status, audience);

-- name: vector_top3
-- Nearest chunks by cosine distance. 1 - distance is the cosine similarity.
SELECT id, round((1 - (embedding <=> :'qvec'))::numeric, 3) AS similarity
FROM chunks
ORDER BY embedding <=> :'qvec'
LIMIT 3;

-- name: vector_top3_filtered
-- The same search, limited to current documents a customer may see.
SELECT id, round((1 - (embedding <=> :'qvec'))::numeric, 3) AS similarity
FROM chunks
WHERE status = 'current' AND audience = 'customer'
ORDER BY embedding <=> :'qvec'
LIMIT 3;

-- name: keyword_top3
-- Postgres full-text search. websearch_to_tsquery reads plain user text.
SELECT id, round(ts_rank(fts, q)::numeric, 3) AS rank
FROM chunks, websearch_to_tsquery('english', :'qtext') AS q
WHERE fts @@ q AND status = 'current' AND audience = 'customer'
ORDER BY ts_rank(fts, q) DESC
LIMIT 3;

-- name: hybrid_top3
-- Reciprocal rank fusion: each list gives a chunk 1 / (60 + its rank). Sum and sort.
WITH vec AS (
    SELECT id, row_number() OVER (ORDER BY embedding <=> :'qvec') AS r
    FROM chunks WHERE status = 'current' AND audience = 'customer'
    ORDER BY embedding <=> :'qvec' LIMIT 20
), kw AS (
    SELECT id, row_number() OVER (ORDER BY ts_rank(fts, q) DESC) AS r
    FROM chunks, websearch_to_tsquery('english', :'qtext') AS q
    WHERE fts @@ q AND status = 'current' AND audience = 'customer'
    ORDER BY ts_rank(fts, q) DESC LIMIT 20
)
SELECT id, round(sum(1.0 / (60 + r)), 4) AS score
FROM (SELECT * FROM vec UNION ALL SELECT * FROM kw) AS both_lists
GROUP BY id
ORDER BY score DESC, id
LIMIT 3;

-- name: plan
-- Show that the query uses the HNSW index. On 22 rows Postgres prefers a plain scan,
-- so the demo turns sequential scans off for this one statement.
SET enable_seqscan = off;
EXPLAIN (COSTS OFF) SELECT id FROM chunks ORDER BY embedding <=> :'qvec' LIMIT 3;
