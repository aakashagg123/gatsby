"""Consistent hashing: how many keys move, and what virtual nodes do for balance. Run: python3 consistent_hash.py"""
import bisect
import hashlib


def h(s):
    return int(hashlib.md5(s.encode()).hexdigest(), 16)


class Ring:
    def __init__(self, nodes, vnodes=1):
        self.points = sorted((h(f"{n}#{i}"), n) for n in nodes for i in range(vnodes))
        self.keys = [p for p, _ in self.points]

    def owner(self, key):
        i = bisect.bisect(self.keys, h(key)) % len(self.points)
        return self.points[i][1]


def moved(before, after, keys):
    return sum(1 for k in keys if before(k) != after(k)) / len(keys)


def balance(ring, keys, nodes):
    counts = {n: 0 for n in nodes}
    for k in keys:
        counts[ring.owner(k)] += 1
    return max(counts.values()) / (len(keys) / len(nodes))


if __name__ == "__main__":
    keys = [f"user:{i}" for i in range(20000)]
    nodes = [f"s{i}" for i in range(10)]
    mod_before = lambda k: h(k) % 10
    mod_after = lambda k: h(k) % 11
    r1, r2 = Ring(nodes, 100), Ring(nodes + ["s10"], 100)
    mv_mod = moved(mod_before, mod_after, keys)
    mv_ring = moved(r1.owner, r2.owner, keys)
    print(f"add 1 node to 10: hash mod N moves {mv_mod:.0%} of keys, ring with 100 vnodes moves {mv_ring:.1%} (ideal {1/11:.1%})")
    for v in (1, 10, 100):
        print(f"  {v:3d} vnodes per server: busiest server holds {balance(Ring(nodes, v), keys, nodes):.2f}x the average")
    assert mv_mod > 0.85 and 0.05 < mv_ring < 0.14
    assert balance(Ring(nodes, 100), keys, nodes) < balance(Ring(nodes, 1), keys, nodes)
    print("consistent hash ok")
