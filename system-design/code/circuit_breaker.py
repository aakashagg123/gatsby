"""A circuit breaker with closed, open and half-open states, driven by a fake clock. Run: python3 circuit_breaker.py"""


class Breaker:
    def __init__(self, threshold=3, reset_after=30.0):
        self.threshold, self.reset_after = threshold, reset_after
        self.state, self.failures, self.opened_at = "closed", 0, 0.0

    def allow(self, now):
        if self.state == "open":
            if now - self.opened_at >= self.reset_after:
                self.state = "half-open"          # let one trial call through
                return True
            return False
        return True

    def record(self, now, ok):
        if ok:
            self.state, self.failures = "closed", 0
        else:
            self.failures += 1
            if self.state == "half-open" or self.failures >= self.threshold:
                self.state, self.opened_at = "open", now


if __name__ == "__main__":
    b = Breaker()
    calls_to_dependency = 0
    now = 0.0
    for _ in range(3):                           # the dependency is down: three failures trip the breaker
        calls_to_dependency += 1
        b.record(now, ok=False)
    tripped = b.state
    rejected = sum(1 for t in range(1, 21) if not b.allow(float(t)))    # 20 calls in the next 20 s are refused without calling
    probe_allowed = b.allow(31.0)                # after 30 s one trial call is allowed
    b.record(31.0, ok=False)                     # the trial fails: open again
    reopened = b.state
    assert b.allow(62.0)                         # another 30 s later, another trial
    b.record(62.0, ok=True)
    print(f"after 3 failures: {tripped}; {rejected} calls refused without touching the dependency; trial at 31 s fails -> {reopened}; trial at 62 s succeeds -> {b.state}")
    assert tripped == "open" and rejected == 20 and probe_allowed and reopened == "open" and b.state == "closed"
    print("circuit breaker ok")
