"""Lesson 3: matrix multiplication, the workhorse. A layer is one multiply plus a bias.

Run: python3 lesson3_matmul.py
"""
import math
import os
import random
import sys

from tensor import DTYPE_BYTES, Tensor, close, matmul_flops

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "machine-learning", "code"))
from data import make_customers, standardize  # noqa: E402
from mlp import TinyNet, sigmoid  # noqa: E402


def linear(x, w, b):
    """A linear layer: (batch, in) times (in, out), plus a bias of shape (out,) stretched over the batch."""
    return x.matmul(w) + b


def tiny_net_forward(net, x):
    """The forward pass of the machine-learning module's TinyNet, written as two matrix multiplies."""
    hidden, n_in = len(net.w1), len(net.w1[0])
    w1 = Tensor.from_nested(net.w1).transpose()               # (hidden, in) -> (in, hidden)
    b1 = Tensor(list(net.b1), (hidden,))
    w2 = Tensor(list(net.w2), (hidden, 1))
    h = linear(x, w1, b1).map(math.tanh)                      # (batch, hidden)
    z = linear(h, w2, Tensor([net.b2], (1,)))                 # (batch, 1)
    return h, z.map(sigmoid)


def intensity(m, k, n, dtype="float32"):
    """FLOPs per byte moved, if each matrix is read or written once. A model, not a measurement."""
    moved = DTYPE_BYTES[dtype] * (m * k + k * n + m * n)
    return matmul_flops(m, k, n) / moved


def main():
    # 1. The rule on a small example: (2,3) times (3,2) gives (2,2).
    a = Tensor.from_nested([[1, 2, 3], [4, 5, 6]])
    b = Tensor.from_nested([[7, 8], [9, 10], [11, 12]])
    ab = a.matmul(b)
    try:
        a.matmul(a)
        refused = False
    except ValueError:
        refused = True

    # 2. TinyNet as matrix multiplies, on a batch of customers (two standardized columns).
    rows, labels = make_customers(200)
    x2 = [[r[1], r[2]] for r in rows]
    (x2,) = standardize(x2)
    net = TinyNet(n_in=2, n_hidden=6, seed=3)
    batch = Tensor.from_nested(x2)
    h, p = tiny_net_forward(net, batch)
    row_by_row = [net.forward(x)[1] for x in x2]
    worst = max(abs(u - v) for u, v in zip(p.data, row_by_row))
    flops = matmul_flops(200, 2, 6) + matmul_flops(200, 6, 1)

    # 3. A batch of 3-D input: (batch, tokens, features) times (features, out).
    seq = Tensor(list(range(2 * 3 * 4)), (2, 3, 4)).map(float)
    w = Tensor.full((4, 5), 0.5)
    out3 = seq.matmul(w)

    # 4. Why one big multiply beats many small ones: the weights are read once, not once per input.
    k = n = 4096
    table = {m: intensity(m, k, n) for m in (1, 8, 64, 512)}
    weight_bytes = DTYPE_BYTES["float32"] * k * n
    one_by_one = 512 * weight_bytes                           # 512 separate (1,k) x (k,n) products
    batched = weight_bytes                                    # one (512,k) x (k,n) product
    return dict(ab=ab, refused=refused, worst=worst, flops=flops, p=p, out3=out3, table=table,
                ratio=one_by_one / batched)


if __name__ == "__main__":
    r = main()
    print("(2,3) @ (3,2) =", r["ab"].tolist(), "| a (2,3) @ (2,3) is refused:", r["refused"])
    print(f"TinyNet forward as matmul vs the hand-written loop: largest difference {r['worst']:.2e}")
    print(f"FLOPs for one forward pass of 200 customers: {r['flops']:,}")
    print("batched (2,3,4) @ (4,5) shape:", r["out3"].shape)
    print("FLOPs per byte moved for a 4096 x 4096 layer, by batch size:",
          {m: round(v, 2) for m, v in r["table"].items()})
    print(f"512 single-row products read the weights {r['ratio']:.0f} times as many bytes as one batched product")
    assert r["ab"].tolist() == [[58.0, 64.0], [139.0, 154.0]]
    assert r["refused"]
    assert r["worst"] < 1e-12
    assert r["flops"] == 2 * 200 * 2 * 6 + 2 * 200 * 6 * 1
    assert r["out3"].shape == (2, 3, 5) and r["out3"].tolist()[0][0] == [3.0] * 5      # (0+1+2+3) * 0.5
    t = r["table"]
    assert t[1] < 1.0 < t[8] < t[64] < t[512] and t[512] > 100
    assert r["ratio"] == 512
    print("lesson 3 ok")
