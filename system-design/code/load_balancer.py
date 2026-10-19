"""Load balancing: round robin vs least connections, health-check removal and connection draining.
Run: python3 load_balancer.py"""
import itertools


class Pool:
    def __init__(self, servers):
        self.active = {s: 0 for s in servers}        # open connections per server
        self.healthy = set(servers)
        self.draining = set()
        self._rr = itertools.cycle(servers)

    def eligible(self):
        return [s for s in self.active if s in self.healthy and s not in self.draining]

    def pick_round_robin(self):
        for _ in range(len(self.active)):
            s = next(self._rr)
            if s in self.eligible():
                return s
        raise RuntimeError("no healthy server")

    def pick_least_connections(self):
        return min(self.eligible(), key=lambda s: self.active[s])

    def open(self, s):
        self.active[s] += 1

    def close(self, s):
        self.active[s] -= 1


def spread(policy, durations):
    """Assign requests with the given durations; return the largest number of open connections seen on one server."""
    pool = Pool(["a", "b", "c"])
    open_until, peak, t = [], 0, 0.0
    for d in durations:
        t += 0.1
        for end, s in [x for x in open_until if x[0] <= t]:
            pool.close(s)
        open_until = [x for x in open_until if x[0] > t]
        s = pool.pick_round_robin() if policy == "rr" else pool.pick_least_connections()
        pool.open(s)
        open_until.append((t + d, s))
        peak = max(peak, max(pool.active.values()))
    return peak


if __name__ == "__main__":
    # every third request is slow (5 s), the rest are fast (0.1 s). Round robin sends all slow ones to server "a".
    durations = [5.0 if i % 3 == 0 else 0.1 for i in range(60)]
    rr, lc = spread("rr", durations), spread("lc", durations)
    print(f"peak open connections on one server: round robin {rr}, least connections {lc}")
    p = Pool(["a", "b", "c"])
    p.healthy.discard("b")
    picks = {p.pick_round_robin() for _ in range(9)}
    p.draining.add("c")
    after_drain = {p.pick_round_robin() for _ in range(9)}
    print(f"after a failed health check on b, round robin used {sorted(picks)}; after draining c it used {sorted(after_drain)}")
    assert lc < rr and rr >= 4
    assert picks == {"a", "c"} and after_drain == {"a"}
    print("load balancer ok")
