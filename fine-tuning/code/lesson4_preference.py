"""Lesson 4: preference tuning. A reward model, best-of-n, the DPO step, and reward hacking.

Run: python3 lesson4_preference.py
"""
import math
import random

from lesson1_pipeline import dpo_step
from toy_lm import IDX, pretrained

Q, ANS, SORRY = IDX["q"], IDX["answer"], IDX["sorry"]


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def fit_reward_model(pairs, steps=300, lr=0.5):
    """Bradley-Terry: P(a beats b) = sigmoid(r(a) - r(b)), with r a weighted sum of two features. Plain gradient descent."""
    w = [0.0, 0.0]
    for _ in range(steps):
        g = [0.0, 0.0]
        for a, b, a_won in pairs:
            diff = [a[0] - b[0], a[1] - b[1]]
            p = sigmoid(w[0] * diff[0] + w[1] * diff[1])
            for i in range(2):
                g[i] += (p - (1.0 if a_won else 0.0)) * diff[i]
        w = [wi - lr * gi / len(pairs) for wi, gi in zip(w, g)]
    return w


def human_pairs(n, length_bias, seed=0):
    """Candidates have a true quality and a length. Annotators mostly prefer quality, and drift toward long answers."""
    rng = random.Random(seed)
    pairs = []
    for _ in range(n):
        a = (rng.gauss(0, 1), rng.gauss(0, 1))
        b = (rng.gauss(0, 1), rng.gauss(0, 1))
        p = sigmoid(2.0 * (a[0] - b[0]) + length_bias * (a[1] - b[1]))
        pairs.append((a, b, rng.random() < p))
    return pairs


def best_of_n(n, noise_scale, trials=1500, seed=0):
    """Pick the candidate the proxy reward likes best. The proxy is true quality plus a heavy-tailed error.
    Returns the average true quality of the pick, and the average proxy score."""
    rng = random.Random(seed)
    true_total = proxy_total = 0.0
    for _ in range(trials):
        best = None
        for _ in range(n):
            q = rng.gauss(0, 1)
            err = noise_scale * math.tan(math.pi * (rng.random() - 0.5))       # a heavy-tailed error
            if best is None or q + err > best[1]:
                best = (q, q + err)
        true_total += best[0]
        proxy_total += best[1]
    return true_total / trials, proxy_total / trials


def main():
    w_clean = fit_reward_model(human_pairs(2000, 0.0, seed=1))
    w_biased = fit_reward_model(human_pairs(2000, 1.5, seed=1))
    curve = {n: best_of_n(n, 0.3) for n in (1, 4, 16, 64, 512)}
    ref = pretrained()
    policy = ref.copy()
    margins = [dpo_step(policy, ref, Q, ANS, SORRY, lr=0.3, beta=1.0) for _ in range(40)]
    return dict(w_clean=w_clean, w_biased=w_biased, curve=curve, margins=margins,
                p=(ref.probs(Q)[ANS], policy.probs(Q)[ANS], policy.probs(Q)[SORRY]))


if __name__ == "__main__":
    r = main()
    print("reward model weights (quality, length): unbiased annotators", [round(x, 2) for x in r["w_clean"]],
          "| annotators who like long answers", [round(x, 2) for x in r["w_biased"]])
    print("best-of-n against a noisy reward model: n -> (true quality of the pick, proxy score)")
    for n, (t, p) in r["curve"].items():
        print(f"  n={n:4d}  true {t:5.2f}  proxy {p:5.2f}")
    print(f"DPO on a toy policy: margin {r['margins'][0]:.2f} -> {r['margins'][-1]:.2f}; "
          f"P(answer|q) {r['p'][0]:.3f} -> {r['p'][1]:.3f}, P(sorry|q) {r['p'][2]:.3f}")
    c = r["curve"]
    assert r["w_clean"][1] < 0.3 and r["w_biased"][1] > 2 * abs(r["w_clean"][1])          # the reward model learns the annotators' length bias
    assert c[16][0] > c[1][0] + 0.3 and c[512][0] < c[16][0]                               # true quality rises, then falls
    assert c[512][1] > c[16][1] > c[1][1]                                                  # while the proxy score keeps rising
    assert r["margins"][-1] > r["margins"][0] + 3                                           # the policy moves away from the reference
    assert r["p"][2] < 0.01 and r["p"][1] > 1.5 * r["p"][0]                                # the rejected word collapses, the preferred one rises less
    print("lesson 4 ok")
