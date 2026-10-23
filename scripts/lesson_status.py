#!/usr/bin/env python3
"""Evidence for the "Build" / "Use" claims in the phased tracks (harness, flowable).

A lesson table says what a lesson ships. This module checks it. For every lesson folder it
finds the code, runs what can run offline, parses the XML, and returns one state:

  verified    offline Python ran, exited 0, and contains assertions
  xml-valid   the lesson ships XML (BPMN, DMN, CMMN) and every file parses
  unasserted  offline Python exits 0 but asserts nothing
  service     the only Python needs an API key, a Flowable server or a third-party package
  untested    code exists (Java, properties) that no CI step runs
  spec        the lesson names code it does not ship
  failing     something that should run does not

Only `verified` and `xml-valid` earn a green check. build_site.py calls collect() on every
build and rewrites the tables from the result. tests/test_lesson_code.py calls the same
run_script(), so a green check and a green pytest mean the same thing.

Run:  python3 scripts/lesson_status.py       (prints a table of every lesson)
"""
import ast
import glob
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACKS = ("harness-engineering", "flowable")
SOURCE_URL = "https://github.com/aakashagg123/gatsby/blob/master/"

NETWORK_MODULES = ("urllib.request", "http.client", "requests", "httpx", "aiohttp")
XML_EXTS = (".xml", ".bpmn", ".dmn", ".cmmn")
OTHER_CODE_EXTS = (".java", ".properties")
# A script that imports a network module still counts as offline if it runs. It becomes a
# service script only when it fails with one of these.
SERVICE_ERRORS = re.compile(r"URLError|Connection (refused|reset)|Name or service|ConnectionError|"
                            r"urlopen error|API[_ ]?KEY|timed out", re.I)
SCRIPT_TIMEOUT = 60
OUT_TAIL_LINES = 14
OUT_MAX_CHARS = 1600

# state -> (glyph, label). Green only where a test or a parse backs it.
BADGES = {
    "verified": ("✅", "Tested"),
    "xml-valid": ("✅", "Valid XML"),
    "unasserted": ("🚧", "Runs, no checks"),
    "service": ("🚧", "Needs live service"),
    "untested": ("🚧", "Not CI-tested"),
    "spec": ("🚧", "Spec only"),
    "failing": ("❌", "Failing"),
    "concept": ("📖", "Read"),
}
GREEN = ("verified", "xml-valid")


def badge_text(state):
    glyph, label = BADGES[state]
    return f"{glyph} {label}"


_LOCAL = []


def local_modules():
    """Stems of every lesson script. A later lesson may import an earlier one's module."""
    if not _LOCAL:
        _LOCAL.append({os.path.splitext(os.path.basename(p))[0]
                       for t in TRACKS for p in glob.glob(os.path.join(ROOT, t, "phases", "*", "*", "code", "*.py"))})
    return _LOCAL[0]


def lesson_types():
    """{lesson rel path: 'Build'|'Use'|'Concept'} from the Type column of each phase README.
    A lesson with no table row (the harness track) counts as Build: every lesson ships code."""
    types = {}
    for track in TRACKS:
        for readme in sorted(glob.glob(os.path.join(ROOT, track, "phases", "*", "README.md"))):
            header = []
            with open(readme, encoding="utf-8") as f:
                for line in f:
                    if line.startswith("| #"):
                        header = [c.strip() for c in line.strip().strip("|").split("|")]
                        continue
                    m = re.search(r"\]\((\./[^)\s]+?)/docs/en\.md\)", line)
                    if m and "Type" in header:
                        cells = [c.strip() for c in line.strip().strip("|").split("|")]
                        rel = os.path.normpath(os.path.join(os.path.dirname(readme), m.group(1)))
                        types[os.path.relpath(rel, ROOT).replace(os.sep, "/")] = cells[header.index("Type")]
    return types


