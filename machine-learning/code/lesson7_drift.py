"""Lesson 7: what breaks after launch. Skew (training and serving disagree) and drift (the world moves).

Run: python3 lesson7_drift.py
"""
import math

from data import make_customers, standardize
from lesson3_gradient_descent import predict, train_logistic
from lesson5_metrics import auc

N_BINS = 10


def psi(expected, actual, bins=N_BINS):
    """Population stability index: how far has a column's spread moved from what we trained on?

    Cut the training values into equal-sized bands. Count the share of live values in each band.
    A share that matches the training share contributes zero. Many teams treat 0.1 as 'look' and
    0.25 as 'act'. That is a habit from credit-risk work, not a standard.
    """
    ordered = sorted(expected)
    edges = [ordered[int(len(ordered) * i / bins)] for i in range(1, bins)]

    def shares(values):
        counts = [0] * bins
        for v in values:
            counts[sum(1 for e in edges if v > e)] += 1
        return [max(c / len(values), 1e-4) for c in counts]

    e, a = shares(expected), shares(actual)
    return sum((ai - ei) * math.log(ai / ei) for ei, ai in zip(e, a))


def skew_demo():
    rows, labels = make_customers(6000, seed=11)
    cut = 3000
    tr_x, tr_y = rows[:cut], labels[:cut]
    mean = [sum(c) / len(c) for c in zip(*tr_x)]                     # the model's view of "normal"
    s_tr, = standardize(tr_x)
    w, b, _ = train_logistic(s_tr, tr_y)

    def score(rs):
        sd = [math.sqrt(sum((v - m) ** 2 for v in c) / len(c)) or 1.0 for c, m in zip(zip(*tr_x), mean)]
        return predict(w, b, [[(v - m) / s for v, m, s in zip(r, mean, sd)] for r in rs])

    good = score(rows[cut:])
    # The serving system sends tenure in DAYS. Nothing crashes. The numbers are just wrong.
    wrong_rows, _ = make_customers(6000, seed=11, tenure_scale=30)
    bad = score(wrong_rows[cut:])
    truth = labels[cut:]
    tenure_train = [r[0] for r in tr_x]
    return dict(auc_offline=auc(good, truth), auc_served=auc(bad, truth),
                psi_tenure=psi(tenure_train, [r[0] for r in wrong_rows[cut:]]),
                psi_tickets=psi([r[1] for r in tr_x], [r[1] for r in wrong_rows[cut:]]))


def drift_demo():
    """Six months after launch the customer base changes: newer customers, fewer logins, tickets matter less."""
    old_x, old_y = make_customers(4000, seed=21)
    s_old, = standardize(old_x)
    w, b, _ = train_logistic(s_old, old_y)
    mean = [sum(c) / len(c) for c in zip(*old_x)]
    sd = [math.sqrt(sum((v - m) ** 2 for v in c) / len(c)) for c, m in zip(zip(*old_x), mean)]

    def scale(rs):
        return [[(v - m) / s for v, m, s in zip(r, mean, sd)] for r in rs]

    months = []
    for month in range(6):
        d = month / 5
        rows, labels = make_customers(3000, seed=100 + month, tenure_mean=18 * (1 - 0.5 * d),
                                      login_mean=14 * (1 - 0.4 * d), ticket_weight=0.5 * (1 - 0.8 * d))
        months.append(dict(
            month=month, auc=auc(predict(w, b, scale(rows)), labels),
            psi_tenure=psi([r[0] for r in old_x], [r[0] for r in rows]),
            psi_logins=psi([r[2] for r in old_x], [r[2] for r in rows]),
            rows=rows, labels=labels))
    # Retrain on the newest data and score on a fresh sample from the same period.
    new_x, new_y = months[-1]["rows"], months[-1]["labels"]
    s_new, = standardize(new_x)
    w2, b2, _ = train_logistic(s_new, new_y)
    mean2 = [sum(c) / len(c) for c in zip(*new_x)]
    sd2 = [math.sqrt(sum((v - m) ** 2 for v in c) / len(c)) for c, m in zip(zip(*new_x), mean2)]
    fresh_x, fresh_y = make_customers(3000, seed=999, tenure_mean=9.0, login_mean=8.4, ticket_weight=0.1)
    stale = auc(predict(w, b, scale(fresh_x)), fresh_y)
    fixed = auc(predict(w2, b2, [[(v - m) / s for v, m, s in zip(r, mean2, sd2)] for r in fresh_x]), fresh_y)
    return months, stale, fixed


if __name__ == "__main__":
    s = skew_demo()
    print(f"skew: AUC offline {s['auc_offline']:.3f}, served with the wrong unit {s['auc_served']:.3f}")
    print(f"      PSI tenure {s['psi_tenure']:.2f}, PSI tickets {s['psi_tickets']:.2f}")
    months, stale, fixed = drift_demo()
    print("month  AUC    PSI tenure  PSI logins")
    for m in months:
        print(f"{m['month']:5d}  {m['auc']:.3f}  {m['psi_tenure']:.2f}        {m['psi_logins']:.2f}")
    print(f"after drift: old model AUC {stale:.3f}, retrained model AUC {fixed:.3f}")
    assert s["auc_served"] < s["auc_offline"] - 0.1 and s["psi_tenure"] > 0.25 and s["psi_tickets"] < 0.1
    assert months[0]["psi_tenure"] < 0.1 and months[-1]["psi_tenure"] > 0.25
    assert months[-1]["auc"] < months[0]["auc"] - 0.05
    assert fixed > stale
    print("lesson 7 ok")
