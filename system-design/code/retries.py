"""A retry storm. A service that can handle 100 requests per second is offered 90. A blip makes it fail for one second.
Naive clients retry at once, three times, so the offered load becomes 360 and the service stays overloaded.
Backoff with jitter and a retry budget lets it recover. Run: python3 retries.py"""
import random


def simulate(policy, seconds=30, base_load=90, capacity=100, seed=1):
    """Each second, new requests arrive and last second's failed requests come back as retries.
    Naive clients retry each failed original request 3 times. Budgeted clients add at most 10% of the base load."""
    rng = random.Random(seed)
    retries = 0
    overloaded_seconds = 0
    outage = {5}                                # one second when the service errors for everyone
    peak_offered = 0
    for t in range(seconds):
        offered = base_load + retries
        peak_offered = max(peak_offered, offered)
        failed = offered if t in outage else max(0, offered - capacity)
        if failed and t not in outage:
            overloaded_seconds += 1
        originals_failed = min(failed, base_load)
        if policy == "naive":
            retries = 3 * originals_failed
        else:
            budget = base_load // 10
            retries = int(min(originals_failed, budget) * rng.uniform(0.5, 1.0))
    return peak_offered, overloaded_seconds


if __name__ == "__main__":
    n_peak, n_over = simulate("naive")
    s_peak, s_over = simulate("budget")
    print(f"naive retries: peak offered load {n_peak}/s, {n_over} overloaded seconds; backoff + jitter + budget: peak {s_peak}/s, {s_over} overloaded seconds")
    assert n_peak == 360 and n_over > 20
    assert s_peak <= 100 and s_over == 0
    print("retries ok")
