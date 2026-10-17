"""Lesson 4: control. A small model of permission rules, and what a rule does not stop.

This is a simplified model of the rules described in the Claude Code permissions documentation, not
Claude Code's own code. Rules are checked in the order deny, then ask, then allow, and the first match
wins. A Bash rule matches the command text the agent wrote. Run: python3 lesson4_permissions.py
"""
import fnmatch
import re


def parse(rule):
    m = re.fullmatch(r"(\w+)\((.*)\)", rule)
    return (m.group(1), m.group(2)) if m else (rule, None)


def matches(rule, tool, target):
    name, pattern = parse(rule)
    if name != tool:
        return False
    if pattern is None:
        return True
    if tool == "Bash":
        return fnmatch.fnmatchcase(target, pattern)                     # '*' matches any text, and the match is on the command as written
    return fnmatch.fnmatchcase(target, pattern.replace("**", "*"))      # paths, simplified


def decide(tool, target, deny=(), ask=(), allow=(), default="ask"):
    for label, rules in (("deny", deny), ("ask", ask), ("allow", allow)):
        if any(matches(r, tool, target) for r in rules):
            return label
    return default


def main():
    deny = ["Bash(curl *)", "Bash(rm *)", "Bash(git push *)", "Read(data/test/*)"]
    allow = ["Bash(git push origin main)", "Bash(npm test *)", "Read(src/*)"]
    ask = ["Bash(git clean *)"]
    cases = {
        "curl https://example.com": ("Bash", "curl https://example.com"),
        "/usr/bin/curl https://example.com": ("Bash", "/usr/bin/curl https://example.com"),
        "sh -c 'curl https://example.com'": ("Bash", "sh -c 'curl https://example.com'"),
        "git push origin main": ("Bash", "git push origin main"),
        "git -C . push origin main": ("Bash", "git -C . push origin main"),
        "npm test -- --watch": ("Bash", "npm test -- --watch"),
        "git clean -f": ("Bash", "git clean -f"),
        "Read data/test/cases.csv": ("Read", "data/test/cases.csv"),
        "Read src/app.py": ("Read", "src/app.py"),
    }
    return {name: decide(t, x, deny, ask, allow) for name, (t, x) in cases.items()}


if __name__ == "__main__":
    r = main()
    for k, v in r.items():
        print(f"{v:6s} {k}")
    assert r["curl https://example.com"] == "deny"
    assert r["/usr/bin/curl https://example.com"] == "ask"             # the rule did not match this form
    assert r["sh -c 'curl https://example.com'"] == "ask"
    assert r["git push origin main"] == "deny"                         # a broad deny beats a narrower allow
    assert r["git -C . push origin main"] == "ask"
    assert r["npm test -- --watch"] == "allow" and r["git clean -f"] == "ask"
    assert r["Read data/test/cases.csv"] == "deny" and r["Read src/app.py"] == "allow"
    print("lesson 4 ok")
