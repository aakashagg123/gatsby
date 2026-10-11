"""Lesson 5: automatic differentiation. A library records the forward pass, then walks it backward
and applies the chain rule. Nobody writes the gradient by hand.

This is a small reverse-mode autograd on tensors. It is checked against the hand-written gradients
of the machine-learning module's TinyNet, and against a slow numerical slope.

Run: python3 lesson5_autograd.py
"""
import math
import os
import sys

from tensor import Tensor, prod

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "machine-learning", "code"))
from data import make_customers, standardize  # noqa: E402
from mlp import TinyNet, sigmoid  # noqa: E402


def unbroadcast(g, shape):
    """Undo a broadcast on the way back: sum the gradient over every axis that was stretched."""
    while g.rank > len(shape):
        g = g.sum(axis=0)
    for axis, size in enumerate(shape):
        if size == 1 and g.shape[axis] != 1:
            g = g.sum(axis=axis, keepdims=True)
    return g


class Var:
    """A tensor that remembers how it was made. `grad` holds d(loss)/d(this tensor)."""

    def __init__(self, value, parents=(), backward=None):
        self.value = value
        self.parents = parents
        self._backward = backward
        self.grad = Tensor.full(value.shape, 0.0)

    def _accumulate(self, g):
        self.grad = self.grad + g                       # gradients add up, they are not overwritten

    def backward(self):
        order, seen = [], set()

        def visit(v):
            if id(v) not in seen:
                seen.add(id(v))
                for p in v.parents:
                    visit(p)
                order.append(v)
        visit(self)
        self._accumulate(Tensor.full(self.value.shape, 1.0))        # d(loss)/d(loss) = 1
        for v in reversed(order):
            if v._backward:
                v._backward(v.grad)

    def zero_grad(self):
        self.grad = Tensor.full(self.value.shape, 0.0)


def matmul(a, b):
    def back(g):
        a._accumulate(g.matmul(b.value.transpose()))
        b._accumulate(a.value.transpose().matmul(g))
    return Var(a.value.matmul(b.value), (a, b), back)


def add(a, b):
    def back(g):
        a._accumulate(unbroadcast(g, a.value.shape))
        b._accumulate(unbroadcast(g, b.value.shape))
    return Var(a.value + b.value, (a, b), back)


def tanh(a):
    out = a.value.map(math.tanh)

    def back(g):
        a._accumulate(g * out.map(lambda t: 1.0 - t * t))
    return Var(out, (a,), back)


def sigmoid_op(a):
    out = a.value.map(sigmoid)

    def back(g):
        a._accumulate(g * out.map(lambda p: p * (1.0 - p)))
    return Var(out, (a,), back)


def log_loss(p, labels):
    """Average log loss of probabilities p (batch, 1) against 0/1 labels."""
    n = len(labels)
    value = 0.0
    for pv, y in zip(p.value.data, labels):
        pv = min(max(pv, 1e-9), 1 - 1e-9)
        value += -(y * math.log(pv) + (1 - y) * math.log(1 - pv))

    def back(g):
        grads = [(min(max(pv, 1e-9), 1 - 1e-9) - y) / (min(max(pv, 1e-9), 1 - 1e-9) * (1 - min(max(pv, 1e-9), 1 - 1e-9))) / n
                 for pv, y in zip(p.value.data, labels)]
        p._accumulate(Tensor(grads, p.value.shape) * g.data[0])
    return Var(Tensor([value / n], ()), (p,), back)


class Net:
    """TinyNet as autograd variables: p = sigmoid(tanh(x W1 + b1) W2 + b2)."""

    def __init__(self, tiny):
        hidden = len(tiny.w1)
        self.w1 = Var(Tensor.from_nested(tiny.w1).transpose())               # (in, hidden)
        self.b1 = Var(Tensor(list(tiny.b1), (hidden,)))
        self.w2 = Var(Tensor(list(tiny.w2), (hidden, 1)))
        self.b2 = Var(Tensor([tiny.b2], (1,)))
        self.params = [self.w1, self.b1, self.w2, self.b2]

    def loss(self, x, labels, detach_hidden=False):
        h = tanh(add(matmul(Var(x), self.w1), self.b1))
        if detach_hidden:
            h = Var(h.value)                      # a copy with no history: the graph is cut here
        p = sigmoid_op(add(matmul(h, self.w2), self.b2))
        return log_loss(p, labels), h, p

    def zero_grad(self):
        for v in self.params:
            v.zero_grad()


