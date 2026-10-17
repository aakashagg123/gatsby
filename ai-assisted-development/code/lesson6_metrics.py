"""Lesson 6: a headline productivity number can point the wrong way. Mix shifts hide the truth.

The pull-request data is invented. Run: python3 lesson6_metrics.py
"""

# (difficulty, group, pull requests, mean cycle hours, share needing rework within 30 days)
DATA = [
    ("easy", "before", 100, 6.0, 0.05),
    ("easy", "agent", 300, 3.0, 0.08),
    ("hard", "before", 100, 40.0, 0.10),
    ("hard", "agent", 50, 32.0, 0.20),
]


def summarize(rows):
    n = sum(r[2] for r in rows)
    return dict(prs=n, cycle=sum(r[2] * r[3] for r in rows) / n, rework=sum(r[2] * r[4] for r in rows) / n)


def by_group(group):
    return summarize([r for r in DATA if r[1] == group])


def by_stratum(difficulty, group):
    return summarize([r for r in DATA if r[0] == difficulty and r[1] == group])


def main():
    return dict(before=by_group("before"), agent=by_group("agent"),
                strata={(d, g): by_stratum(d, g) for d in ("easy", "hard") for g in ("before", "agent")})


if __name__ == "__main__":
    r = main()
    b, a = r["before"], r["agent"]
    print(f"headline: cycle time {b['cycle']:.1f} h -> {a['cycle']:.1f} h ({b['cycle'] / a['cycle']:.1f}x faster), "
          f"rework {b['rework']:.1%} -> {a['rework']:.1%}, PRs {b['prs']} -> {a['prs']}")
    for d in ("easy", "hard"):
        sb, sa = r["strata"][(d, "before")], r["strata"][(d, "agent")]
        print(f"  {d:5s} cycle {sb['cycle']:5.1f} h -> {sa['cycle']:5.1f} h, rework {sb['rework']:.0%} -> {sa['rework']:.0%}")
    # the headline gain is mostly a change in the mix of work, not speed
    easy_share_b = by_stratum("easy", "before")["prs"] / b["prs"]
    easy_share_a = by_stratum("easy", "agent")["prs"] / a["prs"]
    print(f"easy share of PRs: {easy_share_b:.0%} -> {easy_share_a:.0%}")
    # throughput and rework-adjusted output
    clean_b = b["prs"] * (1 - b["rework"])
    clean_a = a["prs"] * (1 - a["rework"])
    print(f"PRs that needed no rework: {clean_b:.0f} -> {clean_a:.0f}")
    hard_b, hard_a = r["strata"][("hard", "before")], r["strata"][("hard", "agent")]
    assert b["cycle"] / a["cycle"] > 3                                   # a big headline win
    assert hard_a["cycle"] / hard_b["cycle"] > 0.75                      # but hard work improved by under 25%
    assert hard_a["rework"] == 2 * hard_b["rework"]                      # and its rework doubled
    assert easy_share_a > easy_share_b + 0.3                             # the mix moved toward easy work
    assert a["rework"] > b["rework"]                                     # blended rework rose too
    print("lesson 6 ok")
