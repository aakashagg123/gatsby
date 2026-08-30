# Recap & real-world examples

*Part of [System design for the technical PM](./README.md)*

## TL;DR

This track covered **28 real-world systems** across eight lessons, from single-server scaling patterns to microsecond-latency stock exchanges. The systems span six categories — web-scale services, real-time communication, storage, geospatial, data infrastructure, and financial/transactional — but the same dozen patterns appear again and again. This recap maps every system at a glance, names the recurring patterns that connect them, and distills the practitioner-level takeaways that cut across all 28 designs.

> 🎯 **For the technical PM**
>
> **Why it matters** — Seeing the patterns that repeat across 28 systems gives you a vocabulary for evaluating any new design. You stop treating each system as a special case and start recognizing the shared building blocks and tradeoffs.
>
> **What it changes in your decisions** — When your team proposes an architecture, you can identify which of these 28 systems it most resembles, ask whether they've addressed that system's known failure modes, and check whether they've chosen the right consistency/availability tradeoff.
>
> **Ask your eng team** — *"Which of these established system designs is ours closest to, and what did we learn from their known failure modes?"*
>
> **Risk if ignored** — You reinvent solutions to problems that were solved a decade ago, miss failure modes that are well-documented in existing designs, and make avoidable tradeoff mistakes.

---

## The systems at a glance

| # | System | Lesson | Scale | Core tradeoff | Key mechanism |
|---|---|---|---|---|---|
| 1 | Scaling (single to millions) | [Foundations](./foundations-and-framework.md) | 0 to 10M+ users | Vertical vs. horizontal scaling | Stateless web tier, sharding |
| 2 | Back-of-envelope estimation | [Foundations](./foundations-and-framework.md) | Any | Precision vs. speed of analysis | Power-of-2 reasoning, latency table |
| 3 | Four-step framework | [Foundations](./foundations-and-framework.md) | Any | Breadth vs. depth in design | Scope, sketch, deep-dive, wrap-up |
| 4 | Rate limiter | [Building blocks](./core-building-blocks.md) | Millions of requests/sec | User experience vs. system protection | Token bucket, sliding window |
| 5 | Consistent hashing | [Building blocks](./core-building-blocks.md) | N nodes, dynamic membership | Even distribution vs. simplicity | Virtual nodes on a hash ring |
| 6 | Key-value store | [Building blocks](./core-building-blocks.md) | Billions of keys | Consistency vs. availability (CAP) | Quorum reads/writes, vector clocks |
| 7 | Unique ID generator | [Building blocks](./core-building-blocks.md) | Millions of IDs/sec | Sortability vs. coordination-freedom | Snowflake: timestamp + machine + sequence |
| 8 | URL shortener | [Web-scale](./web-scale-services.md) | 100M URLs | Read vs. write optimization | Base-62 encoding, 301/302 redirect |
| 9 | Web crawler | [Web-scale](./web-scale-services.md) | Billions of pages | Freshness vs. politeness | Priority queue, URL frontier, robots.txt |
| 10 | Notification system | [Web-scale](./web-scale-services.md) | Millions of pushes/min | Delivery reliability vs. latency | APNs/FCM, retry with backoff |
| 11 | News feed | [Web-scale](./web-scale-services.md) | 100M+ DAU | Fanout-on-write vs. fanout-on-read | Hybrid: push for normal, pull for celebrities |
| 12 | Chat system | [Real-time](./real-time-systems.md) | Millions concurrent | Consistency vs. real-time delivery | WebSocket, message queue, read receipts |
| 13 | Search autocomplete | [Real-time](./real-time-systems.md) | 100K QPS | Freshness vs. latency | Trie in memory, async updates |
| 14 | Video streaming | [Real-time](./real-time-systems.md) | Millions concurrent streams | Quality vs. bandwidth/cost | Adaptive bitrate, DAG transcoding, CDN |
| 15 | Google Drive (file sync) | [Storage](./storage-and-sync.md) | 50M users, 10GB each | Sync speed vs. bandwidth | 4MB blocks, delta sync, long polling |
| 16 | S3-like object storage | [Storage](./storage-and-sync.md) | 100 PB | Durability vs. storage cost | Erasure coding (8+4), WAL merging |
| 17 | Proximity service | [Location](./location-and-geo-services.md) | 200M businesses | Query speed vs. index complexity | Geohash + 8-neighbor lookup |
| 18 | Nearby friends | [Location](./location-and-geo-services.md) | 10M concurrent | Real-time accuracy vs. resource cost | WebSocket + Redis pub/sub |
| 19 | Google Maps | [Location](./location-and-geo-services.md) | 1B DAU | Tile freshness vs. CDN efficiency | Hierarchical routing, pre-rendered tiles |
| 20 | Distributed message queue | [Data infra](./data-infrastructure.md) | Millions msgs/sec | Durability vs. throughput | WAL, ISR replication, consumer groups |
| 21 | Metrics monitoring | [Data infra](./data-infrastructure.md) | 10M metrics | Resolution vs. storage cost | Down-sampling, double-delta encoding |
| 22 | Ad click aggregation | [Data infra](./data-infrastructure.md) | 1B clicks/day | Accuracy vs. latency | Kappa architecture, watermarking |
| 23 | Distributed email | [Data infra](./data-infrastructure.md) | 100K emails/sec | Deliverability vs. throughput | SPF/DKIM, IP warm-up, Cassandra by user |
| 24 | Hotel reservation | [Transactional](./transactional-and-financial.md) | ~3 TPS | Simplicity vs. concurrency | DB constraints, idempotency key |
| 25 | Gaming leaderboard | [Transactional](./transactional-and-financial.md) | 5M DAU | Memory vs. scale | Redis sorted sets, O(log N) ZRANK |
| 26 | Payment system | [Transactional](./transactional-and-financial.md) | Millions txn/day | Safety vs. speed | Double-entry ledger, PSP idempotency |
| 27 | Digital wallet | [Transactional](./transactional-and-financial.md) | 1M TPS | Consistency vs. throughput | Event sourcing + CQRS + Raft |
| 28 | Stock exchange | [Transactional](./transactional-and-financial.md) | 1B orders/day | Latency vs. distribution | Single-server mmap, custom sequencer |

