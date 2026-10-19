"""Nearby search with a grid index: look in the rider's cell and its neighbours, not at every driver.
A plain square grid stands in for geohash, S2 or H3. Run: python3 geo_grid.py"""
import math
import random

CELL = 0.01   # degrees, about 1.1 km


def cell(lat, lon):
    return (math.floor(lat / CELL), math.floor(lon / CELL))


def build(drivers):
    index = {}
    for d, (lat, lon) in drivers.items():
        index.setdefault(cell(lat, lon), []).append(d)
    return index


def near(index, lat, lon, ring=1):
    cx, cy = cell(lat, lon)
    found, scanned = [], 0
    for dx in range(-ring, ring + 1):
        for dy in range(-ring, ring + 1):
            for d in index.get((cx + dx, cy + dy), []):
                found.append(d)
    return found


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


if __name__ == "__main__":
    rng = random.Random(3)
    drivers = {i: (37.0 + rng.random() * 0.5, -122.5 + rng.random() * 0.5) for i in range(50_000)}
    index = build(drivers)
    rider = (37.25, -122.25)
    cands = near(index, *rider, ring=1)
    truth = {d for d, p in drivers.items() if dist(p, rider) <= CELL}
    missed = truth - set(cands)
    print(f"{len(drivers):,} drivers; the grid looked at {len(cands)} candidates instead of all of them")
    print(f"drivers within one cell width: {len(truth)}; missed by the 3x3 search: {len(missed)}")
    assert len(cands) < len(drivers) / 100 and not missed
    print("geo grid ok")
