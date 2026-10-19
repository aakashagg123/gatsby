"""A saga: local steps with compensations. If a step fails, the completed steps are undone in reverse order.
Run: python3 saga.py"""


def run_saga(steps, fail_at=None):
    """steps: list of (name, do, undo). Returns (log, succeeded)."""
    log, done = [], []
    for i, (name, do, undo) in enumerate(steps):
        if fail_at == name:
            log.append(f"FAILED {name}")
            for n, u in reversed(done):
                u()
                log.append(f"compensate {n}")
            return log, False
        do()
        log.append(f"ok {name}")
        done.append((name, undo))
    return log, True


if __name__ == "__main__":
    state = {"flight": False, "hotel": False, "card": False}
    steps = [
        ("reserve flight", lambda: state.update(flight=True), lambda: state.update(flight=False)),
        ("reserve hotel", lambda: state.update(hotel=True), lambda: state.update(hotel=False)),
        ("charge card", lambda: state.update(card=True), lambda: state.update(card=False)),
    ]
    log, ok = run_saga(steps, fail_at="charge card")
    print(" -> ".join(log))
    print("final state:", state)
    assert not ok and log == ["ok reserve flight", "ok reserve hotel", "FAILED charge card", "compensate reserve hotel", "compensate reserve flight"]
    assert not any(state.values())
    state2 = {"flight": False, "hotel": False, "card": False}
    steps2 = [("reserve flight", lambda: state2.update(flight=True), lambda: None), ("charge card", lambda: state2.update(card=True), lambda: None)]
    _, ok2 = run_saga(steps2)
    assert ok2 and state2["card"]
    print("saga ok")
