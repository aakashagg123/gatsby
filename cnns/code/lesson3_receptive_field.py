"""Lesson 3: from edges to objects.

Each layer looks at a small window of the layer before it. Stack layers, and the window
each value sees in the original image (its receptive field) grows. Downsampling makes it
grow faster. This file computes receptive fields and feature-map sizes for small stacks and
for the stem of a ResNet, and shows the arithmetic of a residual (skip) connection.
Run: python3 cnns/code/lesson3_receptive_field.py
"""


def receptive_field(layers):
    """layers: list of (kernel, stride). Returns the receptive field in input pixels.
    Each layer adds (kernel - 1) times the current step between neighbouring values."""
    r, jump = 1, 1
    for k, s in layers:
        r += (k - 1) * jump
        jump *= s
    return r


def out_size(w, f, s=1, p=0):
    """Output width, rounding down as PyTorch does: floor((W - F + 2P) / S) + 1."""
    return (w - f + 2 * p) // s + 1


def residual_block(x, w):
    """y = x + F(x), with F a single weighted step and a ReLU. Lists of numbers."""
    fx = [max(0.0, sum(wij * xj for wij, xj in zip(row, x))) for row in w]
    return [xi + fi for xi, fi in zip(x, fx)]


def plain_block(x, w):
    """y = F(x) only, with no skip connection."""
    return [max(0.0, sum(wij * xj for wij, xj in zip(row, x))) for row in w]


def main():
    # 1. Stacked 3x3 layers at stride 1: the view grows 3, 5, 7 (2n + 1).
    assert [receptive_field([(3, 1)] * n) for n in (1, 2, 3)] == [3, 5, 7]

    # 2. Three 3x3 layers versus one 7x7 layer, C channels in and out (CS231n): 27C^2 vs 49C^2.
    c = 64
    three_small = 3 * (c * 3 * 3 * c)
    one_large = c * 7 * 7 * c
    print(f"C={c}: three 3x3 layers {three_small:,} weights, one 7x7 layer {one_large:,} weights")
    assert three_small == 27 * c * c == 110_592
    assert one_large == 49 * c * c == 200_704
    assert receptive_field([(7, 1)]) == receptive_field([(3, 1)] * 3) == 7

    # 3. Downsampling speeds it up. A ResNet stem: 7x7 conv stride 2, then 3x3 max pool stride 2.
    stem = [(7, 2), (3, 2)]
    assert receptive_field(stem) == 11
    assert receptive_field(stem + [(3, 1)]) == 19        # one more 3x3 layer after the stem
    assert receptive_field([(3, 1)] * 4) == 9            # four 3x3 layers without downsampling
    # ResNet-50 layer1: three bottleneck blocks, one 3x3 each (the 1x1 convs add nothing).
    assert [receptive_field(stem + [(3, 1)] * n) for n in (1, 2, 3)] == [19, 27, 35]
    assert 224 // 56 == 4 and 224 // 7 == 32                  # pixels per position: layer1 vs last stage

    # 4. Feature-map sizes through torchvision's ResNet layout for a 224 x 224 input.
    sizes = [224]
    sizes.append(out_size(sizes[-1], 7, 2, 3))   # conv1: 7x7, stride 2, padding 3
    sizes.append(out_size(sizes[-1], 3, 2, 1))   # max pool: 3x3, stride 2, padding 1
    for _ in range(3):                           # layer2, layer3, layer4 each start with stride 2
        sizes.append(out_size(sizes[-1], 3, 2, 1))
    print("feature-map width:", " -> ".join(map(str, sizes)))
    assert sizes == [224, 112, 56, 28, 14, 7]
    assert 224 // sizes[-1] == 32

    # 5. A residual block with all-zero weights passes its input through. A plain one does not.
    x = [0.5, -1.0, 2.0]
    zeros = [[0.0] * 3 for _ in range(3)]
    assert residual_block(x, zeros) == x
    assert plain_block(x, zeros) == [0.0, 0.0, 0.0]
    print("all lesson 3 checks pass")


if __name__ == "__main__":
    main()
