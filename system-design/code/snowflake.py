"""A Snowflake-style 64-bit ID generator and what it does when the clock moves back. Run: python3 snowflake.py"""
EPOCH = 1_288_834_974_657  # Twitter's custom epoch, in milliseconds
TS_BITS, MACHINE_BITS, SEQ_BITS = 41, 10, 12


class Snowflake:
    def __init__(self, machine, clock):
        self.machine, self.clock, self.last, self.seq = machine, clock, -1, 0

    def next(self):
        now = self.clock()
        if now < self.last:
            raise RuntimeError(f"clock moved back {self.last - now} ms; refuse to issue IDs")
        if now == self.last:
            self.seq = (self.seq + 1) & ((1 << SEQ_BITS) - 1)
            if self.seq == 0:                       # 4,096 IDs in this millisecond: wait for the next one
                while now <= self.last:
                    now = self.clock()
        else:
            self.seq = 0
        self.last = now
        return ((now - EPOCH) << (MACHINE_BITS + SEQ_BITS)) | (self.machine << SEQ_BITS) | self.seq


if __name__ == "__main__":
    t = [1_700_000_000_000]
    g = Snowflake(machine=7, clock=lambda: t[0])
    ids = [g.next() for _ in range(5)]
    t[0] += 1
    ids.append(g.next())
    print("IDs:", ids[:3], "... sorted by time:", ids == sorted(ids))
    years = (1 << TS_BITS) / (1000 * 3600 * 24 * 365.25)
    print(f"41 timestamp bits last {years:.1f} years; {1 << MACHINE_BITS} machines; {1 << SEQ_BITS} IDs per ms per machine")
    t[0] -= 5
    try:
        g.next()
        raised = False
    except RuntimeError as e:
        raised = True
        print("clock rollback:", e)
    assert ids == sorted(ids) and len(set(ids)) == len(ids)
    assert round(years, 1) == 69.7 and raised
    assert (ids[0] >> (MACHINE_BITS + SEQ_BITS)) + EPOCH == 1_700_000_000_000
    print("snowflake ok")
