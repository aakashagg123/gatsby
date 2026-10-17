#!/usr/bin/env python3
"""A Stop hook that refuses to let the agent finish until a check passes.

Register it in .claude/settings.json under hooks.Stop. Claude Code sends the event as JSON on stdin.
The hook runs the command in GATE_COMMAND (default: pytest -x -q). If the check passes, it exits 0 and
the agent may stop. If it fails, it exits 2 and writes the reason to stderr; Claude Code then keeps the
agent working and gives it that message. It exits 0 at once when stop_hook_active is true, so a check that
cannot be fixed does not trap the agent in a loop. Claude Code also overrides a Stop hook after eight
consecutive blocks.
"""
import json
import os
import subprocess
import sys


def main():
    event = json.load(sys.stdin)
    if event.get("stop_hook_active"):
        return 0
    command = os.environ.get("GATE_COMMAND", "pytest -x -q")
    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=event.get("cwd") or None)
    if result.returncode == 0:
        return 0
    tail = "\n".join((result.stdout + result.stderr).strip().splitlines()[-15:])
    sys.stderr.write(f"The check `{command}` failed (exit {result.returncode}). Fix it before you finish.\n{tail}\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
