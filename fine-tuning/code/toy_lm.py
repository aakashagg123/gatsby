"""A tiny next-word model, trained by gradient descent, so fine-tuning effects can be measured.

The model is two tables. An embedding table E gives each word a vector. A shared output
table U turns a vector into one score per word. Because U is shared by every context,
changing it for one behaviour moves the others too. That is how forgetting happens.
Plain Python, no install. Gradients are written by hand.
"""
import math
import random

WORDS = ["the", "a", "cat", "dog", "sat", "ran", "on", "mat", "rug", "q", "answer", "sorry"]
IDX = {w: i for i, w in enumerate(WORDS)}
V = len(WORDS)


def softmax(xs):
    m = max(xs)
    e = [math.exp(x - m) for x in xs]
    s = sum(e)
    return [v / s for v in e]


class ToyLM:
    def __init__(self, d=6, seed=0):
        rng = random.Random(seed)
        self.d = d
        self.E = [[rng.gauss(0, 0.5) for _ in range(d)] for _ in range(V)]
        self.U = [[rng.gauss(0, 0.5) for _ in range(V)] for _ in range(d)]
        self.A = self.B = None                      # LoRA factors, set by add_lora

    def add_lora(self, rank, seed=1):
        """Add a low-rank change U + A B. Only A and B are trained afterwards."""
        rng = random.Random(seed)
        self.A = [[rng.gauss(0, 0.5) for _ in range(rank)] for _ in range(self.d)]
        self.B = [[0.0] * V for _ in range(rank)]    # zero at the start, so the model is unchanged

    def copy(self):
        m = ToyLM.__new__(ToyLM)
        m.d = self.d
        m.E = [r[:] for r in self.E]
        m.U = [r[:] for r in self.U]
        m.A = [r[:] for r in self.A] if self.A else None
        m.B = [r[:] for r in self.B] if self.B else None
        return m

    def logits(self, p):
        h = self.E[p]
        out = [sum(h[i] * self.U[i][v] for i in range(self.d)) for v in range(V)]
        if self.A:
            r = len(self.B)
            z = [sum(h[i] * self.A[i][k] for i in range(self.d)) for k in range(r)]
            out = [o + sum(z[k] * self.B[k][v] for k in range(r)) for v, o in enumerate(out)]
        return out

    def probs(self, p):
        return softmax(self.logits(p))

    def step(self, p, t, lr, lora_only=False, weight=1.0):
        """One gradient step on the pair (previous word p, next word t). Returns the loss."""
        h = self.E[p]
        pr = self.probs(p)
        g = [weight * (pr[v] - (1.0 if v == t else 0.0)) for v in range(V)]
        if self.A:
            r = len(self.B)
            z = [sum(h[i] * self.A[i][k] for i in range(self.d)) for k in range(r)]
            dz = [sum(self.B[k][v] * g[v] for v in range(V)) for k in range(r)]
            for k in range(r):
                for v in range(V):
                    self.B[k][v] -= lr * z[k] * g[v]
            dh_lora = [sum(self.A[i][k] * dz[k] for k in range(r)) for i in range(self.d)]
            for i in range(self.d):
                for k in range(r):
                    self.A[i][k] -= lr * h[i] * dz[k]
        else:
            dh_lora = [0.0] * self.d
        if not lora_only:
            dh = [sum(self.U[i][v] * g[v] for v in range(V)) + dh_lora[i] for i in range(self.d)]
            for i in range(self.d):
                for v in range(V):
                    self.U[i][v] -= lr * h[i] * g[v]
                self.E[p][i] -= lr * dh[i]
        return -math.log(max(pr[t], 1e-12))

    def n_trainable(self, lora_only=False):
        lora = (sum(len(r) for r in self.A) + sum(len(r) for r in self.B)) if self.A else 0
        full = sum(len(r) for r in self.E) + sum(len(r) for r in self.U)
        return lora if lora_only else full + lora


def pretrained(seed=0, d=2):
    """The base model every lesson starts from: trained on the grammar only, with no idea what to do after q."""
    model = ToyLM(d=d, seed=seed)
    train(model, make_corpus(60, seed=1), epochs=8, lr=0.2)
    return model


def make_corpus(n, seed=0):
    """Pairs (previous word, next word) from a small grammar: 'the cat sat on a mat'. The word q is followed by anything."""
    rng = random.Random(seed)
    pairs = []
    for _ in range(n):
        det = rng.choice(["the", "a"])
        noun = rng.choice(["cat", "dog"])
        verb = rng.choice(["sat", "ran"])
        det2 = rng.choice(["the", "a"])
        obj = rng.choice(["mat", "rug"])
        s = [det, noun, verb, "on", det2, obj]
        pairs += list(zip(s, s[1:]))
        pairs.append(("q", rng.choice(WORDS)))                 # before fine-tuning, q is followed by anything
    return [(IDX[a], IDX[b]) for a, b in pairs]


def avg_loss(model, pairs):
    return sum(-math.log(max(model.probs(p)[t], 1e-12)) for p, t in pairs) / len(pairs)


def train(model, pairs, epochs, lr, seed=0, lora_only=False):
    rng = random.Random(seed)
    for _ in range(epochs):
        order = pairs[:]
        rng.shuffle(order)
        for p, t in order:
            model.step(p, t, lr, lora_only)
