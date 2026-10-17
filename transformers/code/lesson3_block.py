"""Lesson 3: the block. Heads write into a shared residual stream. The MLP holds most of the weights.

Run: python3 lesson3_block.py
"""
import copy

from mini_transformer import Config, Transformer, add, layer_norm, matmul, transpose
from lesson1_shape import GPT2_SMALL, shares


def heads_are_additive(seed=3):
    """Concatenating the heads and applying the output matrix equals summing each head's own contribution."""
    cfg = Config(d_model=12, n_heads=3, n_layers=1, vocab=20, max_len=16)
    model = Transformer(cfg, seed)
    L = model.layers[0]
    tokens = [1, 5, 2, 9]
    x = add([model.tok[t] for t in tokens], model.position_rows(0, len(tokens)))
    h = layer_norm(x)
    q, k, v = matmul(h, L["wq"]), matmul(h, L["wk"]), matmul(h, L["wv"])
    joined = matmul(model.attend(q, k, v), L["wo"])
    dk = cfg.d_head
    parts = None
    for head in range(cfg.n_heads):
        keep = lambda m: [[(val if head * dk <= j < (head + 1) * dk else 0.0) for j, val in enumerate(row)] for row in m]
        # a head's contribution: zero every other head's slice of the concatenated output, then apply Wo
        out = model.attend(q, k, v)
        mine = matmul(keep(out), L["wo"])
        parts = mine if parts is None else add(parts, mine)
    return max(abs(a - b) for r, s in zip(joined, parts) for a, b in zip(r, s))


def zero_block_is_identity(seed=4):
    """If a block's output matrices are zero, the block returns its input. Residuals make that possible."""
    cfg = Config(d_model=8, n_heads=2, n_layers=1, vocab=10, max_len=8)
    model = Transformer(cfg, seed)
    L = copy.deepcopy(model.layers[0])
    L["wo"] = [[0.0] * 8 for _ in range(8)]
    L["w2"] = [[0.0] * 8 for _ in range(cfg.d_ff)]
    x = add([model.tok[t] for t in (1, 2, 3)], model.position_rows(0, 3))
    y = model.block(x, L)
    return max(abs(a - b) for r, s in zip(x, y) for a, b in zip(r, s))


def norm_stats():
    rows = layer_norm([[3.0, -1.0, 7.0, 2.0, 0.5, 9.0], [100.0, 120.0, 90.0, 80.0, 110.0, 130.0]])
    return [(sum(r) / len(r), sum(v * v for v in r) / len(r)) for r in rows]


def main():
    s = shares(**GPT2_SMALL)
    return dict(heads=heads_are_additive(), identity=zero_block_is_identity(), norms=norm_stats(), shares=s)


if __name__ == "__main__":
    r = main()
    print(f"largest gap between 'concatenate then project' and 'sum over heads': {r['heads']:.2e}")
    print(f"largest change made by a block whose output matrices are zero: {r['identity']:.1e}")
    print("layer norm, (mean, mean square) per row:", [(round(m, 6), round(v, 4)) for m, v in r["norms"]])
    assert r["heads"] < 1e-12
    assert r["identity"] == 0.0
    assert all(abs(m) < 1e-9 and abs(v - 1) < 1e-4 for m, v in r["norms"])
    print("lesson 3 ok")
