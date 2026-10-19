"""A staged rollout that rolls back when the canary slice is worse than the baseline. Run: python3 canary.py"""
import random


def rollout(bad_version, stages=(0.01, 0.10, 0.50, 1.0), requests=20_000, seed=5, tolerance=0.01):
    rng = random.Random(seed)
    base_err = 0.002
    new_err = 0.08 if bad_version else 0.002
    exposed = 0.0
    for share in stages:
        errors_new = sum(rng.random() < new_err for _ in range(int(requests * share)))
        errors_old = sum(rng.random() < base_err for _ in range(int(requests * (1 - share)) or 1))
        rate_new = errors_new / max(int(requests * share), 1)
        rate_old = errors_old / max(int(requests * (1 - share)), 1)
        exposed = share
        if rate_new > rate_old + tolerance:
            return "rolled back", share
    return "completed", exposed


if __name__ == "__main__":
    bad = rollout(bad_version=True)
    good = rollout(bad_version=False)
    print(f"bad version: {bad[0]} while {bad[1]:.0%} of traffic was exposed; good version: {good[0]} at {good[1]:.0%}")
    assert bad == ("rolled back", 0.01) and good == ("completed", 1.0)
    print("canary ok")