---

## Recurring patterns

These patterns appear across many of the 28 systems. Recognizing them lets you transfer understanding from one system to another.

### 1. Separate metadata from data

The most universal pattern: store the catalog of what exists (metadata) separately from the content itself (data), because they have different consistency, access, and scaling requirements.

| System | Metadata | Data |
|---|---|---|
| Google Drive | File tree, versions, sharing (MySQL) | Blocks in cloud storage |
| S3 object storage | Bucket/object catalog (sharded RDBMS) | Blobs on data nodes |
| Distributed email | Headers, folders, labels (Cassandra) | Body/attachments in blob store |
| Video streaming | Video info, processing status (RDBMS) | Encoded segments on CDN |

### 2. Append-only logs (WAL)

Write-ahead logs appear as the foundational data structure in systems that prize write throughput and durability:

- **Kafka** — partitions are append-only logs on disk.
- **S3 data nodes** — small objects are appended to WAL files.
- **Stock exchange** — the event log of all orders and trades.
- **Digital wallet** — event sourcing stores every balance change as an appended event.
- **Key-value store** — LSM trees use WALs for crash recovery.

The pattern: convert random writes to sequential appends, gain throughput, and accept the cost of background compaction.

### 3. Idempotency keys

Every system where a retry is possible (which is every system that uses a network) must make writes idempotent:

- **Hotel reservation** — `reservation_id` as unique constraint.
- **Payment system** — `payment_order_id` as PSP idempotency key.
- **Ad click aggregation** — `(ad_id, window_start)` for deduplicated counts.
- **Notification system** — deduplication of push notifications by event ID.

The pattern: the client generates a unique key before the first attempt; the server uses it to detect and suppress duplicates.

### 4. Consistent hashing for shard distribution

Consistent hashing distributes data across nodes while minimizing reshuffling when nodes join or leave:

- **Key-value store** — partition keys across storage nodes.
- **Nearby friends** — distribute Redis pub/sub channels across a Redis cluster.
- **Distributed email** — Cassandra ring membership.
- **Digital wallet** — shard user balances across database instances.
- **Message queue** — assign partitions to brokers.

### 5. Event sourcing for auditability

When correctness and history matter more than raw performance, systems store events rather than state:

- **Stock exchange** — deterministic replay of every order for disaster recovery.
- **Digital wallet** — complete transaction history for regulatory compliance.
- **Ad click aggregation** — raw events retained for reprocessing when logic changes.
- **Payment system** — double-entry ledger entries are effectively events.

The cost: replaying billions of events is slow without periodic snapshots, and the storage footprint grows indefinitely.

### 6. Pub/sub for fan-out

When one event must reach many consumers, pub/sub decouples the producer from the consumer count:

- **Nearby friends** — Redis pub/sub channels per user.
- **News feed** — fanout-on-write pushes posts to follower inboxes.
- **Metrics monitoring** — Kafka topics fan out to dashboards, alerting, and archival.
- **Stock exchange** — UDP multicast for market data distribution.
- **Notification system** — event bus to APNs/FCM/SMS/email channels.

