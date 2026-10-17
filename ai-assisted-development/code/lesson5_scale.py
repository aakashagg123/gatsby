"""Lesson 5: running at scale. Context cost across a long session, and the arithmetic of fanning out.

Prices and token counts are invented for the arithmetic. Run: python3 lesson5_scale.py
"""

PRICE = 3.0         # dollars per million input tokens, invented
CACHE_READ = 0.1    # cached history is read at a tenth of the price, as for most Claude models


def session_cost(turns, base=20_000, per_turn=8_000, price=PRICE, cache_read=CACHE_READ):
    """Input cost of one session. Each turn reads the whole history, mostly from the cache, and adds new tokens."""
    total = 0.0
    history = base
    for _ in range(turns):
        total += (history * cache_read + per_turn) * price / 1e6
        history += per_turn
    return total


def long_vs_fresh(tasks=5, turns_per_task=20):
    one_long = session_cost(tasks * turns_per_task)
    fresh = tasks * session_cost(turns_per_task)
    return one_long, fresh


def fanout(tasks, p_success, max_attempts, cost_per_attempt, review_minutes):
    """Expected cost and review time for a batch run with retries. Failed tasks after the last attempt need a person."""
    done = 0.0
    attempts = 0.0
    p_fail_all = (1 - p_success) ** max_attempts
    for k in range(1, max_attempts + 1):
        reach = (1 - p_success) ** (k - 1)
        attempts += reach
        done += reach * p_success
    return dict(cost=tasks * attempts * cost_per_attempt, accepted=tasks * done,
                handoff=tasks * p_fail_all, review_hours=tasks * done * review_minutes / 60)


def main():
    one_long, fresh = long_vs_fresh()
    return dict(one_long=one_long, fresh=fresh, small=session_cost(20),
                batch=fanout(200, 0.7, 3, 1.5, 6), single=fanout(200, 0.7, 1, 1.5, 6))


if __name__ == "__main__":
    r = main()
    print(f"one 20-turn session: ${r['small']:.2f} of input; five unrelated tasks in one 100-turn session: ${r['one_long']:.2f}; in five fresh sessions: ${r['fresh']:.2f}")
    b, s = r["batch"], r["single"]
    print(f"200 tasks, 70% pass per attempt, $1.50 per attempt: one attempt -> ${s['cost']:.0f}, {s['accepted']:.0f} accepted, {s['handoff']:.0f} to a person; "
          f"up to 3 attempts -> ${b['cost']:.0f}, {b['accepted']:.0f} accepted, {b['handoff']:.0f} to a person")
    print(f"review time at 6 minutes per accepted task: {s['review_hours']:.0f} hours, then {b['review_hours']:.0f} hours")
    assert r["one_long"] > 2.5 * r["fresh"]                         # clearing between unrelated tasks cuts input cost
    assert b["accepted"] > s["accepted"] and b["cost"] > s["cost"]
    assert b["handoff"] < s["handoff"] / 5
    assert b["review_hours"] > s["review_hours"]                    # more accepted work is more review
    print("lesson 5 ok")
