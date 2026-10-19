"""Cache policies under a skewed load: hit rate with an LRU cache, and what a write-back cache loses when it crashes.
Run: python3 cache_policies.py"""
import random
from collections import OrderedDict


class LRU:
    def __init__(self, capacity):
        self.capacity, self.data = capacity, OrderedDict()

    def get(self, k):
        if k in self.data:
            self.data.move_to_end(k)
            return self.data[k]
        return None

    def put(self, k, v):
        self.data[k] = v
        self.data.move_to_end(k)
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)


def zipf_keys(n_keys, n_requests, s=1.1, seed=7):
    rng = random.Random(seed)
    weights = [1 / (i + 1) ** s for i in range(n_keys)]
    return rng.choices(range(n_keys), weights=weights, k=n_requests)


def hit_rate(capacity, requests):
    c, hits = LRU(capacity), 0
    for k in requests:
        if c.get(k) is not None:
            hits += 1
        else:
            c.put(k, "v")                              # cache-aside: read the database, fill the cache
    return hits / len(requests)


def write_back_loss(writes, flush_every, crash_at):
    """Writes are buffered and flushed to the database in batches. A crash loses the unflushed buffer."""
    db, buffer = [], []
    for i in range(writes):
        buffer.append(i)
        if len(buffer) == flush_every:
            db.extend(buffer)
            buffer = []
        if i == crash_at:
            return len(buffer)                         # lost with the cache
    return 0


if __name__ == "__main__":
    reqs = zipf_keys(n_keys=100_000, n_requests=200_000)
    small, large = hit_rate(1_000, reqs), hit_rate(10_000, reqs)
    print(f"skewed load over 100,000 keys: an LRU cache of 1,000 entries hits {small:.0%}, of 10,000 entries hits {large:.0%}")
    lost = write_back_loss(writes=1_000, flush_every=100, crash_at=457)
    print(f"write-back cache flushed every 100 writes, crash after write 457: {lost} acknowledged writes lost; write-through loses 0")
    assert small > 0.4 and large > small
    assert lost == 58
    print("cache policies ok")
