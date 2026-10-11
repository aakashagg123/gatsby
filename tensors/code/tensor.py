"""A very small tensor, built from the Python standard library, to show how the real ones work.

A tensor here is a flat list of numbers plus a shape. The numbers are stored in row-major
order: the last index changes fastest. Everything a framework does with shapes (strides,
reshape as a view, broadcasting, reductions, matrix multiplication) is done here in plain loops,
so you can read it. It is slow on purpose. Real libraries run the same rules in compiled code.
"""
import math

# Bytes per number for the usual formats. These are fixed by the format definitions.
DTYPE_BYTES = {"float64": 8, "float32": 4, "float16": 2, "bfloat16": 2, "int8": 1, "int32": 4, "int64": 8}


def prod(xs):
    out = 1
    for x in xs:
        out *= x
    return out


def row_major_strides(shape):
    """How far to move in the flat list to step one along each axis."""
    strides, step = [], 1
    for size in reversed(shape):
        strides.append(step)
        step *= size
    return tuple(reversed(strides))


def broadcast_shapes(a, b):
    """The broadcasting rule. Line the shapes up from the right. Each pair of sizes must be
    equal, or one of them must be 1 (or missing). The result takes the larger size."""
    out = []
    for i in range(1, max(len(a), len(b)) + 1):
        x = a[-i] if i <= len(a) else 1
        y = b[-i] if i <= len(b) else 1
        if x != y and x != 1 and y != 1:
            raise ValueError(f"shapes {tuple(a)} and {tuple(b)} cannot be broadcast together")
        out.append(max(x, y) if x != 1 and y != 1 else (y if x == 1 else x))
    return tuple(reversed(out))


def _nested_shape(x):
    shape = []
    while isinstance(x, (list, tuple)):
        shape.append(len(x))
        x = x[0] if x else None
    return tuple(shape)


def _flatten(x, out):
    if isinstance(x, (list, tuple)):
        for item in x:
            _flatten(item, out)
    else:
        out.append(float(x))


