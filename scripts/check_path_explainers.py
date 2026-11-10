#!/usr/bin/env python3
"""Check the learning-path explainers against the path data, so they cannot drift.

Each explainer in gen_learning_paths.STORIES follows one learner through one path. Its stage
names, hours, lesson counts and links must match PATHS in scripts/gen_learning_paths.py, which
also generates the path pages. Importing that module only computes; it writes nothing.

For every explainer that exists, this checks:
  - a heading "## <n> · Stage <k>: <name>" for each path stage, in order, with the path's name
  - under it, the line "*Path stage <k> · <hours> · <n> lessons*", using the path's hours() and count
  - a "**Do this:**" line in each path-stage block
  - every lesson link inside a path-stage block is a lesson of that path stage
  - the path's total hours and the weeks line "At <h> hours a week, about <w> weeks."
  - the whole-journey figure (the page's last figure file) shows every stage's hours, the total and the weeks
Explainers not written yet are skipped. Exit code 1 on any mismatch.

Run:  python3 scripts/check_path_explainers.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import gen_learning_paths as G  # noqa: E402

HEAD = re.compile(r"^## (\d+) · Stage (\d+): (.+)$")
DATA = re.compile(r"^\*Path stage (\d+) · (.+?) · (\d+) lessons\*$")
LINK = re.compile(r"\]\((\.\./|\./)([^)#\s]+?)\.md(?:#[^)]*)?\)")


def stage_targets(s):
    """Repo-relative paths (without .md) of every lesson a path stage lists."""
    out = set()
    for it in s["items"]:
        if it.kind == "t":
            order = G.flat_lessons(it.kw["track"])
            out |= {f"{it.kw['track']}/{order[i - 1]}" for i in it.kw["ids"]}
        elif it.kind == "c":
            out |= {f"content/{it.kw['folder']}/{k}" for k in it.kw["ids"]}
        elif it.kind == "h":
            out.add(f"harness-engineering/phases/{G.HARNESS[it.kw['phase']]}/README")
        elif it.kind == "f":
            out.add("flowable/README")
    return out


def norm(prefix, target):
    """Turn a link written in explainers/ into a repo-relative path without .md."""
    return os.path.normpath(os.path.join("explainers", prefix, target)).replace(os.sep, "/")


def check(slug, p):
    errors = []
    path = os.path.join(ROOT, "explainers", f"{slug}.md")
    lines = open(path, encoding="utf-8").read().split("\n")
    stages = p["stages"]
    found = []
    blocks = []
    for i, line in enumerate(lines):
        m = HEAD.match(line)
        if m:
            blocks.append((i, int(m.group(2)), m.group(3)))
    ends = [b[0] for b in blocks[1:]] + [None]
    for (start, k, name), end in zip(blocks, ends):
        if end is None:
            end = next((j for j in range(start + 1, len(lines)) if lines[j].startswith("## ")), len(lines))
        block = lines[start:end]
        found.append(k)
        if not 1 <= k <= len(stages):
            errors.append(f"{slug}: heading names stage {k}, but the path has {len(stages)} stages")
            continue
        s = stages[k - 1]
        if name != s["name"]:
            errors.append(f"{slug}: stage {k} is named \"{name}\", the path says \"{s['name']}\"")
        data = next((DATA.match(b) for b in block if DATA.match(b)), None)
        want_h, want_n = G.hours(G.stage_minutes(s)), G.stage_lessons(s)
        if not data:
            errors.append(f"{slug}: stage {k} has no line \"*Path stage {k} · {want_h} · {want_n} lessons*\"")
        else:
            if int(data.group(1)) != k:
                errors.append(f"{slug}: stage {k} data line says stage {data.group(1)}")
            if data.group(2) != want_h:
                errors.append(f"{slug}: stage {k} says {data.group(2)}, the path says {want_h}")
            if int(data.group(3)) != want_n:
                errors.append(f"{slug}: stage {k} says {data.group(3)} lessons, the path says {want_n}")
        if not any(b.startswith("**Do this:**") for b in block):
            errors.append(f"{slug}: stage {k} has no \"**Do this:**\" line")
        allowed = stage_targets(s)
        for b in block:
            for prefix, target in LINK.findall(b):
                t = norm(prefix, target)
                if t not in allowed:
                    errors.append(f"{slug}: stage {k} links {t}.md, which is not a lesson of path stage {k}")
    if found != list(range(1, len(stages) + 1)):
        errors.append(f"{slug}: path stages appear as {found}, expected {list(range(1, len(stages) + 1))}")
    text = "\n".join(lines)
    total = G.minutes_of(stages)
    if G.hours(total) not in text:
        errors.append(f"{slug}: the path total ({G.hours(total)}) is not stated")
    weeks = f"At {p['example_hpw']} hours a week, about {G.weeks_at(total, p['example_hpw'])} weeks."
    if weeks not in text:
        errors.append(f"{slug}: missing or wrong weeks line; expected \"{weeks}\"")
    # The whole-journey figure repeats the hours, so a figure not regenerated after a path change is caught too.
    last = text.count("```mermaid") - 1
    fig_path = os.path.join(ROOT, "diagrams", "explainers", f"{slug}-{last}.html")
    if not os.path.exists(fig_path):
        errors.append(f"{slug}: no whole-journey figure at {os.path.relpath(fig_path, ROOT)}")
    else:
        fig = open(fig_path, encoding="utf-8").read()
        want = [f"{G.hours(G.stage_minutes(s))}." for s in stages] + [f"{G.hours(total)} in all", weeks]
        for w in want:
            if w not in fig:
                errors.append(f"{slug}: whole-journey figure lacks \"{w}\"; run scripts/gen_explainer_figures.py")
    return errors


def main():
    errors, checked = [], 0
    for p in G.PATHS:
        slug = G.STORIES.get(p["slug"])
        if not slug or not os.path.exists(os.path.join(ROOT, "explainers", f"{slug}.md")):
            continue
        checked += 1
        errors += check(slug, p)
    for e in errors:
        print("FAIL", e)
    if errors:
        sys.exit(1)
    print(f"ok — {checked} learning-path explainer(s) match the path data")


if __name__ == "__main__":
    main()
