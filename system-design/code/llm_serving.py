"""LLM serving arithmetic: how many long conversations fit beside the weights, how fast one stream decodes, and why continuous
batching beats static batching. The model shape is illustrative. Run: python3 llm_serving.py"""
import random

GIB = 1024 ** 3


def concurrency(hbm_gib, weights_gib, tokens, layers, kv_heads, head_dim, bytes_per=2):
    kv_per_token = 2 * layers * kv_heads * head_dim * bytes_per
    per_request = tokens * kv_per_token
    return int((hbm_gib - weights_gib) * GIB // per_request), per_request / GIB


def decode_tokens_per_second(bandwidth_gb_s, weights_gib, batch=1):
    """Decode reads every weight once per step, whatever the batch size, so a bigger batch shares that cost."""
    steps_per_s = bandwidth_gb_s * 1e9 / (weights_gib * GIB)
    return steps_per_s * batch


def static_steps(lengths, slots):
    batches = [lengths[i:i + slots] for i in range(0, len(lengths), slots)]
    return sum(max(b) for b in batches)                  # each batch runs until its longest request finishes


def continuous_steps(lengths, slots):
    pending, running, steps = list(lengths), [], 0
    while pending or running:
        while pending and len(running) < slots:
            running.append(pending.pop(0))
        steps += 1
        running = [r - 1 for r in running if r - 1 > 0]
    return steps


if __name__ == "__main__":
    dense, per_dense = concurrency(80, 12.6, 8192, layers=32, kv_heads=32, head_dim=128)
    gqa, per_gqa = concurrency(80, 11.1, 8192, layers=32, kv_heads=8, head_dim=128)
    print(f"80 GiB accelerator, 8,192-token conversations: {dense} fit with 32 KV heads ({per_dense:.1f} GiB each), {gqa} with 8 KV heads ({per_gqa:.1f} GiB each)")
    one = decode_tokens_per_second(2000, 12.6)
    batch = decode_tokens_per_second(2000, 12.6, batch=16)
    print(f"2 TB/s of memory bandwidth and 12.6 GiB of weights: about {one:.0f} tokens/s for one stream, about {batch:.0f} tokens/s across a batch of 16")
    rng = random.Random(3)
    lengths = [rng.randint(20, 400) for _ in range(64)]
    s, c = static_steps(lengths, 8), continuous_steps(lengths, 8)
    print(f"64 requests of 20 to 400 tokens on 8 slots: static batching {s:,} steps, continuous batching {c:,} steps ({s / c:.2f}x faster)")
    assert (dense, gqa) == (16, 68) and round(per_dense, 1) == 4.0
    assert c < s and s / c > 1.3
    print("llm serving ok")
