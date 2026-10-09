"""Run every example in this folder. Each file ends with assert lines, so a pass means the
claims in the lessons still hold. Run: python3 machine-learning/code/test_examples.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = [
    "lesson1_rules_vs_learning.py", "lesson2_leakage.py", "lesson3_gradient_descent.py",
    "lesson4_overfitting.py", "lesson5_metrics.py", "lesson6_model_families.py", "lesson7_drift.py",
]

failed = []
for name in FILES:
    run = subprocess.run([sys.executable, os.path.join(HERE, name)], cwd=HERE, capture_output=True, text=True)
    status = "ok" if run.returncode == 0 and run.stdout.strip().endswith("ok") else "FAILED"
    print(f"{status:7s} {name}")
    if status != "ok":
        failed.append(name)
        print(run.stdout[-800:], run.stderr[-800:])
if failed:
    sys.exit(1)
print(f"all {len(FILES)} examples pass")
