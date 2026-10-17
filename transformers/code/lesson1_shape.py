"""Lesson 1: the shape of a transformer. Where the parameters live and where the multiplies go.

Run: python3 lesson1_shape.py
"""
from mini_transformer import Config, Transformer, count_params, reset_ops, OPS

GPT2_SMALL = dict(d=768, layers=12, vocab=50257, max_len=1024)      # the configuration of the small GPT-2 model


def shares(d, layers, vocab, max_len, d_ff=None):
    """Split a model's parameters into embeddings, attention and MLP."""
    d_ff = d_ff or 4 * d
    attn, mlp = layers * (4 * d * d + 4 * d), layers * (2 * d * d_ff + d_ff + d)
    emb = vocab * d + max_len * d
    return dict(embeddings=emb, attention=attn, mlp=mlp)


def flops_per_token(d, layers, vocab, n, d_ff=None):
    """Multiply-adds for one token in a pass over n tokens: projections, MLP, scores, unembedding."""
    d_ff = d_ff or 4 * d
    dense = layers * (4 * d * d + 2 * d * d_ff) + d * vocab
    attn = layers * 2 * n * d
    return dense, attn


def main():
    gpt2 = count_params(**GPT2_SMALL)
    s = shares(**GPT2_SMALL)
    cfg = Config(d_model=16, n_heads=4, n_layers=2, vocab=32, max_len=64)
    model = Transformer(cfg)
    formula = count_params(16, 2, 32, 64, bias=False, layernorm=False)
    n = 8
    reset_ops()
    model.forward(list(range(n)))
    counted = sum(OPS.values())
    dense, attn = flops_per_token(16, 2, 32, n)
    return dict(gpt2=gpt2, shares=s, tiny_counted=model.n_params(), tiny_formula=formula,
                madds_counted=counted, madds_formula=n * dense + n * attn)


if __name__ == "__main__":
    r = main()
    s = r["shares"]
    total = sum(s.values())
    print(f"GPT-2 small by formula: {r['gpt2']:,} parameters")
    for k, v in s.items():
        print(f"  {k:10s} {v:>12,}  {100 * v / r['gpt2']:.1f}%")
    block_total = s["attention"] + s["mlp"]
    print(f"  inside the 12 blocks: attention {100 * s['attention'] / block_total:.1f}%, MLP {100 * s['mlp'] / block_total:.1f}%")
    print(f"tiny model: {r['tiny_counted']:,} weights counted, {r['tiny_formula']:,} by formula")
    print(f"tiny forward pass over 8 tokens: {r['madds_counted']:,} multiply-adds counted, {r['madds_formula']:,} by formula")
    assert r["gpt2"] == 124_439_808
    assert r["tiny_counted"] == r["tiny_formula"]
    assert r["madds_counted"] == r["madds_formula"]
    assert 0.66 < s["mlp"] / (s["attention"] + s["mlp"]) < 0.68        # the MLP holds about two thirds of a block
    print("lesson 1 ok")
