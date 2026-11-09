#!/usr/bin/env python3
"""Lists repeated facts and pointer lines in a repo's README and AGENTS.md files.

    repeats.py --root ROOT [--skip PATH]...

--root is the target repo. It defaults to the current directory. It is never
this file's location.

It reads every README.md and AGENTS.md under --root, git-tracked or untracked
but not ignored when --root is a git checkout. --skip leaves out a file or
folder, such as a README a skill reads or one the build ships.

It prints two kinds of line:

- A repeat: a line of at least MIN_WORDS words that appears both in an
  AGENTS.md and in the README.md beside it, or both in the root AGENTS.md and
  a nested one. Lines are compared after dropping list markers, case,
  punctuation, and extra spaces. Headings and fence markers never count.
- A pointer: a line telling the reader to read, see, or follow an AGENTS.md.

Which copy of a repeat to keep is the caller's call. Exit 1 when it finds
either kind.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

NAMES = {"README.md", "AGENTS.md"}
SKIP_DIRS = {".git", "node_modules", "__pycache__"}
MIN_WORDS = 4
POINTER = re.compile(r"\b(read|see|check|follow|consult|load|open)\b[^.\n]{0,40}\bAGENTS\.md\b", re.I)
LIST_MARKER = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
NON_WORD = re.compile(r"[^\w./-]+")


def main():
    parser = argparse.ArgumentParser(description="List repeats and pointer lines in README and AGENTS.md files.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--skip", action="append", default=[], type=Path)
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        sys.exit(2)
    skips = [(root / s).resolve() for s in args.skip]
    docs = [d for d in find_docs(root) if not any(d == s or s in d.parents for s in skips)]

    hits = []
    for doc in docs:
        for n, line in enumerate(read_lines(doc), 1):
            if POINTER.search(line):
                hits.append(f"{rel(doc, root)}:{n}: pointer: {line.strip()}")

    agents = {d.parent: d for d in docs if d.name == "AGENTS.md"}
    readmes = {d.parent: d for d in docs if d.name == "README.md"}
    pairs = [(agents[f], readmes[f]) for f in sorted(agents) if f in readmes]
    if root in agents:
        pairs += [(agents[root], agents[f]) for f in sorted(agents) if f != root]
    for first, second in pairs:
        seen = facts(first)
        for key, (n, line) in facts(second).items():
            if key in seen:
                hits.append(f"{rel(second, root)}:{n}: repeats {rel(first, root)}:{seen[key][0]}: {line}")

    print("\n".join(hits) if hits else f"Clean: {len(docs)} files.")
    sys.exit(1 if hits else 0)


def find_docs(root):
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard"],
            capture_output=True, text=True, check=True,
        ).stdout.splitlines()
        paths = [root / p for p in out]
    except (OSError, subprocess.CalledProcessError):
        paths = [p for p in root.rglob("*") if not SKIP_DIRS & set(p.relative_to(root).parts)]
    return sorted(p.resolve() for p in paths if p.name in NAMES and p.is_file())


def read_lines(doc):
    return doc.read_text(encoding="utf-8", errors="replace").splitlines()


def facts(doc):
    found = {}
    for n, line in enumerate(read_lines(doc), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "```", "~~~")):
            continue
        words = [w.strip("./-") for w in NON_WORD.sub(" ", LIST_MARKER.sub("", stripped)).lower().split()]
        words = [w for w in words if w]
        if len(words) >= MIN_WORDS:
            found.setdefault(" ".join(words), (n, stripped))
    return found


def rel(path, root):
    return path.relative_to(root).as_posix()


if __name__ == "__main__":
    main()