class Tensor:
    def __init__(self, data, shape):
        shape = tuple(shape)
        if len(data) != prod(shape):
            raise ValueError(f"{len(data)} numbers cannot fill the shape {shape}")
        self.data = data
        self.shape = shape

    # ---- building and inspecting -------------------------------------------------------
    @staticmethod
    def from_nested(x):
        flat = []
        _flatten(x, flat)
        return Tensor(flat, _nested_shape(x))

    @staticmethod
    def full(shape, value=0.0):
        return Tensor([float(value)] * prod(shape), shape)

    @property
    def rank(self):
        return len(self.shape)

    @property
    def size(self):
        return len(self.data)

    @property
    def strides(self):
        return row_major_strides(self.shape)

    def nbytes(self, dtype="float32"):
        return self.size * DTYPE_BYTES[dtype]

    def tolist(self):
        def build(offset, axis):
            if axis == self.rank:
                return self.data[offset]
            step = self.strides[axis]
            return [build(offset + i * step, axis + 1) for i in range(self.shape[axis])]
        return build(0, 0)

    def __getitem__(self, index):
        if not isinstance(index, tuple):
            index = (index,)
        offset = sum(i * s for i, s in zip(index, self.strides))
        if len(index) == self.rank:
            return self.data[offset]
        rest = self.shape[len(index):]
        return Tensor(self.data[offset: offset + prod(rest)], rest)

    # ---- shape changes ---------------------------------------------------------------
    def reshape(self, *shape):
        """A view: the new Tensor shares the same list of numbers. One size may be -1."""
        shape = list(shape[0] if len(shape) == 1 and isinstance(shape[0], (tuple, list)) else shape)
        if -1 in shape:
            known = prod(s for s in shape if s != -1)
            shape[shape.index(-1)] = self.size // known
        return Tensor(self.data, shape)

    def transpose(self):
        """Swap the two axes of a matrix. This copies. Real libraries can return a view."""
        rows, cols = self.shape
        return Tensor([self.data[r * cols + c] for c in range(cols) for r in range(rows)], (cols, rows))

    def broadcast_to(self, shape):
        shape = tuple(shape)
        if broadcast_shapes(self.shape, shape) != shape:
            raise ValueError(f"cannot broadcast {self.shape} to {shape}")
        return Tensor(self._broadcast_data(shape), shape)

    def broadcast_strides(self, shape):
        """The strides a real library uses to stretch this tensor to `shape` without copying:
        a stride of 0 on a stretched axis reads the same number again and again."""
        pad = (1,) * (len(shape) - self.rank) + self.shape
        own = (0,) * (len(shape) - self.rank) + self.strides
        return tuple(0 if p == 1 and s != 1 else st for p, st, s in zip(pad, own, shape))

    def _broadcast_data(self, shape):
        strides = self.broadcast_strides(shape)
        out = []
        index = [0] * len(shape)
        for _ in range(prod(shape)):
            out.append(self.data[sum(i * s for i, s in zip(index, strides))])
            for axis in range(len(shape) - 1, -1, -1):
                index[axis] += 1
                if index[axis] < shape[axis]:
                    break
                index[axis] = 0
        return out

    # ---- elementwise and reductions --------------------------------------------------
    def map(self, fn):
        return Tensor([fn(v) for v in self.data], self.shape)

    def _binary(self, other, op):
        if not isinstance(other, Tensor):
            return Tensor([op(v, other) for v in self.data], self.shape)
        shape = broadcast_shapes(self.shape, other.shape)
        a = self.data if self.shape == shape else self._broadcast_data(shape)
        b = other.data if other.shape == shape else other._broadcast_data(shape)
        return Tensor([op(x, y) for x, y in zip(a, b)], shape)

    def __add__(self, other): return self._binary(other, lambda x, y: x + y)
    def __sub__(self, other): return self._binary(other, lambda x, y: x - y)
    def __mul__(self, other): return self._binary(other, lambda x, y: x * y)
    def __truediv__(self, other): return self._binary(other, lambda x, y: x / y)

    def sum(self, axis=None, keepdims=False):
        if axis is None:
            return sum(self.data)
        axis = axis % self.rank
        out_shape = tuple(1 if i == axis else s for i, s in enumerate(self.shape))
        out = [0.0] * prod(out_shape)
        out_strides = row_major_strides(out_shape)
        for flat in range(self.size):
            rest, o = flat, 0
            for ax, st in enumerate(self.strides):
                idx, rest = divmod(rest, st)
                if ax != axis:
                    o += idx * out_strides[ax]
            out[o] += self.data[flat]
        result = Tensor(out, out_shape)
        return result if keepdims else result.reshape(*[s for i, s in enumerate(out_shape) if i != axis])

    def mean(self, axis=None, keepdims=False):
        if axis is None:
            return sum(self.data) / self.size
        return self.sum(axis, keepdims) * (1.0 / self.shape[axis % self.rank])

    # ---- matrix multiplication -------------------------------------------------------
    def matmul(self, other):
        """(m, k) times (k, n) gives (m, n). A leading batch axis on the left is allowed."""
        if self.rank == 3 and other.rank == 2:
            b, m, k = self.shape
            parts = [self[i].matmul(other) for i in range(b)]
            return Tensor([v for p in parts for v in p.data], (b, m, other.shape[1]))
        if self.rank != 2 or other.rank != 2 or self.shape[1] != other.shape[0]:
            raise ValueError(f"cannot multiply shapes {self.shape} and {other.shape}")
        m, k = self.shape
        n = other.shape[1]
        out = [0.0] * (m * n)
        for i in range(m):
            row = self.data[i * k: (i + 1) * k]
            for j in range(n):
                out[i * n + j] = sum(row[t] * other.data[t * n + j] for t in range(k))
        return Tensor(out, (m, n))

    __matmul__ = matmul

    def __repr__(self):
        return f"Tensor(shape={self.shape})"


def matmul_flops(m, k, n):
    """Each of the m*n outputs needs k multiplies and k-1 adds. The usual count is 2*m*k*n."""
    return 2 * m * k * n


def close(a, b, tol=1e-9):
    return all(abs(x - y) <= tol for x, y in zip(a.data, b.data)) and a.shape == b.shape


tanh = math.tanh
