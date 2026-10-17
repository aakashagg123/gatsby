"""Lesson 3: LoRA. Freeze the model, train a small low-rank change, keep or drop it at will.

Run: python3 lesson3_lora.py
"""
from toy_lm import IDX, avg_loss, make_corpus, pretrained, train

Q, ANS = IDX["q"], IDX["answer"]
HELD = [(p, t) for p, t in make_corpus(40, seed=2) if p != Q]


def lora_params(d_in, d_out, rank):
    """A d_in by d_out matrix is changed by A (d_in by r) times B (r by d_out)."""
    return rank * (d_in + d_out)


def model_numbers(layers=32, d=4096, rank=16, total_params=6_738_415_616, matrices_per_layer=2):
    """Trainable parameters for LoRA on two d by d matrices per layer, and training memory for both methods.
    Mixed-precision Adam costs 16 bytes per trained parameter: 2 weight, 2 gradient, 12 optimizer state."""
    trainable = layers * matrices_per_layer * lora_params(d, d, rank)
    full_gib = total_params * 16 / 2 ** 30
    lora_gib = (total_params * 2 + trainable * 16) / 2 ** 30      # frozen 16-bit weights, plus state for the adapter only
    return dict(trainable=trainable, share=trainable / total_params, full_gib=full_gib, lora_gib=lora_gib)


def main():
    base = pretrained()
    tuned = base.copy()
    tuned.add_lora(rank=1)
    before = tuned.probs(Q)
    train(tuned, [(Q, ANS)] * 50, epochs=3, lr=0.2, lora_only=True)
    after_p = tuned.probs(Q)[ANS]
    frozen = base.E == tuned.E and base.U == tuned.U
    with_adapter = avg_loss(tuned, HELD)
    adapter = (tuned.A, tuned.B)
    tuned.A = tuned.B = None                                      # drop the adapter
    return dict(zero_start=max(abs(a - b) for a, b in zip(before, base.probs(Q))), p_answer=after_p, frozen=frozen,
                with_adapter=with_adapter, without=avg_loss(tuned, HELD), base=avg_loss(base, HELD),
                full_params=base.n_trainable(), lora_params=sum(len(r) for r in adapter[0]) + sum(len(r) for r in adapter[1]),
                nums=model_numbers(), small=model_numbers(layers=12, d=768, rank=8, total_params=124_439_808))


if __name__ == "__main__":
    r = main()
    print(f"adapter at the start changes the output by {r['zero_start']:.1e}")
    print(f"after training the adapter only: P(answer|q) {r['p_answer']:.3f}; base weights untouched: {r['frozen']}")
    print(f"general loss: base {r['base']:.3f}, with the adapter {r['with_adapter']:.3f}, adapter dropped {r['without']:.3f}")
    print(f"toy model: {r['full_params']} weights, adapter {r['lora_params']}")
    n = r["nums"]
    print(f"7B-class, rank 16 on two matrices per layer: {n['trainable']:,} trainable ({100 * n['share']:.2f}%); "
          f"training memory {n['full_gib']:.0f} GiB full vs {n['lora_gib']:.1f} GiB with the adapter")
    assert r["zero_start"] == 0.0                                  # B starts at zero, so the model starts unchanged
    assert r["p_answer"] > 0.5 and r["frozen"]
    assert r["without"] == r["base"]                               # dropping the adapter restores the base model exactly
    assert r["lora_params"] < r["full_params"] / 2
    assert 8_000_000 < n["trainable"] < 9_000_000 and n["share"] < 0.002
    assert n["full_gib"] > 100 and n["lora_gib"] < 20
    print("lesson 3 ok")
