"""Exact versus approximate nearest-neighbour search, and the filter trap.

An IVF-style index (inverted file) groups vectors into lists around centres found by k-means.
A query scans only the nprobe lists whose centres are closest. Fewer lists scanned is faster,
and sometimes misses a true neighbour. The vectors are random but clustered, with a fixed seed.
Run: python3 ann_demo.py
"""
import math
import random

N, D, CLUSTERS, LISTS, K, QUERIES, TENANTS = 5000, 12, 40, 32, 10, 40, 50


def unit(v):
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def make_data(rng):
    centres = [unit([rng.gauss(0, 1) for _ in range(D)]) for _ in range(CLUSTERS)]
    pts = []
    for _ in range(N):
        c = rng.choice(centres)
        pts.append(unit([x + rng.gauss(0, 0.35) for x in c]))
    tenant = [rng.randrange(TENANTS) for _ in range(N)]
    return pts, tenant


def kmeans(pts, k, rng, iters=4):
    cents = rng.sample(pts, k)
    for _ in range(iters):
        groups = [[] for _ in range(k)]
        for i, p in enumerate(pts):
            groups[max(range(k), key=lambda j: dot(p, cents[j]))].append(i)
        cents = [unit([sum(pts[i][d] for i in g) for d in range(D)]) if g else cents[j]
                 for j, g in enumerate(groups)]
    return cents, groups


def exact(pts, q, k, keep=None):
    ids = range(len(pts)) if keep is None else keep
    return [i for _, i in sorted(((dot(q, pts[i]), i) for i in ids), reverse=True)[:k]]


def ivf_search(pts, cents, groups, q, k, nprobe):
    near = sorted(range(len(cents)), key=lambda j: -dot(q, cents[j]))[:nprobe]
    cand = [i for j in near for i in groups[j]]
    return exact(pts, q, k, cand), len(cand)


def main():
    rng = random.Random(42)
    pts, tenant = make_data(rng)
    cents, groups = kmeans(pts, LISTS, rng)
    queries = [unit([x + rng.gauss(0, 0.3) for x in rng.choice(pts)]) for _ in range(QUERIES)]
    truth = [exact(pts, q, K) for q in queries]
    sweep = {}
    for nprobe in (1, 2, 4, 8, LISTS):
        rec = scanned = 0
        for q, t in zip(queries, truth):
            got, n = ivf_search(pts, cents, groups, q, K, nprobe)
            rec += len(set(got) & set(t)) / K
            scanned += n
        sweep[nprobe] = (round(rec / QUERIES, 3), round(100 * scanned / (QUERIES * N), 1))
    # The filter trap: search first, then keep one tenant's rows (2% of the data).
    post, pre = 0, 0
    for n, q in enumerate(queries):
        t = n % TENANTS
        top40, _ = ivf_search(pts, cents, groups, q, 4 * K, 4)
        post += len([i for i in top40 if tenant[i] == t][:K])
        pre += len(exact(pts, q, K, [i for i in range(N) if tenant[i] == t]))
    return dict(sweep=sweep, post_filter=round(post / QUERIES, 1), pre_filter=round(pre / QUERIES, 1))


if __name__ == "__main__":
    r = main()
    print(f"{N} vectors, {D} numbers each, {LISTS} lists, top-{K}, {QUERIES} queries")
    for nprobe, (rec, pct) in r["sweep"].items():
        print(f"  scan {nprobe:2d} lists: recall@{K} {rec:.3f}, {pct:5.1f}% of vectors compared")
    print(f"one tenant (2% of rows): search-then-filter returns {r['post_filter']} of {K} results; "
          f"filter-then-search returns {r['pre_filter']}")
    s = r["sweep"]
    assert s[LISTS][0] == 1.0 and s[LISTS][1] == 100.0          # scanning every list is exact search
    assert s[1][0] < s[4][0] < s[LISTS][0] and s[4][1] < 25      # recall rises with work done
    assert r["post_filter"] < 2 and r["pre_filter"] == K
    print("ann ok")
