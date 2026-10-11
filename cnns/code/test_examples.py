"""Run every example in this folder. Each file ends with assert lines. A pass means the
numbers and the direction of each claim in lessons 2, 3 and 5 still hold.
Run: python3 cnns/code/test_examples.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ["lesson2_convolution.py", "lesson3_receptive_field.py", "lesson5_patches.py"]

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
