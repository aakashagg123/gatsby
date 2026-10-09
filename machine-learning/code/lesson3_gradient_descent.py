"""Lesson 3: training is a loop. Measure the error, nudge every knob to reduce it, repeat.

Run: python3 lesson3_gradient_descent.py
"""
import math

from data import make_customers, split, standardize
from lesson1_rules_vs_learning import balanced_accuracy


def one_knob(start=0.0, target=3.0, lr=0.1, steps=5):
    """The smallest possible training run: one knob w, loss = (w - target)^2.

    The slope of the loss is 2 * (w - target). Each step moves w a little downhill.
    """
    w, path = start, [start]
    for _ in range(steps):
        slope = 2 * (w - target)
        w = w - lr * slope
        path.append(round(w, 4))
    return path


def sigmoid(z):
    return 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, z))))


def log_loss(weights, bias, rows, labels):
    """Average 'surprise' of the model. Lower is better. 0.693 is a coin flip."""
    total = 0.0
    for x, y in zip(rows, labels):
        p = min(max(sigmoid(sum(w * v for w, v in zip(weights, x)) + bias), 1e-9), 1 - 1e-9)
        total += -(y * math.log(p) + (1 - y) * math.log(1 - p))
    return total / len(rows)


def train_logistic(rows, labels, lr=0.5, epochs=150):
    """Logistic regression by full-batch gradient descent. Returns (weights, bias, loss_curve)."""
    n, d = len(rows), len(rows[0])
    weights, bias, curve = [0.0] * d, 0.0, []
    for _ in range(epochs):
        grad_w, grad_b = [0.0] * d, 0.0
        for x, y in zip(rows, labels):
            err = sigmoid(sum(w * v for w, v in zip(weights, x)) + bias) - y   # prediction minus truth
            for j in range(d):
                grad_w[j] += err * x[j]
            grad_b += err
        weights = [w - lr * g / n for w, g in zip(weights, grad_w)]           # step downhill
        bias -= lr * grad_b / n
        curve.append(log_loss(weights, bias, rows, labels))
    return weights, bias, curve


def predict(weights, bias, rows):
    return [sigmoid(sum(w * v for w, v in zip(weights, x)) + bias) for x in rows]


def main():
    rows, labels = make_customers(4000)
    tr_x, tr_y, te_x, te_y = split(rows, labels)
    tr_x, te_x = standardize(tr_x, [te_x])
    base_rate = sum(tr_y) / len(tr_y)
    baseline_loss = log_loss([0.0] * 4, math.log(base_rate / (1 - base_rate)), te_x, te_y)
    w, b, curve = train_logistic(tr_x, tr_y)
    test_loss = log_loss(w, b, te_x, te_y)
    cut = base_rate
    bal = balanced_accuracy([1 if p >= cut else 0 for p in predict(w, b, te_x)], te_y)
    _, _, slow = train_logistic(tr_x, tr_y, lr=0.01, epochs=150)
    _, _, wild = train_logistic(tr_x, tr_y, lr=60.0, epochs=20)
    return dict(path=one_knob(), curve=curve, baseline_loss=baseline_loss, test_loss=test_loss,
                balanced=bal, weights=w, slow=slow, wild=wild)


if __name__ == "__main__":
    r = main()
    print("one knob:", r["path"])
    print(f"loss at epoch 1 {r['curve'][0]:.3f}, epoch 10 {r['curve'][9]:.3f}, epoch 150 {r['curve'][-1]:.3f}")
    print(f"test loss {r['test_loss']:.3f} against {r['baseline_loss']:.3f} for 'always predict the average'")
    print(f"balanced accuracy at the base-rate cutoff {r['balanced']:.3f}")
    print(f"slow learning rate: loss after 150 epochs {r['slow'][-1]:.3f}")
    print(f"wild learning rate: first losses {[round(x, 2) for x in r['wild'][:6]]}, "
          f"range over {len(r['wild'])} epochs {min(r['wild']):.2f} to {max(r['wild']):.2f}")
    assert all(a >= b - 1e-12 for a, b in zip(r["curve"], r["curve"][1:]))   # loss only falls
    assert r["test_loss"] < r["baseline_loss"]
    assert r["slow"][-1] > r["curve"][-1]                                    # too small: still far behind
    assert max(r["wild"]) > r["wild"][0]                                     # too big: loss gets worse
    assert round(min(r["wild"]), 2) == 0.92 and round(max(r["wild"]), 2) == 3.69   # the range quoted in the lesson
    assert r["path"][-1] > 1.9 and r["path"][-1] < 3.0
    print("lesson 3 ok")
