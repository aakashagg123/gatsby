"""Lesson 2: attention from scratch. Queries, keys, values, the scale and the mask.

Run: python3 lesson2_attention.py
"""
import math
import random

from mini_transformer import matmul, softmax, transpose


def attention(q, k, v, scale=True, causal=True):
    """One head. Returns the output rows and the weight matrix."""
    dk = len(q[0])
    scores = matmul(q, transpose(k), "attn")
    weights = []
    for i, row in enumerate(scores):
        row = [(s / math.sqrt(dk) if scale else s) if (not causal or j <= i) else float("-inf") for j, s in enumerate(row)]
        weights.append(softmax(row))
    return matmul(weights, v, "attn"), weights


def previous_token_head(tokens, vocab, strength=12.0):
    """A head with hand-set weights that copies the previous token. Trained models learn heads like it."""
    n = len(tokens)
    pos = lambda i: [1.0 if j == i else 0.0 for j in range(n)]
    tok = lambda t: [1.0 if j == t else 0.0 for j in range(vocab)]
    # Each query asks for "the position before me". Each key says "I am position i". Each value is its token.
    # attention() divides scores by sqrt(d_k), so the query is multiplied by sqrt(d_k) to give the intended strength.
    q = [[strength * math.sqrt(n) * x for x in (pos(i - 1) if i > 0 else pos(i))] for i in range(n)]
    k = [pos(i) for i in range(n)]
    v = [tok(t) for t in tokens]
    return attention(q, k, v, scale=True)


def softmax_sharpness(dk, scale, trials=200, keys=8, seed=1):
    """Average largest weight when query and keys are random with unit variance."""
    rng = random.Random(seed)
    total = 0.0
    for _ in range(trials):
        q = [[rng.gauss(0, 1) for _ in range(dk)]]
        k = [[rng.gauss(0, 1) for _ in range(dk)] for _ in range(keys)]
        _, w = attention(q, k, k, scale=scale, causal=False)
        total += max(w[0])
    return total / trials


def dot_variance(dk, trials=2000, seed=2):
    rng = random.Random(seed)
    xs = [sum(rng.gauss(0, 1) * rng.gauss(0, 1) for _ in range(dk)) for _ in range(trials)]
    mean = sum(xs) / trials
    return sum((x - mean) ** 2 for x in xs) / trials


def main():
    words = ["the", "cat", "sat", "on", "the", "mat"]
    vocab = sorted(set(words))
    ids = [vocab.index(w) for w in words]
    out, w = previous_token_head(ids, len(vocab))
    copied = [vocab[max(range(len(vocab)), key=r.__getitem__)] for r in out]
    last_row = w[-1]
    return dict(words=words, copied=copied, weights=w, last_row=last_row,
                var16=dot_variance(16), var256=dot_variance(256),
                sharp_unscaled=softmax_sharpness(256, False), sharp_scaled=softmax_sharpness(256, True))


if __name__ == "__main__":
    r = main()
    print("tokens:        ", r["words"])
    print("head output:   ", r["copied"], "(the token each position attends to)")
    print("last row of weights:", [round(x, 3) for x in r["last_row"]])
    print(f"variance of a dot product: {r['var16']:.1f} at d_k=16, {r['var256']:.1f} at d_k=256")
    print(f"average largest softmax weight over 8 keys at d_k=256: unscaled {r['sharp_unscaled']:.2f}, scaled {r['sharp_scaled']:.2f}")
    assert r["copied"][1:] == r["words"][:-1]                      # every position after the first reads the token before it
    assert all(abs(sum(row) - 1) < 1e-9 for row in r["weights"])   # each row of weights sums to 1
    assert all(r["weights"][i][j] == 0.0 for i in range(6) for j in range(i + 1, 6))   # nothing looks forward
    assert 12 < r["var16"] < 20 and 220 < r["var256"] < 290        # variance grows with d_k
    assert r["sharp_unscaled"] > 0.9 and r["sharp_scaled"] < 0.6   # without the scale, softmax saturates
    print("lesson 2 ok")
