"""Delivery routing: the vehicle routing problem is NP-hard, so real systems use heuristics. A nearest-neighbour tour is quick
and rough, and a 2-opt pass improves it. Run: python3 vrp.py"""
import math
import random


def length(points, tour):
    return sum(math.dist(points[tour[i]], points[tour[(i + 1) % len(tour)]]) for i in range(len(tour)))


def nearest_neighbour(points):
    left, tour = set(range(1, len(points))), [0]
    while left:
        nxt = min(left, key=lambda j: math.dist(points[tour[-1]], points[j]))
        tour.append(nxt)
        left.remove(nxt)
    return tour


def two_opt(points, tour):
    best = tour[:]
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best) - 1):
            for j in range(i + 1, len(best)):
                cand = best[:i] + best[i:j + 1][::-1] + best[j + 1:]
                if length(points, cand) < length(points, best) - 1e-9:
                    best, improved = cand, True
    return best


if __name__ == "__main__":
    rng = random.Random(8)
    pts = [(rng.random() * 20, rng.random() * 20) for _ in range(40)]       # 40 stops in a 20 km square, depot is stop 0
    nn = nearest_neighbour(pts)
    opt = two_opt(pts, nn)
    ln, lo = length(pts, nn), length(pts, opt)
    print(f"40 stops: nearest-neighbour tour {ln:.1f} km, after 2-opt {lo:.1f} km ({1 - lo / ln:.0%} shorter)")
    assert sorted(opt) == list(range(40)) and lo < ln
    print("vrp ok")
