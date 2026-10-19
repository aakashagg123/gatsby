"""Approximate nearest neighbour search with a coarse index: put vectors in the bucket of their nearest centroid, then search
only the nearest few buckets. More buckets probed means better recall and more work. Run: python3 ann_search.py"""
import math
import random

DIM = 16


def unit(rng):
    v = [rng.gauss(0, 1) for _ in range(DIM)]
    n = math.sqrt(sum(x * x for x in v))
    return [x / n for x in v]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def build(n=20_000, n_centroids=64, seed=4):
    rng = random.Random(seed)
    data = [unit(rng) for _ in range(n)]
    centroids = [unit(rng) for _ in range(n_centroids)]
    buckets = {c: [] for c in range(n_centroids)}
    for i, v in enumerate(data):
        buckets[max(range(n_centroids), key=lambda c: dot(v, centroids[c]))].append(i)
    return rng, data, centroids, buckets


def search(data, centroids, buckets, q, nprobe, k=10):
    order = sorted(range(len(centroids)), key=lambda c: -dot(q, centroids[c]))[:nprobe]
    cand = [i for c in order for i in buckets[c]]
    return sorted(cand, key=lambda i: -dot(q, data[i]))[:k], len(cand)


if __name__ == "__main__":
    rng, data, centroids, buckets = build()
    queries = [unit(rng) for _ in range(30)]
    for nprobe in (1, 4, 16):
        rec, scanned = 0.0, 0
        for q in queries:
            truth = set(sorted(range(len(data)), key=lambda i: -dot(q, data[i]))[:10])
            got, n = search(data, centroids, buckets, q, nprobe)
            rec += len(truth & set(got)) / 10
            scanned += n
        print(f"probe {nprobe:2d} of 64 buckets: recall@10 {rec / len(queries):.0%}, scanned {scanned / len(queries) / len(data):.0%} of the vectors")
    r1 = None
    def recall(nprobe):
        r = 0.0
        for q in queries:
            truth = set(sorted(range(len(data)), key=lambda i: -dot(q, data[i]))[:10])
            r += len(truth & set(search(data, centroids, buckets, q, nprobe)[0])) / 10
        return r / len(queries)
    assert recall(1) < recall(4) < recall(16) + 1e-9 and recall(16) > 0.75
    print("ann search ok")
