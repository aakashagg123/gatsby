"""Lesson 2: a lint for a project instruction file such as CLAUDE.md, and what a long file costs.

The rules follow the Claude Code documentation: keep the file short, put in what the agent cannot work out
from the code, avoid advice with no test, and avoid contradictions. The sample file is invented.
Run: python3 lesson2_context_file.py
"""
import re

SAMPLE = """# Project
- Write clean code.
- Follow best practices.
- Use pytest. Run `pytest -x` before you say you are done.
- IMPORTANT: never edit files under migrations/.
- IMPORTANT: NEVER commit secrets. MUST use the vault.
- Use pytest. Run `pytest -x` before you say you are done.
- src/billing/invoice.py contains the Invoice class, which has a total() method and a send() method.
- Be careful with the database.
- Run `make lint` before every commit.
- Use tabs for indentation.
- Use spaces for indentation.
"""

VAGUE = ("write clean code", "follow best practices", "be careful", "write good code", "be thorough", "use common sense")


def lint(text, max_lines=200):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    findings = []
    if len(text.splitlines()) > max_lines:
        findings.append(("too long", f"{len(text.splitlines())} lines; the docs target under {max_lines}"))
    seen = {}
    for i, l in enumerate(lines):
        body = l.lstrip("-* ").lower()
        if any(v in body for v in VAGUE):
            findings.append(("vague advice", l))
        if re.search(r"\b[\w./-]+\.(py|js|ts|go|rs)\b contains\b", body):
            findings.append(("describes the code", l))
        if body in seen:
            findings.append(("duplicate", l))
        seen.setdefault(body, i)
    shouting = sum(len(re.findall(r"\b(IMPORTANT|NEVER|MUST|ALWAYS)\b", l)) for l in lines)
    if shouting > 3:
        findings.append(("too much emphasis", f"{shouting} shouted words; emphasis only works on one or two lines"))
    if ("tabs for indentation" in text) and ("spaces for indentation" in text):
        findings.append(("contradiction", "tabs and spaces are both required"))
    if not re.search(r"`[^`]*(test|pytest|make|npm|cargo)[^`]*`", text):
        findings.append(("no commands", "no build or test command the agent can run"))
    return findings


def file_cost(lines, tokens_per_line=14, sessions_per_day=40, developers=25, price_per_mtok=3.0, cache_read=0.1):
    """Input tokens the file adds at the start of every session, and what that costs a team in a month (22 working days)."""
    tokens = lines * tokens_per_line
    monthly = tokens * sessions_per_day * developers * 22
    return tokens, monthly * price_per_mtok / 1e6, monthly * price_per_mtok * cache_read / 1e6


def main():
    return dict(findings=lint(SAMPLE), short=file_cost(150), long=file_cost(600))


if __name__ == "__main__":
    r = main()
    for kind, detail in r["findings"]:
        print(f"{kind:20s} {detail}")
    kinds = [k for k, _ in r["findings"]]
    print("150-line file: %d tokens per session, $%.0f a month uncached, $%.0f with cache reads" % r["short"])
    print("600-line file: %d tokens per session, $%.0f a month uncached, $%.0f with cache reads" % r["long"])
    assert kinds.count("vague advice") == 3 and kinds.count("duplicate") == 1
    assert "describes the code" in kinds and "too much emphasis" in kinds and "contradiction" in kinds
    assert "no commands" not in kinds and "too long" not in kinds
    assert r["long"][0] == 4 * r["short"][0]
    print("lesson 2 ok")
