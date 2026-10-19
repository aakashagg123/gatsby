"""At-least-once delivery with an idempotent consumer. A crash between processing and committing the offset
causes a redelivery. Run: python3 delivery_semantics.py"""


def consume(messages, crash_after_processing_at=None, idempotent=True):
    committed = 0
    processed = []                 # side effects, such as charges
    done_ids = set()
    crashed = False
    while committed < len(messages):
        msg_id, amount = messages[committed]
        if not (idempotent and msg_id in done_ids):
            processed.append(amount)
            done_ids.add(msg_id)
        if crash_after_processing_at == committed and not crashed:
            crashed = True          # the consumer restarts and re-reads from the last committed offset
            continue
        committed += 1
    return sum(processed)


if __name__ == "__main__":
    msgs = [("a", 10), ("b", 20), ("c", 30)]
    naive = consume(msgs, crash_after_processing_at=1, idempotent=False)
    safe = consume(msgs, crash_after_processing_at=1, idempotent=True)
    print(f"charges total with a crash at message b: not idempotent {naive}, idempotent {safe} (should be 60)")
    assert naive == 80 and safe == 60
    print("delivery semantics ok")
