"""Double-entry ledger: every transfer posts equal debits and credits, and balances are derived. Run: python3 ledger.py"""


class Ledger:
    def __init__(self):
        self.entries = []          # (txn_id, account, amount_in_cents); credits positive, debits negative
        self.seen = set()

    def post(self, txn_id, lines):
        if txn_id in self.seen:                      # idempotent: a retry changes nothing
            return False
        if sum(a for _, a in lines) != 0:
            raise ValueError("debits and credits must balance")
        for account, amount in lines:
            self.entries.append((txn_id, account, amount))
        self.seen.add(txn_id)
        return True

    def balance(self, account):
        return sum(a for _, acc, a in self.entries if acc == account)


if __name__ == "__main__":
    l = Ledger()
    l.post("t1", [("card", -2000), ("merchant", 1940), ("fees", 60)])
    again = l.post("t1", [("card", -2000), ("merchant", 1940), ("fees", 60)])
    try:
        l.post("t2", [("card", -100), ("merchant", 90)])
        unbalanced = False
    except ValueError:
        unbalanced = True
    total = sum(a for _, _, a in l.entries)
    print(f"balances in cents: merchant {l.balance('merchant')}, fees {l.balance('fees')}, card {l.balance('card')}; sum of all entries {total}")
    print(f"retry of t1 posted again: {again}; unbalanced entry rejected: {unbalanced}")
    assert not again and unbalanced and total == 0 and l.balance("merchant") == 1940
    print("ledger ok")
