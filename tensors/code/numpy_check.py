"""Optional: check the small Tensor against NumPy. Skipped, with a message, when NumPy is not installed.

Run: python3 numpy_check.py
"""
import random

from tensor import Tensor, broadcast_shapes

try:
    import numpy as np
except ImportError:                      # the module needs only the standard library
    np = None


def main():
    if np is None:
        return None
    rng = random.Random(5)
    rand = lambda *shape: Tensor([rng.uniform(-2, 2) for _ in range(int(np.prod(shape)))], shape)
    checks = 0

    def same(mine, theirs, tol=1e-9):
        nonlocal checks
        checks += 1
        assert tuple(mine.shape) == tuple(theirs.shape), (mine.shape, theirs.shape)
        assert np.allclose(np.array(mine.data).reshape(mine.shape), theirs, atol=tol)

    a, b, c = rand(4, 3), rand(3, 5), rand(5)
    A, B, C = (np.array(t.data).reshape(t.shape) for t in (a, b, c))
    same(a.matmul(b), A @ B)
    same(a.matmul(b) + c, A @ B + C)                                   # bias stretched over the rows
    same(a.sum(axis=0), A.sum(axis=0))
    same(a.sum(axis=1, keepdims=True), A.sum(axis=1, keepdims=True))
    same(a.mean(axis=1), A.mean(axis=1))
    same(a.transpose(), A.T)
    same(a.reshape(2, 6), A.reshape(2, 6))
    x, y = rand(8, 1, 6, 1), rand(7, 1, 5)
    same(x + y, np.array(x.data).reshape(x.shape) + np.array(y.data).reshape(y.shape))
    for sa, sb in (((8, 1, 6, 1), (7, 1, 5)), ((5, 4), (4,)), ((3, 1), (1, 4)), ((1,), (9, 1, 2))):
        assert broadcast_shapes(sa, sb) == np.broadcast_shapes(sa, sb)
        checks += 1
    t = rand(2, 3, 4)
    assert tuple(s * 8 for s in t.strides) == np.array(t.data).reshape(t.shape).strides   # NumPy counts bytes
    checks += 1
    s3 = rand(2, 3, 4)
    w = rand(4, 5)
    same(s3.matmul(w), np.array(s3.data).reshape(s3.shape) @ np.array(w.data).reshape(w.shape))
    return checks


if __name__ == "__main__":
    n = main()
    if n is None:
        print("numpy check skipped: NumPy is not installed (the module needs only the standard library)")
    else:
        print(f"{n} checks agree with NumPy {np.__version__}")
    print("numpy check ok")
