"""A small decoder-only transformer in plain Python, with a counter for multiply-adds.

The weights are random, so the model says nothing useful. It exists so that every claim
about shapes, parameters, cost and the key-value cache can be counted and checked.
It uses lists of lists. A real library does the same arithmetic on tensors, in compiled code.
"""
import math
import random
from collections import Counter

OPS = Counter()          # multiply-adds, by kind: proj, kv, attn, mlp, unembed


def reset_ops():
    OPS.clear()


def matmul(a, b, tag="proj"):
    n, k, m = len(a), len(b), len(b[0])
    OPS[tag] += n * k * m
    cols = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in cols] for row in a]


def transpose(a):
    return [list(r) for r in zip(*a)]


def add(a, b):
    return [[x + y for x, y in zip(r, s)] for r, s in zip(a, b)]


def softmax(row):
    m = max(row)
    e = [math.exp(v - m) for v in row]
    s = sum(e)
    return [v / s for v in e]


def layer_norm(x, eps=1e-5):
    out = []
    for row in x:
        mean = sum(row) / len(row)
        var = sum((v - mean) ** 2 for v in row) / len(row)
        out.append([(v - mean) / math.sqrt(var + eps) for v in row])
    return out


def gelu(x):
    return [[0.5 * v * (1 + math.tanh(math.sqrt(2 / math.pi) * (v + 0.044715 * v ** 3))) for v in row] for row in x]


def sinusoidal(pos, d):
    """The position vector from the original transformer paper."""
    v = []
    for i in range(d // 2):
        angle = pos / (10000 ** (2 * i / d))
        v += [math.sin(angle), math.cos(angle)]
    return v


def count_params(d, layers, vocab, max_len, d_ff=None, bias=True, layernorm=True, tied=True):
    """Parameters of a decoder-only transformer, by formula."""
    d_ff = d_ff or 4 * d
    attn = 4 * d * d + (4 * d if bias else 0)                 # query, key, value and output matrices
    mlp = 2 * d * d_ff + ((d_ff + d) if bias else 0)
    norms = 4 * d if layernorm else 0                         # two norms per block, gain and bias each
    block = attn + mlp + norms
    emb = vocab * d + max_len * d
    final = 2 * d if layernorm else 0
    return emb + layers * block + final + (0 if tied else vocab * d)


class Config:
    def __init__(self, d_model=16, n_heads=4, n_layers=2, vocab=32, max_len=64,
                 d_ff=None, n_kv_heads=None, pos="learned"):
        assert d_model % n_heads == 0
        self.d_model, self.n_heads, self.n_layers = d_model, n_heads, n_layers
        self.vocab, self.max_len, self.pos = vocab, max_len, pos
        self.d_head = d_model // n_heads
        self.d_ff = d_ff or 4 * d_model
        self.n_kv_heads = n_kv_heads or n_heads
        assert n_heads % self.n_kv_heads == 0


def _rand(rng, rows, cols, scale):
    return [[rng.gauss(0, scale) for _ in range(cols)] for _ in range(rows)]


class Transformer:
    def __init__(self, cfg, seed=0):
        self.cfg = cfg
        rng = random.Random(seed)
        d, kvd = cfg.d_model, cfg.n_kv_heads * cfg.d_head
        s = 1 / math.sqrt(d)
        self.tok = _rand(rng, cfg.vocab, d, 1.0)
        self.pos = _rand(rng, cfg.max_len, d, 1.0) if cfg.pos == "learned" else None
        self.layers = [dict(wq=_rand(rng, d, d, s), wk=_rand(rng, d, kvd, s), wv=_rand(rng, d, kvd, s),
                            wo=_rand(rng, d, d, s), w1=_rand(rng, d, cfg.d_ff, s),
                            w2=_rand(rng, cfg.d_ff, d, 1 / math.sqrt(cfg.d_ff))) for _ in range(cfg.n_layers)]
        self.trace = None            # set to a list to record attention weights

    def n_params(self):
        n = len(self.tok) * len(self.tok[0]) + (len(self.pos) * len(self.pos[0]) if self.pos else 0)
        for L in self.layers:
            n += sum(len(m) * len(m[0]) for m in L.values())
        return n

    def position_rows(self, start, n):
        c = self.cfg
        if c.pos == "learned":
            return self.pos[start:start + n]
        if c.pos == "sinusoidal":
            return [sinusoidal(p, c.d_model) for p in range(start, start + n)]
        return [[0.0] * c.d_model for _ in range(n)]

    def attend(self, q, k, v, causal=True):
        """q has nq rows, k and v have nk rows. A query may see keys up to its own position."""
        c = self.cfg
        dk, group = c.d_head, c.n_heads // c.n_kv_heads
        shift = len(k) - len(q)
        out = [[] for _ in q]
        for head in range(c.n_heads):
            kv = head // group
            qh = [r[head * dk:(head + 1) * dk] for r in q]
            kh = [r[kv * dk:(kv + 1) * dk] for r in k]
            vh = [r[kv * dk:(kv + 1) * dk] for r in v]
            scores = matmul(qh, transpose(kh), "attn")
            probs = []
            for i, row in enumerate(scores):
                row = [s / math.sqrt(dk) if (not causal or j <= i + shift) else float("-inf")
                       for j, s in enumerate(row)]
                probs.append(softmax(row))
            if self.trace is not None:
                self.trace.append(probs)
            for i, r in enumerate(matmul(probs, vh, "attn")):
                out[i].extend(r)
        return out

    def block(self, x, L, kv_cache=None, causal=True):
        h = layer_norm(x)
        q = matmul(h, L["wq"])
        k = matmul(h, L["wk"], "kv")
        v = matmul(h, L["wv"], "kv")
        if kv_cache is not None:
            kv_cache["k"].extend(k)
            kv_cache["v"].extend(v)
            k, v = kv_cache["k"], kv_cache["v"]
        x = add(x, matmul(self.attend(q, k, v, causal), L["wo"]))
        h = layer_norm(x)
        return add(x, matmul(gelu(matmul(h, L["w1"], "mlp")), L["w2"], "mlp"))

    def logits(self, x):
        return matmul(layer_norm(x), transpose(self.tok), "unembed")

    def forward(self, tokens, causal=True):
        x = add([self.tok[t] for t in tokens], self.position_rows(0, len(tokens)))
        for L in self.layers:
            x = self.block(x, L, None, causal)
        return self.logits(x)

    def new_cache(self):
        return [dict(k=[], v=[]) for _ in self.layers]

    def step(self, token, pos, cache):
        """Process one new token, reusing the cached keys and values of earlier tokens."""
        x = add([self.tok[token]], self.position_rows(pos, 1))
        for L, kv in zip(self.layers, cache):
            x = self.block(x, L, kv)
        return self.logits(x)[0]


def cache_numbers(cache):
    return sum(len(r) * len(r[0]) for kv in cache for r in (kv["k"], kv["v"]) if r)


def argmax(row):
    return max(range(len(row)), key=row.__getitem__)