# ---- static facts about one script ---------------------------------------------------
def classify_script(path):
    """Return {'kind': 'offline'|'service', 'asserts': bool} from the script's own AST."""
    with open(path, encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src, filename=path)
    siblings = local_modules()
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            imported.add(node.module)
            imported.update(f"{node.module}.{a.name}" for a in node.names)
    third_party = any(
        m.split(".")[0] not in sys.stdlib_module_names and m.split(".")[0] not in siblings
        for m in imported)
    networked = any(m == n or m.startswith(n + ".") for m in imported for n in NETWORK_MODULES)
    asserts = os.path.basename(path).startswith("test_") or any(
        isinstance(n, ast.Assert) for n in ast.walk(tree))
    return {"kind": "service" if third_party else "offline", "networked": networked, "asserts": asserts}


def run_script(path, timeout=SCRIPT_TIMEOUT):
    """Run a lesson script from its own folder. Returns {'rc', 'out'}; out is the tail."""
    env = {k: v for k, v in os.environ.items() if "KEY" not in k and "TOKEN" not in k}
    try:
        r = subprocess.run([sys.executable, os.path.basename(path)], cwd=os.path.dirname(path),
                           capture_output=True, text=True, timeout=timeout, env=env)
        rc, out = r.returncode, (r.stdout + r.stderr)
    except subprocess.TimeoutExpired:
        rc, out = 124, f"timed out after {timeout}s"
    tail = "\n".join(out.strip().splitlines()[-OUT_TAIL_LINES:])
    return {"rc": rc, "out": tail[-OUT_MAX_CHARS:]}


def xml_ok(path):
    try:
        ET.parse(path)
        return True
    except ET.ParseError:
        return False


# ---- one lesson ----------------------------------------------------------------------
def lesson_dirs():
    for track in TRACKS:
        for d in sorted(glob.glob(os.path.join(ROOT, track, "phases", "*", "*", ""))):
            if os.path.exists(os.path.join(d, "docs", "en.md")):
                yield os.path.normpath(d)


def lesson_record(lesson_dir, run=True):
    rel = os.path.relpath(lesson_dir, ROOT).replace(os.sep, "/")
    scripts = []
    for p in sorted(glob.glob(os.path.join(lesson_dir, "code", "*.py"))):
        info = classify_script(p)
        entry = {"name": os.path.basename(p), "path": p, "rel": os.path.relpath(p, ROOT).replace(os.sep, "/"), **info}
        if run and info["kind"] == "offline":
            result = run_script(p)
            if info["networked"] and result["rc"] != 0 and SERVICE_ERRORS.search(result["out"]):
                entry["kind"] = "service"
            else:
                entry["run"] = result
        scripts.append(entry)
    xml_files = []
    for sub in ("code", "outputs"):
        for p in sorted(glob.glob(os.path.join(lesson_dir, sub, "*"))):
            if p.endswith(XML_EXTS):
                xml_files.append({"name": os.path.basename(p), "rel": os.path.relpath(p, ROOT).replace(os.sep, "/"),
                                  "ok": xml_ok(p)})
    other = [os.path.basename(p) for p in sorted(glob.glob(os.path.join(lesson_dir, "code", "*")))
             if p.endswith(OTHER_CODE_EXTS)]

    offline = [s for s in scripts if s["kind"] == "offline"]
    if offline:
        if run and any(s["run"]["rc"] != 0 for s in offline):
            state = "failing"
        elif any(s["asserts"] for s in offline):
            state = "verified"
        else:
            state = "unasserted"
    elif scripts:
        state = "service"
    elif xml_files:
        state = "xml-valid" if all(x["ok"] for x in xml_files) else "failing"
    elif other:
        state = "untested"
    else:
        state = "concept" if lesson_types().get(rel) == "Concept" else "spec"
    return {"rel": rel, "scripts": scripts, "xml": xml_files, "other": other, "state": state,
            "type": lesson_types().get(rel, "Build")}


def collect(run=True):
    """{lesson rel path: record}. Offline scripts run in parallel (they are independent)."""
    dirs = list(lesson_dirs())
    with ThreadPoolExecutor(max_workers=8) as pool:
        records = list(pool.map(lambda d: lesson_record(d, run=run), dirs))
    return {r["rel"]: r for r in records}


# ---- rendering into the copied markdown ---------------------------------------------
ROW_LINK = re.compile(r"\]\((\.[^)\s]*?/docs/en\.md)\)\s*✅")


