"""Lesson 4: batching, memory and precision. Will it fit, and what do the number formats trade?

Part A is a training-memory calculator. Part B shows what float16 and bfloat16 do to numbers.

Run: python3 lesson4_memory.py
"""
import math
import struct

GB = 1e9      # decimal gigabytes, as in the papers that quote these figures

# Bytes of "model state" per parameter, for each training setup. Each part is listed.
SCHEMES = {
    "fp32 + SGD":            {"weights": 4, "gradients": 4},
    "fp32 + SGD momentum":   {"weights": 4, "gradients": 4, "momentum": 4},
    "fp32 + Adam":           {"weights": 4, "gradients": 4, "adam_m": 4, "adam_v": 4},
    # Mixed precision keeps fp16 copies for the forward and backward pass, and fp32 "master" copies for the update.
    "mixed precision + Adam": {"weights fp16": 2, "gradients fp16": 2, "master weights fp32": 4, "adam_m": 4, "adam_v": 4},
}


def state_bytes(params, scheme):
    return params * sum(SCHEMES[scheme].values())


def inference_bytes(params, bytes_per_weight):
    return params * bytes_per_weight


def activation_bytes(batch, layers, tokens, width, bytes_per_number):
    """A simplified, invented model: each layer keeps one (tokens, width) output per sample for the backward pass.
    Real networks keep several tensors per layer, so this is a lower bound."""
    return batch * layers * tokens * width * bytes_per_number


def largest_batch(budget, states, per_sample_activation):
    spare = budget - states
    return max(0, int(spare // per_sample_activation))


# ---- number formats --------------------------------------------------------------------
def round_fp32(x):
    return struct.unpack("<f", struct.pack("<f", x))[0]


def round_fp16(x):
    try:
        return struct.unpack("<e", struct.pack("<e", x))[0]
    except OverflowError:
        return math.copysign(math.inf, x)


def round_bf16(x):
    """bfloat16 is the top 16 bits of a float32: the same 8 exponent bits, only 7 fraction bits."""
    bits = struct.unpack("<I", struct.pack("<f", x))[0]
    bits += 0x7FFF + ((bits >> 16) & 1)            # round to nearest, ties to even
    return struct.unpack("<f", struct.pack("<I", bits & 0xFFFF0000))[0]


def accumulate(start, step, times, rounder):
    total = start
    for _ in range(times):
        total = rounder(total + step)
    return total


def main():
    # Part A: memory.
    params = 1.5e9
    states = {name: state_bytes(params, name) for name in SCHEMES}
    weights_fp16 = inference_bytes(params, 2)
    p7 = 7e9
    infer7 = inference_bytes(p7, 2)
    train7 = state_bytes(p7, "mixed precision + Adam")

    layers, tokens, width = 32, 2048, 4096
    per_sample = activation_bytes(1, layers, tokens, width, 2)
    device = 80 * GB                                        # an invented device with 80 GB
    small_model = 1.0e9
    small_states = state_bytes(small_model, "mixed precision + Adam")
    batch_fit = largest_batch(device, small_states, per_sample)
    batch_fit_after_halving = largest_batch(device, small_states, per_sample / 2)

    # Part B: formats.
    eps = {"float32": 2.0 ** -23, "float16": 2.0 ** -10, "bfloat16": 2.0 ** -7}
    fp16_max = round_fp16(65504.0)
    fp16_over = round_fp16(70000.0)
    bf16_70000 = round_bf16(70000.0)
    tiny = 1e-8
    fp16_tiny, bf16_tiny = round_fp16(tiny), round_bf16(tiny)
    scale = 1024.0
    scaled_back = round_fp16(tiny * scale) / scale          # loss scaling: multiply, store, divide
    stall16 = accumulate(1.0, 1e-4, 10000, round_fp16)
    stall32 = accumulate(1.0, 1e-4, 10000, round_fp32)
    return dict(states=states, weights_fp16=weights_fp16, infer7=infer7, train7=train7, per_sample=per_sample,
                batch_fit=batch_fit, batch_fit_half=batch_fit_after_halving, small_states=small_states,
                eps=eps, fp16_max=fp16_max, fp16_over=fp16_over, bf16_70000=bf16_70000, fp16_tiny=fp16_tiny,
                bf16_tiny=bf16_tiny, scaled_back=scaled_back, stall16=stall16, stall32=stall32,
                one_plus_fp16=round_fp16(1.0 + 2.0 ** -11), one_plus_bf16=round_bf16(1.0 + 2.0 ** -8))


if __name__ == "__main__":
    r = main()
    print("model state for a 1.5 billion parameter model (decimal GB):")
    for name, b in r["states"].items():
        print(f"  {name:24s} {b / GB:6.1f} GB  ({b / 1.5e9:.0f} bytes per parameter)")
    print(f"weights alone at float16: {r['weights_fp16'] / GB:.1f} GB")
    print(f"7 billion parameters: inference at float16 {r['infer7'] / GB:.0f} GB; "
          f"training state with mixed precision + Adam {r['train7'] / GB:.0f} GB, before any activations")
    print(f"activations per sample (invented 32-layer model, 2,048 tokens, width 4,096, float16): {r['per_sample'] / GB:.2f} GB")
    print(f"1B-parameter model on an 80 GB device: state {r['small_states'] / GB:.0f} GB, largest batch {r['batch_fit']}; "
          f"with half the activation memory per sample: {r['batch_fit_half']}")
    print("machine epsilon (smallest step near 1.0):", {k: f"{v:.2e}" for k, v in r["eps"].items()})
    print(f"float16 holds 65504 as {r['fp16_max']:.0f}, but 70000 becomes {r['fp16_over']}; bfloat16 keeps 70000 as {r['bf16_70000']:.0f}")
    print(f"1e-8 becomes {r['fp16_tiny']} in float16 and {r['bf16_tiny']:.3e} in bfloat16")
    print(f"loss scaling: 1e-8 x 1024, stored in float16, divided back = {r['scaled_back']:.4e}")
    print(f"adding 0.0001 ten thousand times to 1.0: float16 gives {r['stall16']}, float32 gives {r['stall32']:.4f}")
    s = r["states"]
    assert s["fp32 + Adam"] == 24e9 and s["mixed precision + Adam"] == 24e9      # 16 bytes per parameter, 1.5e9 parameters
    assert s["fp32 + SGD"] == 12e9 and s["fp32 + SGD momentum"] == 18e9
    assert r["weights_fp16"] == 3e9
    assert r["infer7"] == 14e9 and r["train7"] == 112e9
    assert r["per_sample"] == 32 * 2048 * 4096 * 2
    assert r["batch_fit"] == int((80e9 - 16e9) // r["per_sample"]) and r["batch_fit_half"] > 2 * r["batch_fit"] - 1
    assert r["eps"]["bfloat16"] > r["eps"]["float16"] > r["eps"]["float32"]
    assert r["fp16_max"] == 65504.0 and math.isinf(r["fp16_over"]) and 69000 < r["bf16_70000"] < 71000
    assert r["fp16_tiny"] == 0.0 and 0.9e-8 < r["bf16_tiny"] < 1.1e-8
    assert abs(r["scaled_back"] - 1e-8) / 1e-8 < 0.01
    assert r["stall16"] == 1.0 and abs(r["stall32"] - 2.0) < 0.01              # float16 never moves; float32 reaches about 2
    assert r["one_plus_fp16"] == 1.0 and r["one_plus_bf16"] == 1.0
    print("lesson 4 ok")
