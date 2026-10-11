"""Lesson 2: how a convolution sees.

A convolution slides one small grid of weights (a kernel) across an image. The same
weights are used at every position. This file checks the output-size formula, shows that a
convolution is one matrix multiplication in disguise (im2col), counts parameters and FLOPs
for the worked example, and shows that a shifted input gives a shifted output.
Run: python3 cnns/code/lesson2_convolution.py
"""


def out_size(w, f, s=1, p=0):
    """Output width for input width w, kernel f, stride s, padding p: (W - F + 2P) / S + 1."""
    assert (w - f + 2 * p) % s == 0, "the kernel does not fit evenly; most libraries round down"
    return (w - f + 2 * p) // s + 1


def pad(img, p):
    """Zero-pad a 2-D grid (list of rows) by p on every side."""
    w = len(img[0])
    rows = [[0.0] * (w + 2 * p) for _ in range(p)]
    body = [[0.0] * p + list(r) + [0.0] * p for r in img]
    return rows + body + [list(r) for r in rows]


def conv2d(img, kernel, stride=1, padding=0, bias=0.0):
    """One input channel, one kernel. Plain loops: slide, multiply, add."""
    x = pad(img, padding) if padding else img
    f = len(kernel)
    oh = out_size(len(img), f, stride, padding)
    ow = out_size(len(img[0]), f, stride, padding)
    out = []
    for i in range(oh):
        row = []
        for j in range(ow):
            total = bias
            for a in range(f):
                for b in range(f):
                    total += kernel[a][b] * x[i * stride + a][j * stride + b]
            row.append(total)
        out.append(row)
    return out


def im2col(img, f, stride=1):
    """Stretch every f x f window into one column. One column per output position."""
    oh, ow = out_size(len(img), f, stride), out_size(len(img[0]), f, stride)
    cols = []
    for i in range(oh):
        for j in range(ow):
            cols.append([img[i * stride + a][j * stride + b] for a in range(f) for b in range(f)])
    return cols, oh, ow


def conv_as_matmul(img, kernel, stride=1):
    """The same convolution as one row of weights times a matrix of windows."""
    flat_k = [v for row in kernel for v in row]
    cols, oh, ow = im2col(img, len(kernel), stride)
    flat = [sum(k * c for k, c in zip(flat_k, col)) for col in cols]
    return [flat[r * ow:(r + 1) * ow] for r in range(oh)]


def conv_params(f, c_in, c_out):
    """Weights F*F*C_in per kernel, C_out kernels, plus one bias per kernel."""
    return f * f * c_in * c_out + c_out


def conv_flops(h_out, w_out, c_out, f, c_in):
    """2 FLOPs (a multiply and an add) per weight per output value. Bias ignored."""
    return 2 * h_out * w_out * c_out * f * f * c_in


def main():
    # 1. The output-size formula, with the CS231n examples (7x7 input, 3x3 kernel).
    assert out_size(7, 3, s=1, p=0) == 5
    assert out_size(7, 3, s=2, p=0) == 3
    assert out_size(224, 3, s=1, p=1) == 224          # padding 1 keeps a 3x3 layer the same size

    # 2. An edge detector. Left half dark (0), right half bright (1).
    img = [[0.0, 0.0, 0.0, 1.0, 1.0, 1.0] for _ in range(6)]
    vertical_edge = [[-1.0, 0.0, 1.0]] * 3              # bright on the right, dark on the left
    out = conv2d(img, vertical_edge)
    print("edge response row:", out[0])
    assert out[0] == [0.0, 3.0, 3.0, 0.0]               # fires only where the edge is

    # 3. Same weights everywhere: shift the image one pixel right, the response shifts too.
    shifted = [[0.0] + row[:-1] for row in img]
    out_shifted = conv2d(shifted, vertical_edge)
    assert out_shifted[0] == [0.0, 0.0, 3.0, 3.0]
    assert out_shifted[0][1:] == out[0][:-1]

    # 4. A convolution is one matrix multiplication over stretched windows (im2col).
    import random
    rng = random.Random(7)
    x = [[rng.uniform(-1, 1) for _ in range(9)] for _ in range(9)]
    k = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(3)]
    for s in (1, 2):
        a, b = conv2d(x, k, stride=s), conv_as_matmul(x, k, stride=s)
        assert max(abs(p - q) for ra, rb in zip(a, b) for p, q in zip(ra, rb)) < 1e-12

    # 5. Worked example: 224 x 224 RGB, 3x3 kernels, 64 of them, stride 1, padding 1.
    h = w = out_size(224, 3, s=1, p=1)
    params = conv_params(3, 3, 64)
    flops = conv_flops(h, w, 64, 3, 3)
    inputs, outputs = 224 * 224 * 3, h * w * 64
    dense = inputs * outputs                           # weights of a fully connected layer, no bias
    print(f"output {h}x{w}x64, params {params:,}, FLOPs {flops:,}")
    print(f"dense layer: {inputs:,} inputs x {outputs:,} outputs = {dense:,} weights")
    assert (h, w) == (224, 224)
    assert params == 1_792
    assert flops == 173_408_256
    assert (inputs, outputs) == (150_528, 3_211_264)
    assert dense == 483_385_147_392
    assert dense // params == 269_746_176 and dense % params == 0

    # 6. Double the resolution: 4x the FLOPs, the same parameters.
    flops_448 = conv_flops(448, 448, 64, 3, 3)
    assert flops_448 == 4 * flops
    assert conv_params(3, 3, 64) == params

    # 7. The CS231n AlexNet first-layer numbers: 55*55*96 positions, 11*11*3 + 1 per position.
    assert 55 * 55 * 96 * (11 * 11 * 3 + 1) == 105_705_600   # without sharing
    assert conv_params(11, 3, 96) == 34_944                    # with sharing
    print("all lesson 2 checks pass")


if __name__ == "__main__":
    main()
