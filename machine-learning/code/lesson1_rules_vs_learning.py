"""Lesson 1: a hand-written rule, a rule learned from data, and a do-nothing baseline.

Run: python3 lesson1_rules_vs_learning.py
"""
from data import FEATURES, make_customers, split


def balanced_accuracy(pred, truth):
    """Average of two rates: churners we catch, and stayers we leave alone.

    It stays honest when one class is rare. Plain accuracy does not (lesson 5).
    """
    pos = [p for p, t in zip(pred, truth) if t == 1]
    neg = [p for p, t in zip(pred, truth) if t == 0]
    return (sum(pos) / len(pos) + sum(1 for p in neg if p == 0) / len(neg)) / 2


def do_nothing(rows):
    return [0 for _ in rows]                      # predict that nobody churns


def hand_rule(rows):
    return [1 if r[1] >= 3 else 0 for r in rows]  # "3 or more tickets means trouble"


def learn_stump(rows, labels):
    """Learn a one-feature rule: try every feature, every cut point, both directions.

    This is machine learning in its smallest form. The program is the search. The rule is
    what it found.
    """
    best = (-1, None)
    for f in range(len(rows[0])):
        for cut in sorted({r[f] for r in rows}):
            for sign in (1, -1):
                pred = [1 if sign * (r[f] - cut) >= 0 else 0 for r in rows]
                score = balanced_accuracy(pred, labels)
                if score > best[0]:
                    best = (score, (f, cut, sign))
    return best[1]


def apply_stump(rule, rows):
    f, cut, sign = rule
    return [1 if sign * (r[f] - cut) >= 0 else 0 for r in rows]


def main():
    rows, labels = make_customers(4000)
    tr_x, tr_y, te_x, te_y = split(rows, labels)
    rule = learn_stump(tr_x, tr_y)
    scores = {
        "do nothing": balanced_accuracy(do_nothing(te_x), te_y),
        "hand-written rule": balanced_accuracy(hand_rule(te_x), te_y),
        "learned rule": balanced_accuracy(apply_stump(rule, te_x), te_y),
    }
    f, cut, sign = rule
    print(f"learned rule: {FEATURES[f]} {'>=' if sign == 1 else '<='} {cut}")
    for name, s in scores.items():
        print(f"{name:18s} balanced accuracy {s:.3f}")
    return scores, rule


if __name__ == "__main__":
    scores, rule = main()
    assert scores["do nothing"] == 0.5                        # a do-nothing rule is a coin flip
    assert scores["learned rule"] > scores["hand-written rule"] > scores["do nothing"]
    print("lesson 1 ok")
