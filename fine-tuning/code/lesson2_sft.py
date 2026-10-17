"""Lesson 2: supervised fine-tuning. How much data, how fast, and what it costs the rest of the model.

Run: python3 lesson2_sft.py
"""
import random

from toy_lm import IDX, avg_loss, make_corpus, pretrained, train

Q, ANS, SORRY = IDX["q"], IDX["answer"], IDX["sorry"]
CORPUS = make_corpus(60, seed=1)
HELD = [(p, t) for p, t in make_corpus(40, seed=2) if p != Q]
REPLAY = [(p, t) for p, t in CORPUS if p != Q]


def run(model, data, epochs=1, lr=0.2):
    m = model.copy()
    train(m, data, epochs=epochs, lr=lr)
    return m.probs(Q)[ANS], avg_loss(m, HELD), m


def main():
    base = pretrained()
    out = dict(base=avg_loss(base, HELD))
    out["examples"] = {n: run(base, [(Q, ANS)] * n)[:2] for n in (0, 5, 20, 50)}
    out["lr"] = {lr: run(base, [(Q, ANS)] * 20, epochs=3, lr=lr)[:2] for lr in (0.05, 0.2, 0.5, 1.0)}
    out["replay"] = {k: run(base, [(Q, ANS)] * 20 + REPLAY[:k], epochs=3)[:2] for k in (0, 60, 240)}
    rng = random.Random(3)
    noisy = [(Q, ANS if rng.random() < 0.8 else SORRY) for _ in range(50)]
    _, _, m = run(base, noisy, epochs=5)
    out["noise"] = dict(wrong=sum(1 for _, t in noisy if t == SORRY), p_answer=m.probs(Q)[ANS], p_sorry=m.probs(Q)[SORRY],
                        base_sorry=base.probs(Q)[SORRY])
    return out


if __name__ == "__main__":
    r = main()
    print(f"general loss before any tuning: {r['base']:.3f}")
    print("examples (1 epoch, lr 0.2):  ", {n: (round(a, 3), round(b, 3)) for n, (a, b) in r["examples"].items()}, "(P(answer|q), general loss)")
    print("learning rate (20 examples, 3 epochs):", {lr: (round(a, 3), round(b, 3)) for lr, (a, b) in r["lr"].items()})
    print("general pairs mixed in (20 examples, 3 epochs):", {k: (round(a, 3), round(b, 3)) for k, (a, b) in r["replay"].items()})
    n = r["noise"]
    print(f"{n['wrong']} of 50 labels wrong: P(answer|q) {n['p_answer']:.3f}, P(sorry|q) {n['p_sorry']:.3f} (before tuning {n['base_sorry']:.3f})")
    ex, lr, rp = r["examples"], r["lr"], r["replay"]
    assert ex[5][0] < 0.2 and ex[50][0] > 0.9                         # a handful of examples does little; enough does a lot
    assert ex[50][1] > r["base"] + 0.5                                # and the rest of the model pays for it
    assert lr[0.05][1] < lr[0.2][1] < lr[0.5][1] < lr[1.0][1]         # a higher learning rate forgets more
    assert rp[0][1] > 2 * rp[240][1] and rp[240][0] > 0.9             # general data mixed in keeps the rest and the behaviour
    assert n["p_sorry"] > 4 * n["base_sorry"]                         # wrong labels teach the wrong behaviour
    print("lesson 2 ok")
