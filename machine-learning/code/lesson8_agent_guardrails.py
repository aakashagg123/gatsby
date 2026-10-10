"""Lesson 8: controls you give a coding agent that runs ML experiments for you.

An agent that can run code and chase a score will find shortcuts. The two that matter most are
tuning on the test rows and using a column that leaks the answer. This file builds the checks
that make both loud, and measures how much the first one inflates a score.

  1. A ledger that lets the test rows be scored once, and logs every evaluation.
  2. A sweep that shows how much a score is overstated when the test rows pick the winner.
  3. A leak audit: a single column that predicts the label almost perfectly is a leak
     until proven otherwise, and a customer on both sides of a split is a leak.

Run: python3 lesson8_agent_guardrails.py
"""
import itertools
import random

from data import FEATURES, make_customers
from lesson1_rules_vs_learning import balanced_accuracy
from tree import grow, proba


class TestSetReused(Exception):
    """Raised when something asks to score the protected split a second time."""


class Ledger:
    """Holds the splits, scores them, and writes down every evaluation.

    The log is the evidence an agent must show you: which split, which score, which note.
    The protected split can be scored once. A second request raises, so a tuning loop that
    reads the test score stops on its first step.
    """

    def __init__(self, splits, protected="test"):
        self.splits = splits
        self.protected = protected
        self.log = []

    def count(self, split):
        return sum(1 for entry in self.log if entry[0] == split)

    def score(self, split, predict, note=""):
        if split == self.protected and self.count(split) >= 1:
            raise TestSetReused(f"the {split} rows were already scored once: {self.log[-1]}")
        rows, labels = self.splits[split]
        value = balanced_accuracy(predict(rows), labels)
        self.log.append((split, round(value, 4), note))
        return value


def tree_predictor(rows, labels, depth, min_leaf):
    tree = grow(rows, labels, depth, min_leaf=min_leaf)
    cut = sum(labels) / len(labels)
    return lambda xs: [1 if proba(tree, x) >= cut else 0 for x in xs]


CONFIGS = list(itertools.product(range(1, 13), (1, 5, 20)))      # 36 settings an agent might try


def make_splits(seed):
    rows, labels = make_customers(6000, seed=seed)
    return {"train": (rows[:800], labels[:800]), "valid": (rows[800:2000], labels[800:2000]),
            "test": (rows[2000:2400], labels[2000:2400]), "fresh": (rows[2400:], labels[2400:])}


def sweep(splits):
    """Score every setting on validation, test and fresh rows. Returns one tuple per setting."""
    tr = splits["train"]
    out = []
    for depth, min_leaf in CONFIGS:
        predict = tree_predictor(tr[0], tr[1], depth, min_leaf)
        out.append(tuple(balanced_accuracy(predict(splits[s][0]), splits[s][1])
                         for s in ("valid", "test", "fresh")))
    return out


def optimism(repeats=30, tries=(1, 6, 36)):
    """Average over many repeats: how much does choosing on a split overstate the score?

    For each repeat the sweep scores 36 settings. A tuner that tries k settings keeps the best.
    'fresh' rows were never used to choose, so they show what the chosen setting really does.
    """
    gap_test = {k: [] for k in tries}
    gap_valid = []
    for r in range(repeats):
        results = sweep(make_splits(100 + r))
        order = list(range(len(CONFIGS)))
        random.Random(r).shuffle(order)
        for k in tries:
            pool = [results[i] for i in order[:k]]
            best = max(pool, key=lambda t: t[1])                   # chosen by the test rows
            gap_test[k].append(best[1] - best[2])                  # reported minus fresh
        best = max(results, key=lambda t: t[0])                    # chosen by the validation rows
        gap_valid.append(best[1] - best[2])
    mean = lambda xs: sum(xs) / len(xs)
    return {k: mean(v) for k, v in gap_test.items()}, mean(gap_valid), sum(1 for g in gap_test[tries[-1]] if g > 0)


