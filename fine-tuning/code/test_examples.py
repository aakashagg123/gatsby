"""Run every example in this folder. Each file ends with assert lines. A pass means the
direction of each claim in the lessons still holds. It does not check every quoted number.
Run: python3 fine-tuning/code/test_examples.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = [
    "lesson1_pipeline.py", "lesson2_sft.py", "lesson3_lora.py",
    "lesson4_preference.py", "lesson5_dataset.py", "lesson6_decide.py",
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
