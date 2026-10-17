"""Lesson 6: deciding, costing and checking a fine-tune. Break-even volume, distillation cost and a release gate.

All prices and volumes are invented for the arithmetic. They are not quotes. Run: python3 lesson6_decide.py
"""

PRICE = dict(big_in=3.00, big_out=15.00, small_in=0.25, small_out=1.25)      # dollars per million tokens (invented)


def per_request(in_tokens, out_tokens, p_in, p_out):
    return (in_tokens * p_in + out_tokens * p_out) / 1_000_000


def breakeven(prompt_big=1800, prompt_small=150, out_tokens=200, serve_premium=1.5, fixed=2000.0, price=PRICE):
    """A large model with a long few-shot prompt, against a fine-tuned small model with a short prompt.
    serve_premium multiplies the small model's price, for hosting a custom model. fixed is the one-off cost."""
    big = per_request(prompt_big, out_tokens, price["big_in"], price["big_out"])
    small = per_request(prompt_small, out_tokens, price["small_in"] * serve_premium, price["small_out"] * serve_premium)
    saving = big - small
    return dict(big=big, small=small, saving=saving, requests=fixed / saving if saving > 0 else float("inf"))


def distillation_cost(examples=20_000, in_tokens=400, out_tokens=250, price=PRICE):
    """Cost to have the large model write the training answers."""
    return examples * per_request(in_tokens, out_tokens, price["big_in"], price["big_out"])


def release_gate(candidate, baseline, general_before, general_after, min_gain=0.02, max_general_drop=0.01):
    """Ship only if the target task improved enough and general ability did not slip."""
    ok_gain = candidate - baseline >= min_gain
    ok_general = general_before - general_after <= max_general_drop
    return ok_gain and ok_general, ok_gain, ok_general


def main():
    be = breakeven()
    return dict(be=be, be_cheap_fixed=breakeven(fixed=500.0), be_short_prompt=breakeven(prompt_big=300),
                distill=distillation_cost(), gates=[release_gate(0.91, 0.84, 0.80, 0.795),
                                                     release_gate(0.91, 0.84, 0.80, 0.74),
                                                     release_gate(0.85, 0.84, 0.80, 0.80)])


if __name__ == "__main__":
    r = main()
    be = r["be"]
    print(f"per request: large + long prompt ${be['big'] * 1000:.2f} per 1,000, fine-tuned small ${be['small'] * 1000:.2f} per 1,000")
    print(f"saving ${be['saving'] * 1000:.2f} per 1,000 requests; break-even for a $2,000 project: {be['requests']:,.0f} requests")
    print(f"  with a $500 project: {r['be_cheap_fixed']['requests']:,.0f}; if the large model needs only a 300-token prompt: {r['be_short_prompt']['requests']:,.0f}")
    print(f"distilling 20,000 examples from the large model: ${r['distill']:,.2f}")
    print("release gates (gain, general ability):", [(g[1], g[2]) for g in r["gates"]])
    assert round(be["big"] * 1000, 2) == 8.40 and be["saving"] > 0
    assert 200_000 < be["requests"] < 300_000
    assert r["be_short_prompt"]["requests"] > 2 * be["requests"]                 # a short prompt on the big model more than doubles the break-even
    assert r["be_cheap_fixed"]["requests"] < be["requests"] / 3
    assert [g[0] for g in r["gates"]] == [True, False, False]
    print("lesson 6 ok")
