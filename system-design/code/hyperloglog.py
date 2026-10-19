"""HyperLogLog: count distinct items in a few kilobytes. Each item is hashed; the registers remember the longest run of
leading zero bits seen per bucket. Run: python3 hyperloglog.py"""
import hashlib
import math

P = 14                     # 2**14 registers, as in Redis
M = 1 << P


def h64(x):
    return int.from_bytes(hashlib.sha256(str(x).encode()).digest()[:8], "big")


class HLL:
    def __init__(self):
        self.reg = [0] * M

    def add(self, x):
        v = h64(x)
        idx = v >> (64 - P)
        rest = (v << P) & ((1 << 64) - 1)
        rank = (64 - P) + 1 if rest == 0 else (64 - rest.bit_length()) + 1      # position of the first 1 bit
        self.reg[idx] = max(self.reg[idx], rank)

    def count(self):
        alpha = 0.7213 / (1 + 1.079 / M)
        est = alpha * M * M / sum(2.0 ** -r for r in self.reg)
        zeros = self.reg.count(0)
        if est <= 2.5 * M and zeros:
            est = M * math.log(M / zeros)           # small-range correction
        return est

    def merge(self, other):
        self.reg = [max(a, b) for a, b in zip(self.reg, other.reg)]


if __name__ == "__main__":
    a, b = HLL(), HLL()
    for i in range(100_000):
        a.add(i)
    for i in range(50_000, 150_000):
        b.add(i)
    ea, eb = a.count(), b.count()
    a.merge(b)
    eu = a.count()
    err = abs(ea - 100_000) / 100_000
    std = 1.04 / math.sqrt(M)
    print(f"{M:,} registers; 100,000 distinct items counted as {ea:,.0f} (error {err:.2%}); expected standard error {std:.2%}; union of two overlapping sets {eu:,.0f} (true 150,000)")
    assert err < 3 * std and abs(eu - 150_000) / 150_000 < 3 * std and abs(eb - 100_000) / 100_000 < 3 * std
    print("hyperloglog ok")
