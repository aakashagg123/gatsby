"""Lesson 4: position, and what a longer context costs.

Run: python3 lesson4_position_cost.py
"""
import math
import random

from mini_transformer import Config, OPS, Transformer, reset_ops


def order_blindness(seed=5):
    """With no position signal and no mask, shuffling the input shuffles the output the same way."""
    tokens, order = [4, 9, 2, 7, 1], [3, 0, 4, 1, 2]
    results = {}
    for mode in ("none", "learned"):
        m = Transformer(Config(d_model=16, n_heads=4, n_layers=2, vocab=16, max_len=16, pos=mode), seed)
        a = m.forward(tokens, causal=False)
        b = m.forward([tokens[i] for i in order], causal=False)
        results[mode] = max(abs(x - y) for i, j in enumerate(order) for x, y in zip(a[j], b[i]))
    return results


def rope(vec, pos, base=10000.0):
    """Rotary position embedding: turn each pair of numbers by an angle that grows with position."""
    out = []
    for i in range(0, len(vec), 2):
        angle = pos / base ** (i / len(vec))
        c, s = math.cos(angle), math.sin(angle)
        out += [vec[i] * c - vec[i + 1] * s, vec[i] * s + vec[i + 1] * c]
    return out


def rope_is_relative(seed=6):
    rng = random.Random(seed)
    q = [rng.gauss(0, 1) for _ in range(16)]
    k = [rng.gauss(0, 1) for _ in range(16)]
    dot = lambda a, b: sum(x * y for x, y in zip(a, b))
    return dot(rope(q, 10), rope(k, 4)), dot(rope(q, 110), rope(k, 104)), dot(rope(q, 10), rope(k, 7))


def cost_split(d=8, n=None):
    """Multiply-adds in attention and in everything else, for a one-layer model with d_ff = 4d."""
    n = n or 6 * d
    m = Transformer(Config(d_model=d, n_heads=2, n_layers=1, vocab=8, max_len=n, d_ff=4 * d))
    reset_ops()
    m.forward([i % 8 for i in range(n)])
    return OPS["attn"], OPS["proj"] + OPS["kv"] + OPS["mlp"], n


def score_matrix_bytes(n, heads=32, bytes_per=2):
    """Size of the attention score matrices for one layer and one sequence, if they are stored in full."""
    return heads * n * n * bytes_per


def main():
    attn, rest, n = cost_split()
    lo, hi = cost_split(n=6 * 8 // 2)[:2], cost_split(n=6 * 8 * 2)[:2]
    return dict(blind=order_blindness(), rope=rope_is_relative(), split=(attn, rest, n),
                below=lo, above=hi, sizes={k: score_matrix_bytes(k) for k in (1024, 8192, 131072)})


if __name__ == "__main__":
    r = main()
    b = r["blind"]
    print(f"largest output difference after shuffling the input: no positions {b['none']:.1e}, learned positions {b['learned']:.2f}")
    a, c, d = r["rope"]
    print(f"rotary: score for offset 6 at positions (10, 4) = {a:.6f}, at (110, 104) = {c:.6f}, offset 3 at (10, 7) = {d:.6f}")
    attn, rest, n = r["split"]
    print(f"d_model 8, {n} tokens (6 x d_model): attention {attn:,} multiply-adds, everything else {rest:,}")
    print(f"  at half that length: attention {r['below'][0]:,} vs {r['below'][1]:,}; at double: {r['above'][0]:,} vs {r['above'][1]:,}")
    for k, v in r["sizes"].items():
        print(f"score matrices, 32 heads, {k:>7,} tokens, 16-bit: {v / 2 ** 20:,.0f} MiB per layer")
    assert b["none"] < 1e-9 and b["learned"] > 0.01                 # order-blind without positions
    assert abs(a - c) < 1e-9 and abs(a - d) > 1e-3                  # the score depends on the offset only
    assert attn == rest                                             # the two costs meet at 6 x d_model tokens
    assert r["below"][0] < r["below"][1] and r["above"][0] > r["above"][1]
    assert r["sizes"][1024] == 64 * 2 ** 20 and r["sizes"][8192] == 4 * 2 ** 30 and r["sizes"][131072] == 2 ** 40
    print("lesson 4 ok")
