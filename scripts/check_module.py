#!/usr/bin/env python3
"""Score a flat track (or all of them) against CONTENT_FRAMEWORK.md.

Measurable rules only: readability, required sections, review stamps, unsourced
claims, undefined acronyms, and the recap self-test. Judgement rules (accuracy,
worked-example quality) stay with the reviewer and the independent fact-check.

Run:
  python3 scripts/check_module.py ai-agents          # one track, full detail
  python3 scripts/check_module.py --all              # summary table, all flat tracks
  python3 scripts/check_module.py --all --table      # markdown rows for the tracker
  python3 scripts/check_module.py ai-agents --json   # machine-readable
  python3 scripts/check_module.py ai-agents --strict # exit 1 on any FAIL

Exit code is 0 unless --strict is given and a FAIL is found.
"""
import argparse
import datetime
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build_graph  # noqa: E402
import glossary_data  # noqa: E402

FLAT_TRACKS = sorted(build_graph.FLAT_TRACKS)

# Readability thresholds (module averages). Keep in sync with CONTENT_FRAMEWORK.md.
AVG_SENT = (20, 25)     # pass <= 20, warn < 25, fail >= 25
LONG_PCT = (12, 20)     # % of sentences over 30 words
FLESCH = (50, 45)       # pass >= 50, warn >= 45, fail < 45

# Review cadence in months by volatility.
CADENCE = {"fast": 3, "medium": 6, "stable": 12}
# Default volatility for a track that has no stamp yet.
VOLATILITY = {
    "agentic-ai": "fast", "ai-agents": "fast", "agentic-workflows": "fast",
    "tool-calling": "fast", "api-integrations": "fast", "llms": "fast",
    "generative-ai": "fast", "prompt-engineering": "fast",
    "context-engineering": "fast", "memory-and-context": "fast",
    "rag-vector-databases": "medium", "evaluation-and-observability": "fast",
    "ai-security-and-guardrails": "fast", "cost-optimization": "fast",
    "knowledge-graphs": "medium", "system-design": "stable", "access-control": "medium",
    "learning-paths": "medium", "machine-learning": "medium",
    "technical-product-management": "medium", "technical-product-sense": "stable",
    "product-sense": "medium", "first-principles": "stable",
}

STAMP_RE = re.compile(r"^\*Last reviewed: (\d{4})-(\d{2}) · Volatility: (fast|medium|stable)\*\s*$", re.M)
CLAIM_RES = [
    re.compile(r"\b\d+(?:\.\d+)?\s?%"),
    re.compile(r"\bClaude\s+(?:Opus|Sonnet|Haiku|Fable|Mythos)?\s*\d"),
    re.compile(r"\bGPT-?\d"), re.compile(r"\bGemini\s*\d"), re.compile(r"\bo[134]-"),
    re.compile(r"\b20(?:2[3-9]|3\d)\b"), re.compile(r"\bet al\."),
]
COMMON_ACRONYMS = {
    "AI", "PM", "PMS", "API", "APIS", "PRD", "PRDS", "UI", "UX", "CEO", "CTO", "CPO", "CFO",
    "FAQ", "SLA", "SLAS", "KPI", "KPIS", "OKR", "OKRS", "ROI", "URL", "HTTP", "JSON", "SQL",
    "CSV", "PDF", "USD", "EU", "US", "UK", "IT", "QA", "PR", "ID", "IDS", "HR", "SEO", "B2B",
    "B2C", "SAAS", "CRM", "ERP", "RFC", "RFCS", "MVP", "TL", "DR", "TLDR", "CI", "CD", "OS",
}


def glossary_terms():
    terms = set()
    for e in glossary_data.GLOSSARY:
        terms.add(e["t"].lower())
        for a in e.get("aliases", []):
            terms.add(a.lower())
        m = re.findall(r"\(([A-Za-z0-9/ ]+)\)", e["t"])
        terms.update(x.lower() for x in m)
    return terms


def syllables(word):
    w = word.lower()
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and n > 1:
        n -= 1
    return max(n, 1)


