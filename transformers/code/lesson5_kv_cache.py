"""Lesson 5: generating text. Recompute everything, or keep the keys and values.

Run: python3 lesson5_kv_cache.py
"""
from lesson6_variants import DENSE, GQA, card
from mini_transformer import Config, OPS, Transformer, argmax, cache_numbers, reset_ops


def generate_without_cache(model, prompt, steps):
    tokens = list(prompt)
    for _ in range(steps):
        tokens.append(argmax(model.forward(tokens)[-1]))
    return tokens


def generate_with_cache(model, prompt, steps):
    cache, tokens = model.new_cache(), list(prompt)
    logits = None
    for pos, t in enumerate(prompt):                      # prefill: every prompt token goes through once
        logits = model.step(t, pos, cache)
    for i in range(steps):                                # decode: one new token per step
        tokens.append(argmax(logits))
        if i < steps - 1:                                 # the last token needs no step of its own
            logits = model.step(tokens[-1], len(tokens) - 1, cache)
    return tokens, cache


def kv_cache_bytes(layers, kv_heads, d_head, tokens, bytes_per=2):
    return 2 * layers * kv_heads * d_head * tokens * bytes_per


def weight_intensity(tokens_per_pass, bytes_per_weight=2):
    """FLOPs per byte of weights read, when one pass handles this many tokens. Each weight does 2 FLOPs per token."""
    return 2 * tokens_per_pass / bytes_per_weight


def concurrent_sequences(gpu_gib, spec, tokens):
    """How many full-length sequences fit beside the weights. Ignores activations and runtime overhead."""
    c = card(spec)
    weights_gib = c["weight_bytes"] / 2 ** 30
    cache_gib = c["kv_per_token"] * tokens / 2 ** 30
    return int((gpu_gib - weights_gib) // cache_gib), weights_gib, cache_gib


def main():
    cfg = Config(d_model=16, n_heads=4, n_layers=2, vocab=32, max_len=64)
    model = Transformer(cfg, seed=7)
    prompt, steps = [3, 7, 1, 9, 4, 2], 10
    reset_ops()
    slow = generate_without_cache(model, prompt, steps)
    slow_kv = OPS["kv"]
    reset_ops()
    fast, cache = generate_with_cache(model, prompt, steps)
    fast_kv = OPS["kv"]
    n = len(prompt) + steps
    return dict(same=slow == fast, slow_kv=slow_kv, fast_kv=fast_kv, numbers=cache_numbers(cache),
                formula=2 * cfg.n_layers * cfg.d_model * (n - 1),
                gpt2=kv_cache_bytes(12, 12, 64, 1024), big=kv_cache_bytes(32, 32, 128, 8192),
                big_gqa=kv_cache_bytes(32, 8, 128, 8192), tokens=n,
                fit_dense=concurrent_sequences(80, DENSE, 8192), fit_gqa=concurrent_sequences(80, GQA, 8192))


if __name__ == "__main__":
    r = main()
    print(f"same tokens with and without the cache: {r['same']}")
    print(f"key and value multiply-adds: {r['slow_kv']:,} without the cache, {r['fast_kv']:,} with it ({r['slow_kv'] / r['fast_kv']:.1f}x fewer)")
    print(f"numbers held in the cache: {r['numbers']} (formula 2 x layers x d_model x tokens = {r['formula']})")
    mib = lambda b: b / 2 ** 20
    print(f"weights read once per pass: {weight_intensity(1):.0f} FLOP per byte in decode, {weight_intensity(512):.0f} in a 512-token prefill")
    for name, key in (("dense", "fit_dense"), ("grouped-query", "fit_gqa")):
        fit, w, c = r[key]
        print(f"80 GiB, {name} card: weights {w:.1f} GiB, {c:.1f} GiB per 8,192-token sequence -> {fit} sequences at once")
    print(f"GPT-2 small, 1,024 tokens, 16-bit: {mib(r['gpt2']):.0f} MiB per sequence")
    print(f"7B-class (32 layers, 32 heads of 128), 8,192 tokens, 16-bit: {mib(r['big']) / 1024:.1f} GiB; with 8 key-value heads: {mib(r['big_gqa']) / 1024:.1f} GiB")
    assert weight_intensity(1) == 1 and weight_intensity(512) == 512
    assert r["fit_dense"][0] == 16 and r["fit_gqa"][0] > 3 * r["fit_dense"][0]
    assert r["same"]
    assert r["numbers"] == r["formula"]
    assert r["slow_kv"] > 3 * r["fast_kv"]
    assert r["gpt2"] == 37_748_736 and r["big"] == 4 * 2 ** 30 and r["big_gqa"] == 2 ** 30
    print("lesson 5 ok")
