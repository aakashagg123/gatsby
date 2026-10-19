"""Chat: per-conversation sequence numbers, retry-safe sends and catch-up after being offline. Run: python3 chat_sync.py"""


class Conversation:
    def __init__(self):
        self.log = []              # (seq, client_msg_id, text); the seq is the position in the log
        self.seen = {}             # client_msg_id -> seq, so a retried send is not stored twice

    def send(self, client_msg_id, text):
        if client_msg_id in self.seen:
            return self.seen[client_msg_id]
        seq = len(self.log) + 1
        self.log.append((seq, client_msg_id, text))
        self.seen[client_msg_id] = seq
        return seq

    def since(self, last_seq):
        return [m for m in self.log if m[0] > last_seq]


if __name__ == "__main__":
    c = Conversation()
    a = c.send("m-1", "hi")
    retry = c.send("m-1", "hi")                  # the ack was lost, so the client sent it again
    c.send("m-2", "are you there?")
    c.send("m-3", "call me")
    phone_last_seen = 1                          # the phone was offline after message 1
    missed = c.since(phone_last_seen)
    print(f"retry returned seq {retry} and stored {len(c.log)} messages; the phone missed {[m[2] for m in missed]}")
    assert a == retry == 1 and len(c.log) == 3
    assert [m[0] for m in missed] == [2, 3]
    print("chat sync ok")