def graph_numbers(root):
    """How many numbers the graph keeps alive for the backward pass (every non-leaf value)."""
    seen, total = set(), 0

    def visit(v):
        nonlocal total
        if id(v) in seen:
            return
        seen.add(id(v))
        if v.parents:
            total += v.value.size
        for p in v.parents:
            visit(p)
    visit(root)
    return total


def main():
    rows, labels = make_customers(200)
    cols = [[r[1], r[2]] for r in rows]
    (cols,) = standardize(cols)
    x = Tensor.from_nested(cols)

    tiny = TinyNet(n_in=2, n_hidden=6, seed=3)
    net = Net(tiny)
    loss, h, p = net.loss(x, labels)
    loss.backward()
    g_w1, g_b1, g_w2, g_b2 = tiny.gradients(cols, labels)                    # the hand-written gradients
    diff = max(
        max(abs(a - b) for a, b in zip(net.w1.grad.transpose().data, [v for row in g_w1 for v in row])),
        max(abs(a - b) for a, b in zip(net.b1.grad.data, g_b1)),
        max(abs(a - b) for a, b in zip(net.w2.grad.data, g_w2)),
        abs(net.b2.grad.data[0] - g_b2),
    )
    stored = graph_numbers(loss)

    # A numerical check on a few weights: nudge, measure the loss, take the slope.
    eps, numeric_worst = 1e-6, 0.0
    for var, idx in ((net.w1, 3), (net.w2, 2), (net.b1, 1), (net.b2, 0)):
        base = var.value.data[idx]
        var.value.data[idx] = base + eps
        up = net.loss(x, labels)[0].value.data[0]
        var.value.data[idx] = base - eps
        down = net.loss(x, labels)[0].value.data[0]
        var.value.data[idx] = base
        numeric_worst = max(numeric_worst, abs((up - down) / (2 * eps) - var.grad.data[idx]))

    # Gradients accumulate across passes: a second forward and backward without zeroing doubles them.
    first = list(net.w2.grad.data)
    again, _, _ = net.loss(x, labels)
    again.backward()
    doubled = all(abs(b - 2 * a) < 1e-12 for a, b in zip(first, net.w2.grad.data))

    # A cut graph: the hidden layer gets no gradient, so it would never learn.
    net.zero_grad()
    cut_loss, _, _ = net.loss(x, labels, detach_hidden=True)
    cut_loss.backward()
    cut_w1 = max(abs(v) for v in net.w1.grad.data)
    cut_w2 = max(abs(v) for v in net.w2.grad.data)

    # Training with autograd: the loss falls.
    train_net = Net(TinyNet(n_in=2, n_hidden=6, seed=3))
    curve = []
    for _ in range(300):
        train_net.zero_grad()
        l, _, _ = train_net.loss(x, labels)
        l.backward()
        curve.append(l.value.data[0])
        for v in train_net.params:
            v.value = v.value - v.grad * 0.8
    return dict(diff=diff, numeric=numeric_worst, doubled=doubled, cut_w1=cut_w1, cut_w2=cut_w2, curve=curve,
                stored=stored, loss0=loss.value.data[0], batch=len(labels))


if __name__ == "__main__":
    r = main()
    print(f"largest gap between autograd and the hand-written gradients: {r['diff']:.2e}")
    print(f"largest gap between autograd and a numerical slope:          {r['numeric']:.2e}")
    print(f"numbers kept alive for the backward pass (200 customers): {r['stored']:,}")
    print("a second forward and backward pass doubles the gradients unless you zero them:", r["doubled"])
    print(f"cut graph: largest hidden-layer gradient {r['cut_w1']}, largest output-layer gradient {r['cut_w2']:.3f}")
    print(f"training with autograd: loss {r['curve'][0]:.3f} -> {r['curve'][-1]:.3f} in {len(r['curve'])} steps")
    assert r["diff"] < 1e-9
    assert r["numeric"] < 1e-6
    assert r["doubled"]
    assert r["cut_w1"] == 0.0 and r["cut_w2"] > 0.0
    assert r["curve"][-1] < r["curve"][0] and all(b <= a + 1e-12 for a, b in zip(r["curve"], r["curve"][1:]))
    assert r["stored"] == 3 * r["batch"] * 6 + 3 * r["batch"] + 1          # three (batch, 6), three (batch, 1) and the loss
    print("lesson 5 ok")