def rewrite_tables(md, md_dir, records):
    """Swap the hand-typed ✅ after a lesson link for the evidence-backed badge.

    md_dir is the repo-relative folder of the markdown file, so a link like
    ./02-gateways/docs/en.md resolves to a lesson record. A row whose Type cell says Concept
    gets the read badge: it names no code, so there is nothing to test.
    """
    out = []
    for line in md.split("\n"):
        m = ROW_LINK.search(line) if line.startswith("|") else None
        if m:
            lesson_rel = os.path.normpath(os.path.join(md_dir, m.group(1))).replace(os.sep, "/")
            lesson_rel = lesson_rel[: -len("/docs/en.md")]
            rec = records.get(lesson_rel)
            if rec is not None:
                line = line.replace("✅", badge_text(rec["state"]), 1)
        out.append(line)
    return "\n".join(out)


def _fence(code):
    ticks = "```"
    while ticks in code:
        ticks += "`"
    return ticks


def lesson_panel(rec):
    """Markdown/HTML block for the top of a lesson page: badge, run command, source, output."""
    if rec["state"] == "concept":
        return ""
    if rec["state"] == "spec" and not rec["scripts"] and not rec["xml"]:
        return (f'<div class="lesson-code" data-state="spec"><span class="lesson-code-badge">'
                f'{badge_text("spec")}</span> This lesson has no committed code yet. '
                "The page describes the design; it ships nothing you can run.</div>\n")
    parts = [f'<div class="lesson-code" data-state="{rec["state"]}">',
             f'<p><span class="lesson-code-badge">{badge_text(rec["state"])}</span> '
             + {"verified": "Runs offline and checks itself. The build ran it.",
                "xml-valid": "Every XML file parses. A live Flowable engine still has to accept them.",
                "unasserted": "Runs offline, but the script asserts nothing.",
                "service": "Needs an API key, a Flowable server or a third-party package. CI does not run it.",
                "untested": "No CI step runs this code.",
                "failing": "Something here exited with an error. See the run below."}[rec["state"]] + "</p>"]
    for s in rec["scripts"]:
        cmd = f"python3 {s['rel']}"
        note = "" if s["kind"] == "offline" else " (needs a live service)"
        parts.append(
            f'<p class="lesson-code-row"><code>{cmd}</code> '
            f'<button type="button" class="Button" data-variant="outline" data-color="secondary" '
            f'data-size="sm" data-pill data-copy="{cmd}"><span class="ButtonInner">Copy command</span></button> '
            f'<a href="{SOURCE_URL}{s["rel"]}">View source ({s["name"]})</a>{note}</p>')
    for x in rec["xml"]:
        parts.append(f'<p class="lesson-code-row"><a href="{SOURCE_URL}{x["rel"]}">View {x["name"]}</a>'
                     f'{"" if x["ok"] else " (does not parse)"}</p>')
    for s in rec["scripts"]:
        with open(s["path"], encoding="utf-8") as f:
            code = f.read().rstrip("\n")
        fence = _fence(code)
        parts.append(f"\n<details><summary>Source: {s['name']}</summary>\n\n{fence}python\n{code}\n{fence}\n\n</details>")
        if "run" in s:
            r = s["run"]
            body = f"$ python3 {s['name']}\n{r['out']}\n[exit {r['rc']}]"
            parts.append(f"\n<details><summary>Verification run: {s['name']}</summary>\n\n"
                         f"{_fence(body)}text\n{body}\n{_fence(body)}\n\n</details>")
    parts.append("</div>\n")
    return "\n".join(parts)


def add_panel(md, rec):
    """Insert the panel right after the lesson's first H1."""
    lines = md.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            return "\n".join(lines[: i + 1] + ["", lesson_panel(rec)] + lines[i + 1:])
    return lesson_panel(rec) + "\n" + md


def main():
    recs = collect(run=True)
    width = max(len(r) for r in recs)
    for rel, r in recs.items():
        print(f"{rel[:width].ljust(width)}  {badge_text(r['state'])}")
    from collections import Counter
    print(Counter(r["state"] for r in recs.values()))


if __name__ == "__main__":
    main()
