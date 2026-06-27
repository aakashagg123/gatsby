# Quantization Formats: INT8, INT4, FP8, AWQ, GPTQ — and When It Hurts

*Part of [01 · Inference Internals](./README.md)*

## TL;DR

Quantization stores numbers in fewer bits to shrink the model's memory footprint and
move less data per [decode](./prefill-vs-decode.md) step — buying lower cost, more
[KV/batch headroom](./kv-cache-management.md), and often lower latency. The format
(**INT8, FP8, INT4**) sets the precision/range ceiling; the method (**AWQ, GPTQ**, and
others) decides how cleverly you map full-precision weights into that budget. 8-bit is
usually near-lossless; 4-bit is viable *with a good method*; below that, quality
typically collapses. Always confirm with [evals](../04-evals-observability/evals.md) —
degradation is task-specific and invisible to the eye.

## What "quantize" actually means

A full-precision weight is FP16/BF16 (16 bits). Quantization maps ranges of those
values onto a smaller set of levels:

- **Integer (INT8, INT4):** pick a scale (and maybe zero-point) per tensor/channel/
  group, then round weights to integers. Fewer bits = coarser grid = more rounding
  error.
- **Float (FP8):** keep a floating layout (e.g. **E4M3** = 4 exponent + 3 mantissa
  bits, or **E5M2**). Floats preserve **dynamic range** far better than integers at the
  same bit count, which matters for the large outlier values that show up in
  activations.

What you quantize matters as much as the bit count:
- **Weight-only** (most common for INT4) — weights are small precision, math often
  still done in FP16. Great memory win, modest compute win, lower quality risk.
- **Weight + activation** (e.g. W8A8 INT8, or FP8 both) — also speeds up the matmuls,
  but activations have **outliers** that are hard to quantize and are the usual source
  of quality loss.
- **KV-cache quantization** — store the [KV cache](./kv-cache-management.md) in FP8/INT8
  to roughly double or quadruple concurrency; a separate, valuable lever.

## The formats

| Format | Bits | Keeps dynamic range? | Typical use | Quality |
| --- | --- | --- | --- | --- |
| **INT8** | 8 | Moderate | W8A8 serving, broad HW support | Usually near-lossless |
| **FP8 (E4M3/E5M2)** | 8 | **Yes** (float) | Modern GPUs (Hopper+), weights+activations | Near-lossless, range-robust |
| **INT4** | 4 | Low | Weight-only, memory-constrained serving | Good *with AWQ/GPTQ*, risky naive |
| **INT3/INT2** | ≤3 | Very low | Research / extreme compression | Usually large degradation |

FP8 vs INT8 at the same 8 bits: FP8's exponent gives it the **range** to absorb
activation outliers, so it often quantizes activations more gracefully — handy on
hardware with native FP8 support. INT8 has the widest software/hardware support.

## The methods (how to hit 4-bit without wrecking quality)

Naive round-to-nearest at 4-bit loses too much. Smarter post-training quantization
(PTQ) methods use a small **calibration** dataset to minimize error:

- **GPTQ** — quantizes weights one column/group at a time, using approximate
  **second-order (Hessian) information** to compensate remaining weights for the error
  introduced, minimizing layer-wise output error. Strong 4-bit weight-only results;
  calibration-set sensitive.
- **AWQ (Activation-aware Weight Quantization)** — observes that a *small fraction* of
  weight channels (those multiplied by large activations) dominate quality. It scales
  to **protect those salient channels** and quantizes the rest aggressively. Robust at
  4-bit, less sensitive to the calibration set, fast.
- **Others you'll meet:** SmoothQuant (shifts activation outliers into weights so W8A8
  works), GGUF k-quants (llama.cpp's mixed-bit CPU/edge formats), bitsandbytes
  (NF4/INT8 for QLoRA-style training and easy loading), and SpinQuant/QuaRot
  (rotations that make 4-bit activations tractable).

Rule of thumb: **the format sets the ceiling, the method determines how close to it
you get.** "INT4" with AWQ/GPTQ ≫ "INT4" with naive rounding.

## When quantization *hurts*

Degradation is not uniform — it concentrates in specific places:

- **Lower bits, more risk** — INT8/FP8 usually safe; INT4 needs a good method; ≤3-bit
  usually hurts.
- **Activation quantization** is riskier than weight-only because of outliers.
- **Long-context / KV quantization** can accumulate small per-token errors over a long
  sequence.
- **Hard, precision-sensitive tasks** suffer most: math/arithmetic, code, strict
  [structured output / JSON](../02-reliable-outputs/structured-output.md), low-resource
  languages, and long multi-step reasoning. Easy classification/summarization barely
  notices.
- **Small models** have less redundancy to spare and degrade more than large ones at
  the same bit-width.
- **Calibration mismatch** — calibrating GPTQ/AWQ on data unlike production traffic
  bakes in error where you'll actually use the model.

Because it's task-specific, you cannot judge quantization by spot-checking a few
prompts. You need a [task-representative eval set](../04-evals-observability/evals.md),
ideally including adversarial and format-strict cases, run at each candidate bit-width.

## Tradeoffs

| Choice | Buys | Costs |
| --- | --- | --- |
| INT8 / FP8 | ~2× memory, near-lossless | Minimal |
| INT4 (AWQ/GPTQ) | ~4× memory, big $ win | Real but bounded quality risk |
| KV-cache FP8/INT8 | More concurrency/throughput | Small long-context risk |
| Weight+activation | Faster matmuls too | Activation-outlier degradation |

## Practitioner checklist

- [ ] Start at INT8/FP8; only go INT4 if evals hold.
- [ ] Use AWQ or GPTQ (not naive rounding) for 4-bit.
- [ ] Calibrate on data that looks like production traffic.
- [ ] Run task-representative + adversarial evals at each bit-width.
- [ ] Pay special attention to math, code, and strict-JSON tasks.
- [ ] Consider KV-cache quantization as a separate concurrency lever.
- [ ] Confirm your hardware actually accelerates the chosen format (e.g. FP8 on Hopper+).

## Related lessons

- [Speculative decoding vs. quantization vs. distillation](./speculative-quantization-distillation.md)
- [KV cache management](./kv-cache-management.md)
- [Prefill vs. decode](./prefill-vs-decode.md)
- [Evals](../04-evals-observability/evals.md)
- [Structured output](../02-reliable-outputs/structured-output.md)
