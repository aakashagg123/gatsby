"""Cache stampede: a hot key expires and many requests hit the database. Run: python3 stampede.py"""
import random


def simulate(requests_at_expiry=1000, coalesce=False, ttl_jitter=0.0, keys=1, seed=1):
    """Return database reads caused by one synchronized expiry of `keys` hot keys."""
    rng = random.Random(seed)
    db_reads = 0
    for _ in range(keys):
        in_flight = False
        for _ in range(requests_at_expiry):
            if coalesce and in_flight:
                continue                            # wait for the single refill already running
            db_reads += 1
            in_flight = True
    return db_reads


def expiry_spread(keys, ttl, jitter, seed=1):
    """Largest number of keys that expire in the same second. Jitter spreads them."""
    rng = random.Random(seed)
    slots = {}
    for _ in range(keys):
        t = int(ttl * (1 + rng.uniform(0, jitter)))
        slots[t] = slots.get(t, 0) + 1
    return max(slots.values())


if __name__ == "__main__":
    naive = simulate(1000)
    merged = simulate(1000, coalesce=True)
    same, spread = expiry_spread(5000, 600, 0.0), expiry_spread(5000, 600, 0.2)
    print(f"1,000 requests at expiry of one hot key: {naive} database reads naive, {merged} with request coalescing")
    print(f"5,000 keys with TTL 600 s: {same} expire in the same second without jitter, {spread} with 20% jitter")
    assert naive == 1000 and merged == 1
    assert same == 5000 and spread < 100
    print("stampede ok")
