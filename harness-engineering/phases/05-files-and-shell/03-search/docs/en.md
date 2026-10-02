# Search: Glob by Name, Grep by Content

> **Motto** — Find the right 20 lines in a million by searching, not by reading everything.

*Part of Phase 05 — Files and Shell.*

*Last reviewed: 2026-10 · Volatility: fast*

## The Problem

"Where is `parse_config` defined, and who calls it?" The agent cannot read the whole repo to find out. That is slow and it breaks the context budget.

The agent needs two search tools. One finds files by **name** ("every `*.py` under `src`"). One finds lines by **content** ("every line that matches this regex"). Both must return short, citable results, and both must be capped.

## The Concept

```mermaid
flowchart LR
  Q["regex + file filter"] --> S["scan matching files"] --> M["path:line: match (+ context)"]
```

Glob returns paths. Grep returns `path:line: text`. The agent then reads the promising hit and edits it. The core file loop is search, read, edit.

Two details decide the quality of a search tool. Results need an order and a cap. Glob sorts newest first, because recently changed files are usually the relevant ones. Both tools skip vendored and VCS folders such as `.git` and `node_modules`, or the output fills with noise. A truncation line tells the model to narrow the query.

## Build It

`code/search_tools.py` has `find_files` (glob) and `grep` in one file. Grep has three output modes: full lines, file names only, or counts. Context lines use `-` after the file name and match lines use `:`, the same marks as `grep -n -C`.

```python
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv"}


def _files(root, pattern):
    root = Path(root)
    for p in root.glob(pattern):
        if p.is_file() and not (set(p.relative_to(root).parts) & SKIP_DIRS):
            yield p


def find_files(pattern, root=".", limit=100):
    """Glob by name. Newest first, capped, so recent files surface."""
    paths = sorted(_files(root, pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    out = [str(p.relative_to(root)) for p in paths[:limit]]
    if len(paths) > limit:
        out.append(f"[truncated: {len(paths)} files match, showing {limit}; narrow the pattern]")
    return out


def grep(pattern, root=".", glob="**/*", context=0, mode="content", limit=50):
    """Regex search by content. mode: content | files_with_matches | count."""
    rx = re.compile(pattern)
    hits, files, counts = [], [], {}
    for p in sorted(_files(root, glob)):
        try:
            lines = p.read_text().splitlines()
        except (UnicodeDecodeError, PermissionError):
            continue                                   # binary or unreadable
        name = str(p.relative_to(root))
        for i, line in enumerate(lines):
            if not rx.search(line):
                continue
            counts[name] = counts.get(name, 0) + 1
            for j in range(max(0, i - context), min(len(lines), i + context + 1)):
                mark = ":" if j == i else "-"
                hits.append(f"{name}{mark}{j + 1}: {lines[j]}")
        if name in counts:
            files.append(name)
    if mode == "files_with_matches":
        return files
    if mode == "count":
        return [f"{n}:{counts[n]}" for n in files]
    if len(hits) > limit:
        return hits[:limit] + [f"[truncated: {len(hits)} lines, showing {limit}]"]
    return hits
```

There is no index to build or keep in sync. The price is a scan on every call. That is fine for a repo-sized tree. A huge tree needs a real indexer such as ripgrep, or the repo map in [Repo Map](../../../08-extending-mcp-skills-retrieval/04-repo-map/docs/en.md).

The asserts build a small tree with fixed modification times. They check the newest-first order, the skipped folders, the context marks, all three modes, and both truncation notes. Run `python3 code/search_tools.py`.

## Use It

Claude Code has **Glob** and **Grep** tools. Glob matches patterns such as `**/*.js`. It sorts by modification time and caps results at 100 files. It does not respect `.gitignore` by default.

Grep is built on ripgrep, so it uses ripgrep regex syntax. Braces need escaping: find `interface{}` with `interface\{\}`. It has three modes: `files_with_matches` (the default), `content`, and `count`. It respects `.gitignore`. It can filter by `glob` or by file `type`, and it can match across lines with `multiline: true`.

The docs say Glob and Grep are absent by default on macOS, Linux and WSL, with documented ways to bring them back. Check your install before you write a rule for them.

`Read(path)` deny rules are applied to Grep and Glob on a best-effort basis. A `Glob(...)` rule on its own is never consulted. The [Settings.json](../../../06-permissions-and-security/03-settings-json/docs/en.md) lesson explains why.

## Challenge

Add a `.gitignore` reader to `find_files`, so it skips ignored paths the way Grep does. Assert that a file listed in `.gitignore` disappears from the results. Then explain why Claude Code's Glob and Grep differ on this point.

## Sources

Claude Code docs, "Tools reference", sections "Glob tool behavior" and "Grep tool behavior" (code.claude.com/docs/en/tools-reference).

Next: [Bash and Timeouts](../../04-bash-and-timeouts/docs/en.md)
