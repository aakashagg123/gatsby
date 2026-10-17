"""Lesson 1: from base model to assistant. Three stages on a toy model, and what each one changes.

Run: python3 lesson1_pipeline.py
"""
from toy_lm import IDX, ToyLM, avg_loss, make_corpus, pretrained, train

Q, ANS, SORRY = IDX["q"], IDX["answer"], IDX["sorry"]
HELD = [(p, t) for p, t in make_corpus(40, seed=2) if p != Q]


def p_answer(model):
    return model.probs(Q)[ANS]


def dpo_step(policy, ref, p, win, lose, lr, beta=1.0):
    """One direct preference step. Raise the preferred word and lower the other, scaled by how wrong the margin is."""
    import math
    lw, ll = math.log(policy.probs(p)[win]), math.log(policy.probs(p)[lose])
    rw, rl = math.log(ref.probs(p)[win]), math.log(ref.probs(p)[lose])
    margin = beta * ((lw - rw) - (ll - rl))
    c = beta / (1 + math.exp(margin))                  # beta * sigmoid(-margin)
    policy.step(p, win, lr, weight=c)
    policy.step(p, lose, lr, weight=-c)
    return margin


def main():
    base = pretrained()
    stages = {"pretrained": base}
    sft = base.copy()
    train(sft, [(Q, ANS)] * 20, epochs=3, lr=0.2)
    stages["after SFT"] = sft
    tuned = sft.copy()                                     # preference step: for q, "answer" beats "sorry"
    ref = sft.copy()
    margins = [dpo_step(tuned, ref, Q, ANS, SORRY, lr=0.3) for _ in range(30)]
    stages["after preference tuning"] = tuned
    return dict(stages={k: (p_answer(m), m.probs(Q)[SORRY], avg_loss(m, HELD)) for k, m in stages.items()}, margins=margins)


if __name__ == "__main__":
    r = main()
    print(f"{'stage':26s} P(answer|q)  P(sorry|q)  loss on general text")
    for k, (pa, ps, gl) in r["stages"].items():
        print(f"{k:26s} {pa:10.3f}  {ps:10.3f}  {gl:10.3f}")
    s = r["stages"]
    assert s["pretrained"][0] < 0.2 < 0.9 < s["after SFT"][0]               # SFT teaches the behaviour
    assert s["after preference tuning"][1] <= s["after SFT"][1]             # preference tuning pushes the rejected word down
    assert s["after SFT"][2] > s["pretrained"][2] + 0.5                     # narrow tuning spills over: general text gets worse
    assert r["margins"][-1] > r["margins"][0]                               # the policy moves away from the reference
    print("lesson 1 ok")
