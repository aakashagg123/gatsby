"""Run every example in this folder. Each file ends with assert lines. A pass means the
direction of each claim in the lessons still holds. It does not check every quoted number.
pgvector_demo.py runs against a real Postgres when one is reachable, and skips otherwise.
Run: python3 rag-vector-databases/code/test_examples.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = [
    "decide.py", "mini_rag.py", "embeddings_demo.py", "ann_demo.py",
    "chunking_demo.py", "graph_demo.py", "pgvector_demo.py",
]

failed = []
for name in FILES:
    result = subprocess.run([sys.executable, os.path.join(HERE, name)], capture_output=True, text=True, cwd=HERE)
    if result.returncode == 0:
        last = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else ""
        print(f"ok      {name}" + ("   (skipped: no Postgres)" if "skipped" in last else ""))
    else:
        failed.append(name)
        print(f"FAILED  {name}\n{result.stdout}{result.stderr}")
if failed:
    raise SystemExit(f"{len(failed)} example(s) failed: {', '.join(failed)}")
print(f"all {len(FILES)} examples pass")
