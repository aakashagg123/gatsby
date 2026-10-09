"""Lesson 2: two leaks that make a test score look better than the real world will.

Leak 1: a column that is only known AFTER the outcome (retention_offer_sent).
Leak 2: the same customer sits in both the training rows and the test rows.

Run: python3 lesson2_leakage.py
"""
import random

from data import FEATURES, make_customers, split
from lesson1_rules_vs_learning import apply_stump, balanced_accuracy, learn_stump


def leaky_feature_demo():
    rows, labels = make_customers(6000, leak=True)
    tr_x, tr_y, te_x, te_y = split(rows, labels)
    rule = learn_stump(tr_x, tr_y)
    in_test = balanced_accuracy(apply_stump(rule, te_x), te_y)
    # On the day we need a prediction, nobody has been sent a retention offer yet.
    live_x = [r[:-1] + [0] for r in te_x]
    in_production = balanced_accuracy(apply_stump(rule, live_x), te_y)
    names = FEATURES + ["retention_offer_sent"]
    return names[rule[0]], in_test, in_production


def nearest_neighbour(train_x, train_y, x):
    """1-nearest-neighbour: copy the label of the single most similar training row."""
    best, label = None, None
    for r, y in zip(train_x, train_y):
        d = sum((a - b) ** 2 for a, b in zip(r, x))
        if best is None or d < best:
            best, label = d, y
    return label


def make_monthly_snapshots(n_customers=300, months=6, seed=3):
    """Each customer appears in several rows (one per month). Their rows look alike."""
    rng = random.Random(seed)
    rows, labels, owner = [], [], []
    for c in range(n_customers):
        base = [rng.uniform(0, 70), rng.uniform(0, 8), rng.uniform(0, 30), rng.uniform(15, 110)]
        # An unpredictable personal quirk: the label is not a function of the visible columns.
        churn = 1 if rng.random() < 0.25 else 0
        for _ in range(months):
            rows.append([v + rng.gauss(0, 0.4) for v in base])
            labels.append(churn)
            owner.append(c)
    return rows, labels, owner


def duplicate_customer_demo():
    rows, labels, owner = make_monthly_snapshots()
    rng = random.Random(1)
    idx = list(range(len(rows)))
    rng.shuffle(idx)
    cut = int(len(idx) * 0.75)

    def score(train_idx, test_idx):
        tx, ty = [rows[i] for i in train_idx], [labels[i] for i in train_idx]
        hits = sum(nearest_neighbour(tx, ty, rows[i]) == labels[i] for i in test_idx)
        return hits / len(test_idx)

    random_split = score(idx[:cut], idx[cut:])
    # Split by customer: every row of a customer goes to the same side.
    customers = sorted(set(owner))
    rng.shuffle(customers)
    held_out = set(customers[: len(customers) // 4])
    by_customer = score([i for i in idx if owner[i] not in held_out],
                        [i for i in idx if owner[i] in held_out])
    return random_split, by_customer


if __name__ == "__main__":
    feature, in_test, in_production = leaky_feature_demo()
    print(f"best single feature found: {feature}")
    print(f"balanced accuracy in testing    {in_test:.3f}")
    print(f"balanced accuracy in production {in_production:.3f}")
    random_split, by_customer = duplicate_customer_demo()
    print(f"1-NN accuracy, random row split  {random_split:.3f}")
    print(f"1-NN accuracy, split by customer {by_customer:.3f}")
    assert feature == "retention_offer_sent"
    assert in_test > 0.9 and in_production == 0.5
    assert random_split > 0.95 and by_customer < 0.8
    print("lesson 2 ok")
