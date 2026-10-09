"""Lesson 5: one model, many scores. Which one matters depends on what each mistake costs.

Run: python3 lesson5_metrics.py
"""
from data import accuracy, make_customers, split, standardize
from lesson3_gradient_descent import predict, train_logistic

COST_MISSED_CHURNER = 60.0    # invented: margin lost when a customer we did not flag leaves
COST_WASTED_OFFER = 15.0      # invented: price of a retention offer sent to someone who would have stayed


def confusion(pred, truth):
    tp = sum(1 for p, t in zip(pred, truth) if p == 1 and t == 1)
    fp = sum(1 for p, t in zip(pred, truth) if p == 1 and t == 0)
    fn = sum(1 for p, t in zip(pred, truth) if p == 0 and t == 1)
    tn = sum(1 for p, t in zip(pred, truth) if p == 0 and t == 0)
    return tp, fp, fn, tn


def precision_recall(pred, truth):
    tp, fp, fn, _ = confusion(pred, truth)
    precision = tp / (tp + fp) if tp + fp else 0.0   # of the customers we flag, how many leave
    recall = tp / (tp + fn)                          # of the customers who leave, how many we flag
    return precision, recall


def auc(scores, truth):
    """Chance that a random churner scores higher than a random stayer. 0.5 is a coin flip."""
    pos = [s for s, t in zip(scores, truth) if t == 1]
    neg = [s for s, t in zip(scores, truth) if t == 0]
    wins = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return wins / (len(pos) * len(neg))


def total_cost(pred, truth):
    _, fp, fn, _ = confusion(pred, truth)
    return fn * COST_MISSED_CHURNER + fp * COST_WASTED_OFFER


def best_threshold(scores, truth):
    best = None
    for i in range(1, 100):
        t = i / 100
        c = total_cost([1 if s >= t else 0 for s in scores], truth)
        if best is None or c < best[1]:
            best = (t, c)
    return best


def capture_at_top(scores, truth, fraction):
    """If we can only contact the top `fraction` of customers by score, what share of churners is in it?"""
    order = sorted(range(len(scores)), key=lambda i: -scores[i])[: int(len(scores) * fraction)]
    return sum(truth[i] for i in order) / sum(truth)


def calibration_error(scores, truth, bins=10):
    """Average gap between what the model says (say 30%) and what happens (say 18%), by score band."""
    total = 0.0
    for b in range(bins):
        idx = [i for i, s in enumerate(scores) if b / bins <= s < (b + 1) / bins or (b == bins - 1 and s == 1.0)]
        if idx:
            said = sum(scores[i] for i in idx) / len(idx)
            seen = sum(truth[i] for i in idx) / len(idx)
            total += len(idx) / len(scores) * abs(said - seen)
    return total


def main():
    rows, labels = make_customers(8000)
    tr_x, tr_y, te_x, te_y = split(rows, labels, test_fraction=0.5)
    tr_x, te_x = standardize(tr_x, [te_x])
    w, b, _ = train_logistic(tr_x, tr_y)
    scores = predict(w, b, te_x)

    out = {"base_rate": sum(te_y) / len(te_y)}
    nobody = [0] * len(te_y)
    out["acc_nobody"] = accuracy(nobody, te_y)
    half = [1 if s >= 0.5 else 0 for s in scores]
    out["acc_half"] = accuracy(half, te_y)
    out["confusion_half"] = confusion(half, te_y)
    out["pr_half"] = precision_recall(half, te_y)
    out["auc"] = auc(scores, te_y)
    t, c = best_threshold(scores, te_y)
    chosen = [1 if s >= t else 0 for s in scores]
    out.update(threshold=t, cost_best=c, cost_half=total_cost(half, te_y), cost_nobody=total_cost(nobody, te_y),
               pr_best=precision_recall(chosen, te_y), confusion_best=confusion(chosen, te_y))
    out["capture_top10"] = capture_at_top(scores, te_y, 0.10)
    # Same ranking, wrong probabilities: square every score. AUC cannot tell. Calibration can.
    squashed = [s ** 2 for s in scores]
    out.update(auc_squashed=auc(squashed, te_y), cal=calibration_error(scores, te_y),
               cal_squashed=calibration_error(squashed, te_y))
    return out


if __name__ == "__main__":
    r = main()
    for k, v in r.items():
        print(k, v if not isinstance(v, float) else round(v, 3))
    assert r["acc_nobody"] > 0.8 and abs(r["acc_nobody"] - r["acc_half"]) < 0.04     # accuracy barely moves
    assert r["cost_best"] < r["cost_half"] < r["cost_nobody"]
    assert 0.5 < r["auc"] < 1.0
    assert abs(r["auc"] - r["auc_squashed"]) < 1e-9 and r["cal_squashed"] > 3 * r["cal"]
    assert r["capture_top10"] > 0.10
    print("lesson 5 ok")
