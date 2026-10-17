"""Lesson 1: when an agent writes the code, the bottleneck moves to specifying and verifying.

All times are invented minutes for one task. Run: python3 lesson1_bottleneck.py
"""


def human_time(spec=20, code=240, review=30):
    return spec + code + review


def agent_time(spec=40, run=10, review=60, p_fail=0.3, respec=15):
    """Expected minutes per accepted task. Each attempt runs the agent and then a review. A failed attempt
    costs a re-specification and another attempt. Attempts are independent with failure chance p_fail."""
    attempts = 1 / (1 - p_fail)
    return spec + (run + review) * attempts + respec * (attempts - 1)


def main():
    base = human_time()
    cases = {
        "agent, weak checks": agent_time(),
        "agent, strong checks": agent_time(review=25, p_fail=0.15),
        "agent runs instantly, weak checks": agent_time(run=0),
        "agent runs instantly, strong checks": agent_time(run=0, review=25, p_fail=0.15),
    }
    return dict(base=base, cases=cases, speedup={k: base / v for k, v in cases.items()})


if __name__ == "__main__":
    r = main()
    print(f"one task by hand: {r['base']} minutes (20 to specify, 240 to code, 30 to review)")
    for k, v in r["cases"].items():
        print(f"  {k:38s} {v:6.1f} minutes  ({r['speedup'][k]:.2f}x faster)")
    s = r["speedup"]
    assert 1.9 < s["agent, weak checks"] < 2.1                                    # about 2x with weak checks
    assert 3.3 < s["agent, strong checks"] < 3.6                                  # about 3.5x with strong checks
    assert s["agent runs instantly, weak checks"] < 2.4                           # a free agent barely helps without checks
    assert s["agent, strong checks"] > 1.4 * s["agent, weak checks"]              # verification beats raw agent speed
    print("lesson 1 ok")
