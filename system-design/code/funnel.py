"""A recommendation funnel: cheap retrieval narrows a big catalogue so an expensive ranker scores only a few
hundred items. Run: python3 funnel.py"""
import math
import random

DIM = 16


def vec(rng):
    v = [rng.gauss(0, 1) for _ in range(DIM)]
    n = math.sqrt(sum(x * x for x in v))
    return [x / n for x in v]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def build(n_items=20_000, seed=2):
    rng = random.Random(seed)
    return [vec(rng) for _ in range(n_items)], vec(rng)


def true_scores(items, user):
    """The 'heavy model': the real relevance, which also uses a nonlinear term the retrieval stage cannot see."""
    return [dot(it, user) + 0.2 * math.sin(5 * dot(it, user)) for it in items]


if __name__ == "__main__":
    items, user = build()
    heavy = true_scores(items, user)
    best = set(sorted(range(len(items)), key=lambda i: -heavy[i])[:20])      # what the heavy model would show
    cheap = [dot(it, user) for it in items]                                  # retrieval: one dot product per item
    pool = sorted(range(len(items)), key=lambda i: -cheap[i])[:500]
    recall = len(best & set(pool)) / len(best)
    ranked = sorted(pool, key=lambda i: -heavy[i])[:20]                      # the heavy model scores only the pool
    got = len(best & set(ranked)) / len(best)
    cost_all, cost_funnel = len(items) * 100, len(items) * 1 + len(pool) * 100       # heavy model costs 100 units, retrieval 1
    print(f"retrieval pool of {len(pool)} from {len(items):,} items keeps {recall:.0%} of the heavy model's top 20; final top 20 matches {got:.0%}")
    print(f"cost: heavy model on everything {cost_all:,} units, funnel {cost_funnel:,} units ({cost_all / cost_funnel:.0f}x cheaper)")
    assert recall >= 0.9 and cost_all / cost_funnel > 20
    print("funnel ok")
