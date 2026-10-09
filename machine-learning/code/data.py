"""Invented data for the Machine learning module.

One made-up product runs through every lesson: a subscription service that wants to predict
which customers will cancel in the next 30 days. The data is generated with a fixed seed, so
every number in the lessons can be reproduced. Nothing here is real customer data.
"""
import math
import random

FEATURES = ["tenure_months", "tickets_90d", "logins_30d", "monthly_spend"]


def _sigmoid(z):
    return 1.0 / (1.0 + math.exp(-z))


def make_customers(n, seed=7, leak=False, tenure_scale=1.0, tenure_mean=18.0, login_mean=14.0,
                   ticket_weight=0.50):
    """Return (rows, labels). A row is [tenure_months, tickets_90d, logins_30d, monthly_spend].

    Churn is more likely for new customers, customers with many support tickets, and customers
    who rarely log in. Real churn is noisy, so the label is drawn at random from that
    probability: no model can be perfect.

    leak=True appends a fifth column, `retention_offer_sent`. In a real company that offer goes
    out AFTER a customer asks to cancel. It looks like a strong signal in the history and is
    useless on the day you need a prediction. This is the classic leak.

    tenure_scale multiplies tenure. It lets lesson 7 simulate a unit mismatch between training
    and serving (months versus days, scale of about 30). tenure_mean, login_mean and
    ticket_weight let lesson 7 simulate a customer base that changes over time.
    """
    rng = random.Random(seed)
    rows, labels = [], []
    for _ in range(n):
        tenure = min(72, int(rng.expovariate(1 / tenure_mean)) + 1)
        tickets = min(9, int(rng.expovariate(1 / 1.4)))
        logins = max(0, int(rng.gauss(login_mean, 8)))
        spend = round(rng.uniform(15, 110), 2)
        z = -1.1 + ticket_weight * tickets - 0.045 * tenure - 0.045 * logins + 0.004 * spend
        churn = 1 if rng.random() < _sigmoid(z) else 0
        row = [tenure * tenure_scale, tickets, logins, spend]
        if leak:
            offer = 1 if (churn and rng.random() < 0.96) or (not churn and rng.random() < 0.02) else 0
            row.append(offer)
        rows.append(row)
        labels.append(churn)
    return rows, labels


def split(rows, labels, test_fraction=0.25, seed=1):
    """A random train/test split. Returns (train_rows, train_labels, test_rows, test_labels)."""
    rng = random.Random(seed)
    idx = list(range(len(rows)))
    rng.shuffle(idx)
    cut = int(len(idx) * (1 - test_fraction))
    tr, te = idx[:cut], idx[cut:]
    return ([rows[i] for i in tr], [labels[i] for i in tr],
            [rows[i] for i in te], [labels[i] for i in te])


def accuracy(pred, truth):
    return sum(1 for p, t in zip(pred, truth) if p == t) / len(truth)


def standardize(train_rows, other_rows_list=()):
    """Scale each column to mean 0 and spread 1, using the TRAINING rows only.

    Returns the scaled training rows, then the scaled version of each other set. Using the
    test rows to compute the mean is a small leak (lesson 2), so we never do it.
    """
    cols = list(zip(*train_rows))
    mean = [sum(c) / len(c) for c in cols]
    sd = [math.sqrt(sum((v - m) ** 2 for v in c) / len(c)) or 1.0 for c, m in zip(cols, mean)]

    def apply(rows):
        return [[(v - m) / s for v, m, s in zip(r, mean, sd)] for r in rows]

    return (apply(train_rows),) + tuple(apply(r) for r in other_rows_list)
