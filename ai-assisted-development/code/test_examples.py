"""Run every example in this folder. Each file ends with assert lines. A pass means the
direction of each claim in the lessons still holds. It does not check every quoted number.
Run: python3 ai-assisted-development/code/test_examples.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = [
    "lesson1_bottleneck.py", "lesson2_context_file.py", "lesson3_verification.py",
    "lesson4_permissions.py", "lesson5_scale.py", "lesson6_metrics.py",
]

failed = []
for name in FILES:
    result = subprocess.run([sys.executable, os.path.join(HERE, name)], capture_output=True, text=True, cwd=HERE)
    if result.returncode == 0:
        print(f"ok      {name}")
    else:
        failed.append(name)
        print(f"FAILED  {name}\n{result.stdout}{result.stderr}")
if failed:
    raise SystemExit(f"{len(failed)} example(s) failed: {', '.join(failed)}")
print(f"all {len(FILES)} examples pass")
