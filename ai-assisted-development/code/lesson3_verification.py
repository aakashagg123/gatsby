"""Lesson 3: verification is the product. Run the Stop-hook gate against a passing and a failing check.

Run: python3 lesson3_verification.py
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "stop_gate.py")


def run_gate(command, stop_hook_active=False):
    event = json.dumps({"hook_event_name": "Stop", "session_id": "demo", "cwd": HERE, "stop_hook_active": stop_hook_active})
    r = subprocess.run([sys.executable, GATE], input=event, capture_output=True, text=True,
                       env=dict(os.environ, GATE_COMMAND=command))
    return r.returncode, r.stderr


def simulate_turn_loop(attempts_to_fix, cap=8):
    """The agent tries to stop. The gate blocks until the check passes or Claude Code's cap of eight consecutive
    blocks is reached. Returns (blocks, ended_with_passing_check)."""
    blocks = 0
    while True:
        passing = blocks >= attempts_to_fix
        if passing:
            return blocks, True
        if blocks >= cap:
            return blocks, False
        blocks += 1


def main():
    ok = run_gate(f"{sys.executable} -c 'print(1)'")
    bad = run_gate(f"{sys.executable} -c \"import sys; print('2 tests failed'); sys.exit(1)\"")
    reentrant = run_gate(f"{sys.executable} -c 'import sys; sys.exit(1)'", stop_hook_active=True)
    return dict(ok=ok, bad=bad, reentrant=reentrant, easy=simulate_turn_loop(2), stuck=simulate_turn_loop(20))


if __name__ == "__main__":
    r = main()
    print("passing check  -> exit", r["ok"][0])
    print("failing check  -> exit", r["bad"][0], "| message to the agent:", r["bad"][1].strip().splitlines()[0])
    print("re-entry (stop_hook_active) with a failing check -> exit", r["reentrant"][0])
    print("agent fixes it after 2 blocks:", r["easy"], "| never fixes it:", r["stuck"], "(blocks, check passing)")
    assert r["ok"][0] == 0 and r["bad"][0] == 2 and "2 tests failed" in r["bad"][1]
    assert r["reentrant"][0] == 0                       # the guard against loops
    assert r["easy"] == (2, True) and r["stuck"] == (8, False)
    print("lesson 3 ok")
