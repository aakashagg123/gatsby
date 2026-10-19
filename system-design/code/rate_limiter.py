"""Token bucket and sliding-window counter, driven by a fake clock. Run: python3 rate_limiter.py"""


class TokenBucket:
    def __init__(self, rate, capacity):
        self.rate, self.capacity, self.tokens, self.last = rate, capacity, capacity, 0.0

    def allow(self, now):
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


class SlidingWindowCounter:
    """Weights the previous fixed window by how much of it still overlaps the sliding window."""
    def __init__(self, limit, window):
        self.limit, self.window, self.counts = limit, window, {}

    def allow(self, now):
        cur = int(now // self.window)
        frac = (now % self.window) / self.window
        estimate = self.counts.get(cur - 1, 0) * (1 - frac) + self.counts.get(cur, 0)
        if estimate >= self.limit:
            return False
        self.counts[cur] = self.counts.get(cur, 0) + 1
        return True


def count_allowed(limiter, times):
    return sum(limiter.allow(t) for t in times)


if __name__ == "__main__":
    burst = [0.0] * 20
    tb = TokenBucket(rate=5, capacity=10)
    print("token bucket, 20 requests at once:", count_allowed(tb, burst), "allowed (capacity 10)")
    tb2 = TokenBucket(rate=5, capacity=10)
    steady = [i * 0.1 for i in range(100)]
    print("token bucket, 10 requests/s for 10 s:", count_allowed(tb2, steady), "allowed (rate 5/s)")
    # fixed window edge burst: 100 requests just before and just after a boundary
    edge = [9.99] * 100 + [10.01] * 100
    fixed = {}
    ok = 0
    for t in edge:
        w = int(t // 10)
        if fixed.get(w, 0) < 100:
            fixed[w] = fixed.get(w, 0) + 1
            ok += 1
    sw = SlidingWindowCounter(limit=100, window=10)
    sw_ok = count_allowed(sw, edge)
    print(f"edge burst of 200 around a window boundary, limit 100 per 10 s: fixed window allows {ok}, sliding counter allows {sw_ok}")
    assert count_allowed(TokenBucket(5, 10), burst) == 10
    assert 55 <= count_allowed(TokenBucket(5, 10), steady) <= 61
    assert ok == 200 and sw_ok < 110
    print("rate limiter ok")
