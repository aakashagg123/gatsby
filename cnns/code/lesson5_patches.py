"""Lesson 5: CNNs vs. vision transformers.

A vision transformer (ViT) cuts the image into square patches and treats each patch as a
token. This file counts tokens and attention scores at two resolutions, compares the growth
with a convolution layer, and checks that "flatten each patch, multiply by one weight table"
is the same as a convolution whose kernel and stride both equal the patch size.
Run: python3 cnns/code/lesson5_patches.py
"""
import random


def vit_tokens(image, patch, class_token=True):
    """(image // patch)^2 patch tokens, plus one class token (torchvision adds one)."""
    assert image % patch == 0, "torchvision asserts the image divides into whole patches"
    return (image // patch) ** 2 + (1 if class_token else 0)


def patchify(img, p):
    """Split an H x W x C image (nested lists) into flattened p x p patches, row by row."""
    h, w = len(img), len(img[0])
    out = []
    for i in range(0, h, p):
        for j in range(0, w, p):
            out.append([img[i + a][j + b][c] for a in range(p) for b in range(p) for c in range(len(img[0][0]))])
    return out


def embed_patches(patches, weights):
    """Each patch vector times a (patch_len, dim) weight table: one token per patch."""
    return [[sum(v * weights[k][d] for k, v in enumerate(patch)) for d in range(len(weights[0]))] for patch in patches]


def conv_patch_embed(img, p, weights):
    """The same thing written as a convolution with kernel = stride = p."""
    h, w, c = len(img), len(img[0]), len(img[0][0])
    out = []
    for i in range(0, h - p + 1, p):          # stride p: windows never overlap
        for j in range(0, w - p + 1, p):
            window = [img[i + a][j + b][ch] for a in range(p) for b in range(p) for ch in range(c)]
            out.append([sum(v * weights[k][d] for k, v in enumerate(window)) for d in range(len(weights[0]))])
    return out


def main():
    # 1. Tokens and attention scores for ViT-B/16 (patch 16) at 224 and 448 pixels.
    t224, t448 = vit_tokens(224, 16), vit_tokens(448, 16)
    s224, s448 = t224 ** 2, t448 ** 2
    print(f"224 px: {t224} tokens, {s224:,} scores per head per layer")
    print(f"448 px: {t448} tokens, {s448:,} scores per head per layer ({s448 / s224:.1f}x)")
    assert (t224, t448) == (197, 785)
    assert (s224, s448) == (38_809, 616_225)
    assert round(s448 / s224, 1) == 15.9

    # 2. Over the whole ViT-B/16 encoder (12 layers, 12 heads in torchvision's vit_b_16).
    layers = heads = 12
    assert s224 * layers * heads == 5_588_496
    assert s448 * layers * heads == 88_736_400

    # 3. A convolution layer at the same two sizes grows 4x (lesson 2).
    conv = lambda side: 2 * side * side * 64 * 3 * 3 * 3
    assert conv(448) == 4 * conv(224)

    # 4. One 16 x 16 RGB patch is 768 numbers.
    assert 16 * 16 * 3 == 768

    # 5. Patch embedding = a convolution with kernel = stride = patch size.
    rng = random.Random(3)
    img = [[[rng.uniform(-1, 1) for _ in range(3)] for _ in range(8)] for _ in range(8)]   # 8 x 8 x 3
    p, dim = 4, 5
    weights = [[rng.uniform(-1, 1) for _ in range(dim)] for _ in range(p * p * 3)]
    a = embed_patches(patchify(img, p), weights)
    b = conv_patch_embed(img, p, weights)
    assert len(a) == len(b) == vit_tokens(8, 4, class_token=False) == 4
    assert max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb)) < 1e-12
    print("all lesson 5 checks pass")


if __name__ == "__main__":
    main()
