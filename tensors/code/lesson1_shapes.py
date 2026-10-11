"""Lesson 1: what a tensor is. A flat list of numbers plus a shape. Its size in bytes is easy to compute.

Run: python3 lesson1_shapes.py
"""
import os
import sys

from tensor import DTYPE_BYTES, Tensor, prod

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "machine-learning", "code"))
from data import make_customers  # noqa: E402  (the churn table from the machine-learning module)


def megabytes(n_bytes):
    return n_bytes / 2 ** 20


def main():
    # A table of customers is a rank-2 tensor: rows by columns.
    rows, labels = make_customers(1000)
    table = Tensor.from_nested(rows)
    one_row = table[0]                       # indexing drops one axis
    column = [table[i, 1] for i in range(table.shape[0])]

    # A batch of colour images is rank 4: batch, channels, height, width.
    images = (32, 3, 224, 224)
    # A batch of text, after each token is turned into a vector, is rank 3: batch, tokens, features.
    text = (8, 512, 768)

    # Reshape is a view. It changes how the same numbers are read, not the numbers.
    grid = Tensor(list(range(12)), (12,)).reshape(3, 4)
    flat_again = grid.reshape(-1)
    same_storage = grid.data is flat_again.data
    return dict(table=table, one_row=one_row, column=column, images=images, text=text,
                grid=grid, same_storage=same_storage, labels=labels)


if __name__ == "__main__":
    r = main()
    t = r["table"]
    print(f"customer table: shape {t.shape}, rank {t.rank}, {t.size} numbers, strides {t.strides}")
    print(f"first customer: shape {r['one_row'].shape}, values {r['one_row'].data}")
    for name, shape in (("image batch", r["images"]), ("text batch", r["text"])):
        n = prod(shape)
        print(f"{name}: shape {shape}, {n:,} numbers, "
              + ", ".join(f"{d} {megabytes(n * b):.1f} MiB" for d, b in DTYPE_BYTES.items() if d in ("float32", "float16", "int8")))
    print(f"reshape shares storage: {r['same_storage']}; 3x4 grid strides {r['grid'].strides}")
    assert t.shape == (1000, 4) and t.rank == 2 and t.size == 4000
    assert t.strides == (4, 1)                                  # one row is 4 steps; one column step is 1
    assert r["one_row"].shape == (4,) and len(r["column"]) == 1000
    assert prod(r["images"]) * DTYPE_BYTES["float32"] == 19267584      # 32*3*224*224 numbers at 4 bytes each
    assert prod(r["images"]) * DTYPE_BYTES["float16"] * 2 == prod(r["images"]) * DTYPE_BYTES["float32"]
    assert prod(r["text"]) == 3145728 and abs(megabytes(prod(r["text"]) * 4) - 12.0) < 1e-9
    assert r["same_storage"] and r["grid"].shape == (3, 4) and r["grid"][1, 2] == 6.0
    try:
        Tensor([1.0, 2.0, 3.0], (2, 2))
        raise SystemExit("a wrong shape should have been refused")
    except ValueError:
        pass
    print("lesson 1 ok")
