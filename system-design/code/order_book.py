"""A tiny limit order book with price-time priority. Run: python3 order_book.py"""
import heapq
from itertools import count


class Book:
    def __init__(self):
        self.bids, self.asks, self.seq = [], [], count()   # bids: (-price, seq, qty); asks: (price, seq, qty)

    def submit(self, side, price, qty):
        fills = []
        if side == "buy":
            while qty and self.asks and self.asks[0][0] <= price:
                p, s, q = heapq.heappop(self.asks)
                take = min(q, qty)
                fills.append((p, take))
                qty -= take
                if q > take:
                    heapq.heappush(self.asks, (p, s, q - take))      # keeps its place in the queue
            if qty:
                heapq.heappush(self.bids, (-price, next(self.seq), qty))
        else:
            while qty and self.bids and -self.bids[0][0] >= price:
                p, s, q = heapq.heappop(self.bids)
                take = min(q, qty)
                fills.append((-p, take))
                qty -= take
                if q > take:
                    heapq.heappush(self.bids, (p, s, q - take))
            if qty:
                heapq.heappush(self.asks, (price, next(self.seq), qty))
        return fills


if __name__ == "__main__":
    b = Book()
    b.submit("sell", 101, 50)
    b.submit("sell", 100, 30)
    b.submit("sell", 100, 20)                      # same price, arrives later
    fills = b.submit("buy", 101, 60)
    print("buy 60 at limit 101 fills:", fills)
    assert fills == [(100, 30), (100, 20), (101, 10)]
    rest = b.submit("buy", 99, 10)
    assert rest == [] and b.bids[0][2] == 10 and b.asks[0][0] == 101
    print("order book ok")
