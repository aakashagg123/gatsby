"""Lesson 6: three model families on two kinds of data.

Data A (churn table): every family does about as well.
Data B (an interaction): the label depends on two columns TOGETHER. A straight-line model cannot see it.

Run: python3 lesson6_model_families.py
"""
import random

from data import make_customers, split, standardize
from lesson3_gradient_descent import predict as logistic_predict
from lesson3_gradient_descent import train_logistic
from lesson5_metrics import auc
from mlp import TinyNet
from tree import grow, proba


def make_interaction(n, seed=5, noise=0.05):
    """Two scores in [-1, 1]. The label is 1 when they have the SAME sign (an XOR-like rule)."""
    rng = random.Random(seed)
    rows, labels = [], []
    for _ in range(n):
        x1, x2 = rng.uniform(-1, 1), rng.uniform(-1, 1)
        y = 1 if x1 * x2 > 0 else 0
        if rng.random() < noise:
            y = 1 - y
        rows.append([x1, x2])
        labels.append(y)
    return rows, labels


def acc(probs, truth):
    return sum((p >= 0.5) == (t == 1) for p, t in zip(probs, truth)) / len(truth)


def gradient_check(net, rows, labels, eps=1e-5):
    """Compare backpropagation with a slow, obviously-correct numerical slope. They must agree."""
    g_w1, _, g_w2, g_b2 = net.gradients(rows, labels)
    worst = 0.0
    checks = [(net.w1[0], 0, g_w1[0][0]), (net.w1[1], 1, g_w1[1][1]), (net.w2, 2, g_w2[2])]
    for arr, i, analytic in checks:
        old = arr[i]
        arr[i] = old + eps
        up = net.loss(rows, labels)
        arr[i] = old - eps
        down = net.loss(rows, labels)
        arr[i] = old
        numeric = (up - down) / (2 * eps)
        worst = max(worst, abs(numeric - analytic) / max(1e-8, abs(numeric) + abs(analytic)))
    return worst


def main():
    out = {}
    # Data A: the churn table.
    rows, labels = make_customers(8000)
    tr_x, tr_y, te_x, te_y = split(rows, labels, test_fraction=0.5)
    s_tr, s_te = standardize(tr_x, [te_x])
    w, b, _ = train_logistic(s_tr, tr_y)
    out["A_linear_auc"] = auc(logistic_predict(w, b, s_te), te_y)
    tree = grow(tr_x, tr_y, 4, min_leaf=20)
    out["A_tree_auc"] = auc([proba(tree, x) for x in te_x], te_y)

    # Data B: the interaction.
    rows, labels = make_interaction(700)
    tr_x, tr_y, te_x, te_y = rows[:300], labels[:300], rows[300:], labels[300:]
    w, b, _ = train_logistic(tr_x, tr_y, lr=0.5, epochs=300)
    out["B_linear_acc"] = acc(logistic_predict(w, b, te_x), te_y)
    tree = grow(tr_x, tr_y, 5, min_leaf=5)
    out["B_tree_acc"] = acc([proba(tree, x) for x in te_x], te_y)
    net = TinyNet(n_hidden=6, seed=0)
    out["grad_check"] = gradient_check(net, tr_x[:40], tr_y[:40])
    curve = net.train(tr_x, tr_y, lr=0.8, epochs=800)
    out["B_net_acc"] = acc(net.predict(te_x), te_y)
    out["net_loss_start"], out["net_loss_end"] = curve[0], curve[-1]
    out["params"] = sum(len(r) for r in net.w1) + len(net.b1) + len(net.w2) + 1
    return out


if __name__ == "__main__":
    r = main()
    for k, v in r.items():
        print(k, (f"{v:.3g}" if k == "grad_check" else round(v, 4)) if isinstance(v, float) else v)
    assert r["grad_check"] < 1e-5                          # backprop matches the numerical slope
    assert abs(r["A_linear_auc"] - r["A_tree_auc"]) < 0.08  # table data: families are close
    assert r["B_linear_acc"] < 0.62                        # a straight line cannot see the interaction
    assert r["B_tree_acc"] > 0.8 and r["B_net_acc"] > 0.85
    assert r["net_loss_end"] < r["net_loss_start"] / 2
    print("lesson 6 ok")
