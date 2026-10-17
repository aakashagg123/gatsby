"""Lesson 6: reading a model card. Grouped-query attention, mixture of experts, and what they do to memory and compute.

The three cards are illustrative configurations, not products. Run: python3 lesson6_variants.py
"""
from mini_transformer import Config, Transformer, cache_numbers

DENSE = dict(layers=32, d=4096, heads=32, kv_heads=32, d_ff=11008, vocab=32000, experts=1, top_k=1)
GQA = dict(DENSE, kv_heads=8)
MOE = dict(layers=32, d=4096, heads=32, kv_heads=8, d_ff=14336, vocab=32000, experts=8, top_k=2)


def card(c, gated=True, bytes_per=2):
    """Total parameters, active parameters per token, weight memory and cache per token."""
    d, dh = c["d"], c["d"] // c["heads"]
    attn = d * d * 2 + 2 * d * c["kv_heads"] * dh                      # query and output, then key and value
    mlp = (3 if gated else 2) * d * c["d_ff"]                           # a gated MLP has three matrices
    norms = (2 * c["layers"] + 1) * d
    emb = 2 * c["vocab"] * d                                            # input table and a separate output matrix
    total = emb + c["layers"] * (attn + c["experts"] * mlp) + norms
    active = emb // 2 + c["layers"] * (attn + c["top_k"] * mlp) + norms     # the input table is a lookup, not a multiply
    kv_per_token = 2 * c["layers"] * c["kv_heads"] * dh * bytes_per
    return dict(total=total, active=active, weight_bytes=total * bytes_per, kv_per_token=kv_per_token)


def gqa_cache_shrink():
    base = Config(d_model=16, n_heads=8, n_layers=2, vocab=20, max_len=32)
    grouped = Config(d_model=16, n_heads=8, n_layers=2, vocab=20, max_len=32, n_kv_heads=2)
    sizes = []
    for cfg in (base, grouped):
        m = Transformer(cfg, 8)
        cache = m.new_cache()
        for i, t in enumerate([1, 2, 3, 4, 5, 6]):
            m.step(t, i, cache)
        sizes.append(cache_numbers(cache))
    return sizes


def main():
    return dict(dense=card(DENSE), gqa=card(GQA), moe=card(MOE), cache_sizes=gqa_cache_shrink())


if __name__ == "__main__":
    r = main()
    for name in ("dense", "gqa", "moe"):
        c = r[name]
        print(f"{name:6s} total {c['total'] / 1e9:5.2f}B  active {c['active'] / 1e9:5.2f}B  weights {c['weight_bytes'] / 2 ** 30:5.1f} GiB  "
              f"cache {c['kv_per_token'] / 2 ** 20:.3f} MiB per token")
    print("tiny model, 8 heads, cache numbers for 6 tokens: all heads", r["cache_sizes"][0], "| 2 key-value heads", r["cache_sizes"][1])
    d, g, m = r["dense"], r["gqa"], r["moe"]
    assert d["total"] == 6_738_415_616                                  # the familiar 6.7 billion
    assert d["kv_per_token"] == 4 * g["kv_per_token"]                   # 32 key-value heads down to 8
    assert m["total"] > 3.5 * m["active"] and 12e9 < m["active"] < 13.5e9   # memory of a large model, compute of a smaller one
    assert r["cache_sizes"][0] == 4 * r["cache_sizes"][1]
    print("lesson 6 ok")
