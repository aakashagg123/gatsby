"""Quorum overlap: with R + W > N every read set meets every write set. Run: python3 quorum.py"""
from itertools import combinations


def always_overlaps(n, w, r):
    reps = range(n)
    return all(set(a) & set(b) for a in combinations(reps, w) for b in combinations(reps, r))


def stale_read_possible(n, w, r):
    return not always_overlaps(n, w, r)


if __name__ == "__main__":
    for n, w, r in [(3, 2, 2), (3, 1, 1), (3, 3, 1), (5, 3, 3), (5, 2, 2)]:
        print(f"N={n} W={w} R={r}: R+W={r + w} {'>' if r + w > n else '<='} N -> read always sees latest write: {always_overlaps(n, w, r)}")
    for n in range(1, 8):
        for w in range(1, n + 1):
            for r in range(1, n + 1):
                assert always_overlaps(n, w, r) == (r + w > n)
    print("quorum ok")
