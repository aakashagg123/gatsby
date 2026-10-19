"""Read-your-writes on a lagging follower, and the fix. Run: python3 replication_lag.py"""


class Cluster:
    def __init__(self, lag):
        self.lag = lag                    # seconds before a write reaches the follower
        self.leader, self.follower = {}, {}
        self.pending = []                 # (arrives_at, key, value)

    def write(self, now, key, value):
        self.leader[key] = value
        self.pending.append((now + self.lag, key, value))

    def tick(self, now):
        for item in [p for p in self.pending if p[0] <= now]:
            self.follower[item[1]] = item[2]
        self.pending = [p for p in self.pending if p[0] > now]

    def read(self, now, key, last_write_at=None, sticky_window=None):
        """Reads go to the follower, unless the user wrote recently: then read the leader."""
        self.tick(now)
        if sticky_window is not None and last_write_at is not None and now - last_write_at < sticky_window:
            return self.leader.get(key)
        return self.follower.get(key)


if __name__ == "__main__":
    c = Cluster(lag=2.0)
    c.leader["photo"] = "old.jpg"
    c.follower["photo"] = "old.jpg"
    c.write(10.0, "photo", "new.jpg")
    stale = c.read(10.5, "photo")                                    # refresh half a second later
    fixed = c.read(10.5, "photo", last_write_at=10.0, sticky_window=5.0)
    later = c.read(13.0, "photo")                                    # after the lag the follower has caught up
    print(f"0.5 s after the write: follower read {stale}, read-your-writes read {fixed}; 3 s later the follower reads {later}")
    assert stale == "old.jpg" and fixed == "new.jpg" and later == "new.jpg"
    print("replication lag ok")
