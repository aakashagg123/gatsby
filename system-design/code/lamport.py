"""Logical clocks order causally related events; skewed wall clocks make last-write-wins drop the newest write.
Run: python3 lamport.py"""


class Lamport:
    def __init__(self):
        self.t = 0

    def event(self):
        self.t += 1
        return self.t

    def send(self):
        return self.event()

    def receive(self, remote):
        self.t = max(self.t, remote) + 1
        return self.t


def last_write_wins(writes):
    """writes: (timestamp, value). The highest timestamp wins."""
    return max(writes)[1]


if __name__ == "__main__":
    a, b = Lamport(), Lamport()
    a.event()
    send_ts = a.send()                  # A writes a post and tells B
    recv_ts = b.receive(send_ts)        # B reads it, then replies
    reply_ts = b.event()
    ordered = send_ts < recv_ts < reply_ts
    # wall clocks: server A runs 2 s fast. Its write at real time 5 is stamped 7. Server B writes later, at real time 6, stamped 6.
    wall = last_write_wins([(7.0, "x=1 (written first)"), (6.0, "x=2 (written last)")])
    print(f"logical clocks: send {send_ts} < receive {recv_ts} < reply {reply_ts}: {ordered}")
    print("last-write-wins with a 2 s clock skew keeps:", wall)
    assert ordered and wall == "x=1 (written first)"
    print("lamport ok")
