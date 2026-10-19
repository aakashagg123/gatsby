"""Transactional outbox vs a dual write. A crash between "update the database" and "publish the event"
loses the event with a dual write, and loses nothing with an outbox. Run: python3 outbox.py"""


class Db:
    def __init__(self):
        self.orders, self.outbox = [], []

    def commit(self, order, event=None):
        """One atomic transaction: the row and (optionally) the outbox record are stored together."""
        self.orders.append(order)
        if event is not None:
            self.outbox.append(event)


def dual_write(db, bus, order, crash):
    db.commit(order)
    if crash:
        return                                   # process dies before publishing
    bus.append(order)


def with_outbox(db, bus, order, crash):
    db.commit(order, event=order)                # the event is stored in the same transaction
    # a separate relay publishes unsent outbox records, so a crash here only delays publishing


def relay(db, bus):
    while db.outbox:
        bus.append(db.outbox.pop(0))


if __name__ == "__main__":
    db1, bus1 = Db(), []
    for i in range(10):
        dual_write(db1, bus1, i, crash=(i == 6))
    db2, bus2 = Db(), []
    for i in range(10):
        with_outbox(db2, bus2, i, crash=(i == 6))
        if i != 6:
            relay(db2, bus2)
    relay(db2, bus2)                             # the relay restarts and catches up
    print(f"dual write: {len(db1.orders)} orders stored, {len(bus1)} events published; outbox: {len(db2.orders)} stored, {len(bus2)} published")
    assert len(db1.orders) == 10 and len(bus1) == 9
    assert len(db2.orders) == 10 and sorted(bus2) == list(range(10))
    print("outbox ok")