### 7. Tiered storage (hot/warm/cold)

Not all data is equally accessed. Tiering reduces cost without sacrificing access to recent data:

- **Google Drive** — SSD for recent files, HDD for older, archival for 90+ day dormant.
- **S3 object storage** — storage classes (Standard, Infrequent Access, Glacier).
- **Metrics monitoring** — full resolution for 7 days, down-sampled for months/years.
- **Message queue** — retention policy moves old segments off primary storage.

### 8. Geospatial indexing

Converting 2D coordinates to 1D sortable keys enables spatial queries on standard indexes:

- **Proximity service** — geohash prefix queries.
- **Google Maps** — tile addressing by zoom/x/y (geohash-like hierarchy).
- **Nearby friends** — location cache keyed by geohash for bootstrapping.

### 9. Real-time via persistent connections

When latency matters more than resource efficiency, persistent connections (WebSocket, long polling) replace HTTP polling:

- **Chat system** — WebSocket for message delivery.
- **Nearby friends** — WebSocket for location updates.
- **Google Drive** — long polling for sync notifications.
- **Search autocomplete** — persistent connection for keystroke-level latency.

### 10. Exactly-once via idempotent processing

Exactly-once delivery is impossible in a distributed system, but exactly-once *processing* is achievable by combining at-least-once delivery with idempotent consumers:

- **Kafka** — idempotent producer + transactional consumer.
- **Ad click aggregation** — deduplicated writes keyed by `(ad_id, window)`.
- **Payment system** — PSP idempotency key prevents double charges.
- **Hotel reservation** — unique constraint on `reservation_id`.

---

## The practitioner's takeaway

### Start with the constraints, not the technology

Every system in this track began with the same questions: What's the QPS? What's the storage? What's the latency budget? What's the consistency requirement? The answers — not the latest database trend — drive the architecture. A hotel reservation system at 3 TPS doesn't need Kafka. A stock exchange at 100K orders/sec doesn't need Kubernetes.

### Correctness and performance are in tension — pick explicitly

The systems divide cleanly into two camps:
- **Correctness-first** (payments, wallets, exchanges, reservations): accept higher latency and lower throughput for ACID, idempotency, and double-entry guarantees.
- **Throughput-first** (metrics, click aggregation, crawlers, news feed): accept eventual consistency and tolerate occasional duplicates or losses.

The worst designs are the ones that don't choose — they promise both and deliver neither.

### The metadata store is always the critical path

Across Google Drive, S3, email, video streaming, and the stock exchange, the metadata store is the single most critical component. Data can be replicated and reconstructed; metadata loss means the system doesn't know what it has. Invest disproportionately in metadata store durability, replication, and backup.

### Every retry is a potential duplicate

The moment you add a network between two components, you accept that operations may execute more than once. If you haven't made every write operation idempotent, you haven't designed a production system — you've designed a demo.

### Scaling is a sequence, not a choice

The [foundations lesson](./foundations-and-framework.md) laid out the scaling sequence: separate compute from storage, add load balancing, add replication, add caching, add sharding. Every system in this track follows some prefix of this sequence. The art is knowing where to stop — most systems don't need the full sequence, and jumping ahead (sharding before you've cached, caching before you've indexed) creates avoidable complexity.

### The gap between "works" and "works correctly at scale" is where careers are made

A URL shortener, a chat system, or a payment flow can be built in a weekend hackathon. Making it handle 100M users, survive node failures, reconcile every transaction, and maintain sub-200ms latency — that's the work this track is about. The designs here aren't clever algorithms; they're decades of production experience encoded as patterns and checklists.

---

## The full track

1. [Foundations & framework](./foundations-and-framework.md) — scaling, estimation, and the four-step design process
2. [Core building blocks](./core-building-blocks.md) — rate limiting, consistent hashing, key-value stores, unique ID generation
3. [Web-scale services](./web-scale-services.md) — URL shortener, web crawler, notification system, news feed
4. [Real-time systems](./real-time-systems.md) — chat, search autocomplete, video streaming
5. [Storage & sync](./storage-and-sync.md) — Google Drive file sync, S3-like object storage
6. [Location & geo services](./location-and-geo-services.md) — proximity service, nearby friends, Google Maps
7. [Data infrastructure](./data-infrastructure.md) — message queues, metrics monitoring, ad click aggregation, email
8. [Transactional & financial systems](./transactional-and-financial.md) — hotel reservation, leaderboard, payments, digital wallet, stock exchange

← [Transactional & financial systems](./transactional-and-financial.md) · [Back to overview](./README.md)