def column_strength(rows, labels):
    """Best balanced accuracy a single yes-or-no cut on each column can reach."""
    out = []
    for column in zip(*rows):
        values = sorted(set(column))
        step = max(1, len(values) // 40)
        best = 0.0
        for cut in values[::step]:
            for sign in (1, -1):
                pred = [1 if sign * (v - cut) >= 0 else 0 for v in column]
                best = max(best, balanced_accuracy(pred, labels))
        out.append(best)
    return out


def leak_audit(rows, labels, names, limit=0.90):
    """Names of columns that predict the label better than `limit` on their own."""
    return [n for n, s in zip(names, column_strength(rows, labels)) if s > limit]


def shared_ids(train_ids, test_ids):
    return sorted(set(train_ids) & set(test_ids))


def main():
    splits = make_splits(100)

    # 1. The disciplined loop: choose on validation, score the test rows once.
    ledger = Ledger(splits)
    tr = splits["train"]
    best = max(CONFIGS, key=lambda c: ledger.score("valid", tree_predictor(tr[0], tr[1], *c), f"depth={c[0]} leaf={c[1]}"))
    final = ledger.score("test", tree_predictor(tr[0], tr[1], *best), f"final, depth={best[0]} leaf={best[1]}")

    # 2. The shortcut: pick the setting by its test score. The ledger stops it at step two.
    shortcut = Ledger(make_splits(100))
    stopped_at = None
    try:
        for step, c in enumerate(CONFIGS, 1):
            shortcut.score("test", tree_predictor(tr[0], tr[1], *c), f"depth={c[0]} leaf={c[1]}")
    except TestSetReused:
        stopped_at = step

    gap_by_tries, gap_valid, wins = optimism()

    # 3. The leak audit on clean data, on leaky data, and on a split that shares customers.
    clean_rows, clean_labels = make_customers(3000)
    leaky_rows, leaky_labels = make_customers(3000, leak=True)
    names = FEATURES + ["retention_offer_sent"]
    flagged_clean = leak_audit(clean_rows, clean_labels, FEATURES)
    flagged_leaky = leak_audit(leaky_rows, leaky_labels, names)
    strengths = dict(zip(names, column_strength(leaky_rows, leaky_labels)))
    overlap = shared_ids([1, 2, 3, 4, 5], [5, 6, 7])
    return dict(best=best, final=final, ledger=ledger, stopped_at=stopped_at, gap_by_tries=gap_by_tries,
                gap_valid=gap_valid, wins=wins, flagged_clean=flagged_clean, flagged_leaky=flagged_leaky,
                strengths=strengths, overlap=overlap)


if __name__ == "__main__":
    r = main()
    print(f"disciplined loop: best setting {r['best']}, test score {r['final']:.3f}")
    print(f"  evaluations logged: valid {r['ledger'].count('valid')}, test {r['ledger'].count('test')}")
    print(f"shortcut loop: the ledger stopped it at step {r['stopped_at']} of {len(CONFIGS)}")
    print("average overstatement when the test rows choose the setting (reported minus fresh rows):")
    for k, g in r["gap_by_tries"].items():
        print(f"  {k:2d} settings tried: {g * 100:+.1f} points")
    print(f"  chosen on validation instead: {r['gap_valid'] * 100:+.1f} points")
    print(f"  test-chosen score beat the fresh rows in {r['wins']} of 30 repeats")
    print("single-column strength with the leaky column added:",
          {k: round(v, 3) for k, v in r["strengths"].items()})
    print("flagged on clean data:", r["flagged_clean"], "| flagged on leaky data:", r["flagged_leaky"])
    print("customers on both sides of a split:", r["overlap"])
    assert r["ledger"].count("test") == 1 and r["ledger"].count("valid") == len(CONFIGS)
    assert r["stopped_at"] == 2                                    # the second test score raises
    g = r["gap_by_tries"]
    assert g[36] > 0.015                                           # tuning on test overstates the score
    assert abs(r["gap_valid"]) < 0.015                             # tuning on validation does not
    assert g[36] > g[6] > g[1] - 0.005                             # more tries, more overstatement
    assert r["wins"] >= 20
    assert r["flagged_clean"] == [] and r["flagged_leaky"] == ["retention_offer_sent"]
    assert r["strengths"]["retention_offer_sent"] > 0.9
    assert r["overlap"] == [5]
    print("lesson 8 ok")