def paragraphs(text):
    """Prose paragraphs: fenced code, tables, headings, HTML and images removed.
    Each paragraph or list item is one unit; bullets and '>' markers are stripped."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"<details>.*?</details>", "", text, flags=re.S)
    out, cur = [], []
    def flush():
        if cur:
            out.append(" ".join(cur))
            cur.clear()
    for raw in text.split("\n"):
        line = raw.strip()
        if not line or line.startswith(("|", "#", "<", "!", "---")):
            flush()
            continue
        line = re.sub(r"^>\s?", "", line).strip()
        starts_item = bool(re.match(r"^(?:[-*]|\d+\.)\s+", line))
        line = re.sub(r"^(?:[-*]|\d+\.)\s+(?:\[[ x]\]\s*)?", "", line)
        if starts_item:
            flush()
        if line:
            cur.append(line)
    flush()
    return out


def clean(p):
    p = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", p)
    return re.sub(r"[*`_]", "", p)


def sentences(p):
    p = re.sub(r"\b(e\.g|i\.e|et al|vs|etc|approx|Fig)\.", lambda m: m.group(0).replace(".", "~"), p)
    return [s.replace("~", ".") for s in re.split(r"(?<=[.!?])\s+", p) if len(s.split()) > 3]


def readability(text):
    words = sents = syl = longs = 0
    for p in paragraphs(text):
        p = clean(p)
        ss = sentences(p)
        ws = re.findall(r"[A-Za-z']+", p)
        words += len(ws)
        sents += len(ss)
        longs += sum(1 for s in ss if len(s.split()) > 30)
        syl += sum(syllables(w) for w in ws)
    if not sents:
        return dict(words=0, avg=0, long=0, flesch=100)
    avg = words / sents
    fre = 206.835 - 1.015 * avg - 84.6 * (syl / max(words, 1))
    return dict(words=words, avg=round(avg, 1), long=round(100 * longs / sents), flesch=round(fre))


def band(value, limits, higher_is_better=False):
    a, b = limits
    if higher_is_better:
        return "PASS" if value >= a else "WARN" if value >= b else "FAIL"
    return "PASS" if value <= a else "WARN" if value < b else "FAIL"


def has_heading(text, pattern):
    return bool(re.search(r"^#{2,4} .*(?:%s)" % pattern, text, flags=re.M | re.I))


def lesson_checks(path, text, terms):
    stamp = STAMP_RE.search(text)
    onboarded = bool(stamp)
    sections = {
        "tldr": has_heading(text, "TL;DR"),
        "callout": "🎯" in text,
        "failure_modes": has_heading(text, "failure modes"),
        "checklist": has_heading(text, "checklist"),
        "related": has_heading(text, "related"),
        "mental_model": has_heading(text, "mental model|at a glance|the model") or "```mermaid" in text,
        "tradeoffs": has_heading(text, "tradeoff"),
        "worked_example": has_heading(text, "worked|example|mini-case|case") or bool(re.search(r"\*\*📦|\bWorked example\b", text)),
        "under_the_hood": has_heading(text, "under the hood"),
    }
    core = ["tldr", "callout", "failure_modes", "checklist", "related"]
    new = ["mental_model", "worked_example", "under_the_hood"]
    missing_core = [k for k in core if not sections[k]]
    missing_new = [k for k in new if not sections[k]]
    has_sources = has_heading(text, "sources")
    flagged = 0
    for p in paragraphs(text):
        if any(r.search(p) for r in CLAIM_RES) and "](http" not in p and not has_sources:
            flagged += 1
    body = " ".join(clean(p) for p in paragraphs(text))
    defined = set(m.upper() for m in re.findall(r"\(([A-Z][A-Za-z0-9]{1,6}s?)\)", body))
    undefined = sorted({
        a for a in re.findall(r"\b[A-Z]{2,6}s?\b", body)
        if a.upper() not in COMMON_ACRONYMS and a.upper() not in defined
        and a.lower() not in terms and a.rstrip("s").lower() not in terms
    })
    return dict(
        file=os.path.relpath(path, ROOT), onboarded=onboarded,
        stamp=(stamp.group(1) + "-" + stamp.group(2), stamp.group(3)) if stamp else None,
        missing_core=missing_core, missing_new=missing_new,
        unsourced_claims=flagged, undefined_acronyms=undefined, **readability(text),
    )


def overdue(stamp, today):
    y, m = map(int, stamp[0].split("-"))
    months = (today.year - y) * 12 + (today.month - m)
    return months > CADENCE[stamp[1]]


def check_track(track, terms, today):
    files = sorted(glob.glob(os.path.join(ROOT, track, "*.md")))
    lessons = [f for f in files if os.path.basename(f) not in ("README.md", "recap.md")]
    res = [lesson_checks(f, open(f, encoding="utf-8").read(), terms) for f in lessons]
    all_text = "\n".join(open(f, encoding="utf-8").read() for f in lessons)
    rd = readability(all_text)
    recap_p = os.path.join(ROOT, track, "recap.md")
    readme_p = os.path.join(ROOT, track, "README.md")
    recap = open(recap_p, encoding="utf-8").read() if os.path.exists(recap_p) else ""
    readme = open(readme_p, encoding="utf-8").read() if os.path.exists(readme_p) else ""
    onboarded = bool(res) and all(r["onboarded"] for r in res)
    stamped = [r for r in res if r["stamp"]]
    issues = []  # (severity, message)
    for name, val, lim, hib in (("Avg sentence length", rd["avg"], AVG_SENT, False),
                                ("Sentences over 30 words (%)", rd["long"], LONG_PCT, False),
                                ("Flesch reading ease", rd["flesch"], FLESCH, True)):
        issues.append((band(val, lim, hib), f"{name}: {val}"))
    test_yourself = "test yourself" in recap.lower()
    depth_map = bool(re.search(r"where the depth lives", readme, re.I))
    sev_new = "FAIL" if onboarded else "WARN"
    if not test_yourself:
        issues.append((sev_new, "recap has no 'Test yourself' section"))
    if not depth_map:
        issues.append((sev_new, "README has no 'Where the depth lives' map"))
    for r in res:
        for k in r["missing_core"]:
            issues.append(("FAIL", f"{os.path.basename(r['file'])}: missing {k}"))
        for k in r["missing_new"]:
            issues.append((sev_new if r["onboarded"] else "WARN", f"{os.path.basename(r['file'])}: missing {k}"))
        if r["stamp"] and overdue(r["stamp"], today):
            issues.append(("FAIL", f"{os.path.basename(r['file'])}: review overdue ({r['stamp'][0]}, {r['stamp'][1]})"))
        if r["unsourced_claims"]:
            issues.append(("WARN", f"{os.path.basename(r['file'])}: {r['unsourced_claims']} paragraph(s) with versioned/numeric claims and no source"))
    if not stamped:
        issues.append(("WARN", f"no review stamps yet (default volatility: {VOLATILITY.get(track, 'medium')})"))
    verdict = "FAIL" if any(s == "FAIL" for s, _ in issues) else "WARN" if any(s == "WARN" for s, _ in issues) else "PASS"
    return dict(track=track, lessons=len(res), verdict=verdict, onboarded=onboarded,
                words=rd["words"], avg=rd["avg"], long=rd["long"], flesch=rd["flesch"],
                test_yourself=test_yourself, depth_map=depth_map, issues=issues, per_lesson=res)


def print_detail(r):
    print(f"{r['track']}: {r['verdict']}  ({r['lessons']} lessons, {r['words']} words, "
          f"avg sentence {r['avg']}, >30w {r['long']}%, Flesch {r['flesch']})")
    for sev, msg in r["issues"]:
        print(f"  [{sev}] {msg}")
    worst = sorted(r["per_lesson"], key=lambda x: -x["avg"])[:3]
    print("  hardest lessons: " + "; ".join(f"{os.path.basename(x['file'])} (avg {x['avg']}, >30w {x['long']}%)" for x in worst))
    acr = sorted({a for x in r["per_lesson"] for a in x["undefined_acronyms"]})
    if acr:
        print("  acronyms not defined in-lesson or in the glossary: " + ", ".join(acr[:20]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("track", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--table", action="store_true")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    if not args.track and not args.all:
        ap.error("give a track name or --all")
    tracks = FLAT_TRACKS if args.all else [args.track]
    for t in tracks:
        if not os.path.isdir(os.path.join(ROOT, t)):
            ap.error(f"unknown track: {t}")
    terms = glossary_terms()
    today = datetime.date.today()
    results = [check_track(t, terms, today) for t in tracks]
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif args.table:
        print("| Track | Lessons | Avg sentence | >30w % | Flesch | Test yourself | Verdict |")
        print("| --- | --- | --- | --- | --- | --- | --- |")
        for r in results:
            print(f"| `{r['track']}` | {r['lessons']} | {r['avg']} | {r['long']} | {r['flesch']} | "
                  f"{'yes' if r['test_yourself'] else 'no'} | {r['verdict']} |")
    elif args.all:
        print(f"{'track':32s}{'les':>4}{'avg':>6}{'>30w%':>7}{'FRE':>5}  test  verdict")
        for r in sorted(results, key=lambda x: (x["flesch"])):
            print(f"{r['track']:32s}{r['lessons']:>4}{r['avg']:>6}{r['long']:>7}{r['flesch']:>5}  "
                  f"{'yes ' if r['test_yourself'] else 'no  '}  {r['verdict']}")
    else:
        print_detail(results[0])
    if args.strict and any(r["verdict"] == "FAIL" for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
