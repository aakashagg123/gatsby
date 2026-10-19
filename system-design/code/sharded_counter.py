"""A viral post gets thousands of likes per second. One counter row is a hot spot. Spread the writes over shards and add
them on read. Run: python3 sharded_counter.py"""
import random


def max_writes_per_row(likes, shards, seed=1):
    rng = random.Random(seed)
    rows = [0] * shards
    for _ in range(likes):
        rows[rng.randrange(shards)] += 1
    return max(rows), sum(rows)


class Likes:
    def __init__(self):
        self.seen = set()
        self.count = 0

    def like(self, user, post):
        if (user, post) in self.seen:               # double taps do not double count
            return False
        self.seen.add((user, post))
        self.count += 1
        return True


if __name__ == "__main__":
    one, total1 = max_writes_per_row(50_000, 1)
    sixteen, total16 = max_writes_per_row(50_000, 16)
    l = Likes()
    taps = [l.like("u1", "p1") for _ in range(3)] + [l.like("u2", "p1")]
    print(f"50,000 likes in a second: busiest row takes {one:,} writes with 1 counter and {sixteen:,} with 16 shards; reads sum the shards ({total16:,})")
    print(f"double tap by u1 counted once: results {taps}, count {l.count}")
    assert total1 == total16 == 50_000 and sixteen < one / 10
    assert taps == [True, False, False, True] and l.count == 2
    print("sharded counter ok")
