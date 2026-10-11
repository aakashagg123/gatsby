"""Lesson 2: operations and broadcasting. Most framework bugs are shape bugs, and the worst
ones run without an error.

Run: python3 lesson2_broadcasting.py
"""
import os
import sys

from tensor import Tensor, broadcast_shapes

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "machine-learning", "code"))
from data import make_customers  # noqa: E402


def main():
    # The rule, on the example from the NumPy documentation.
    rule = broadcast_shapes((8, 1, 6, 1), (7, 1, 5))

    # Standardize the churn table: (1000, 4) minus a (4,) vector of column means.
    rows, labels = make_customers(1000)
    x = Tensor.from_nested(rows)
    col_mean = x.mean(axis=0)
    centered = x - col_mean
    after = centered.mean(axis=0)
    stretched_strides = col_mean.broadcast_strides(x.shape)          # (0, 1): row axis is re-read

    # Silent bug 1: a square table. The wrong axis still has a legal shape.
    sq = Tensor.from_nested([[1, 2, 3, 4], [2, 4, 6, 8], [0, 0, 0, 0], [10, 20, 30, 40]])
    right = sq - sq.mean(axis=1, keepdims=True)                      # (4,4) - (4,1): centers each row
    wrong = sq - sq.mean(axis=1)                                     # (4,4) - (4,): legal, wrong axis
    row_means_right = right.mean(axis=1).data
    row_means_wrong = wrong.mean(axis=1).data
    taller = Tensor.full((5, 4), 1.0)                                # the same slip on a 5x4 table
    try:
        taller - taller.mean(axis=1)
        taller_failed = False
    except ValueError:
        taller_failed = True

    # Silent bug 2: predictions of shape (n, 1) against labels of shape (n,). The difference is (n, n).
    n = 300
    y = Tensor([float(v) for v in labels[:n]], (n,))
    p = Tensor([0.15 + 0.5 * float(v) for v in labels[:n]], (n, 1))     # predictions that carry signal
    wrong_diff = p - y
    right_diff = p.reshape(n) - y
    wrong_loss = (wrong_diff * wrong_diff).mean()
    right_loss = (right_diff * right_diff).mean()

    # A shape that cannot work is refused, which is the good case.
    try:
        Tensor.full((3,)) + Tensor.full((4,))
        refused = False
    except ValueError:
        refused = True
    return dict(rule=rule, shape=centered.shape, after=after.data, strides=stretched_strides,
                row_means_right=row_means_right, row_means_wrong=row_means_wrong,
                taller_failed=taller_failed, wrong_shape=wrong_diff.shape, right_shape=right_diff.shape,
                wrong_loss=wrong_loss, right_loss=right_loss, refused=refused, n=n)


if __name__ == "__main__":
    r = main()
    print("broadcast (8,1,6,1) with (7,1,5):", r["rule"])
    print("centered table:", r["shape"], "column means after:", [round(v, 12) for v in r["after"]],
          "| strides used to stretch the (4,) vector:", r["strides"])
    print("square table, right axis, row means:", [round(v, 6) for v in r["row_means_right"]])
    print("square table, wrong axis, row means:", [round(v, 3) for v in r["row_means_wrong"]], "(no error)")
    print("the same slip on a 5x4 table raises an error:", r["taller_failed"])
    print(f"predictions (n,1) minus labels (n,) -> shape {r['wrong_shape']} ({r['wrong_shape'][0] * r['wrong_shape'][1]:,} numbers, not {r['n']})")
    print(f"squared-error loss: wrong {r['wrong_loss']:.4f}, right {r['right_loss']:.4f}")
    assert r["rule"] == (8, 7, 6, 5)
    assert r["shape"] == (1000, 4) and all(abs(v) < 1e-9 for v in r["after"])
    assert r["strides"] == (0, 1)
    assert all(abs(v) < 1e-9 for v in r["row_means_right"])
    assert any(abs(v) > 1.0 for v in r["row_means_wrong"])         # the wrong axis leaves rows uncentered
    assert r["taller_failed"] and r["refused"]
    assert r["wrong_shape"] == (300, 300) and r["right_shape"] == (300,)
    assert abs(r["wrong_loss"] - r["right_loss"]) > 0.01           # same code path, a different number
    print("lesson 2 ok")
