#!/usr/bin/env python3
"""Lists repo paths that docs name but the tree no longer has.

    dead-paths.py --root ROOT [--doc-folder PATH]... [--config FILE] [FILE...]

--root is the tree paths resolve against. It defaults to the current directory.
It is never this file's location: a checkout of the skill library is not the
target repo.

Pass doc files, or directories of markdown, as FILE arguments or as repeated
--doc-folder values. A relative path is joined to --root. --config is a text
file of those same paths, one per line. Blank lines and lines starting with #
are ignored.

With no FILE, no --doc-folder, and no --config, the script exits 2. It does
not assume a doc list.

A path counts inside backticks, a Markdown link, or a fenced block. A backtick
path counts when its first segment exists under --root, or when the last
segment has a file extension (so a deleted top-level directory still shows up).
An extensionless path whose first segment is gone is skipped. Relative links
are always checked. Paths holding a placeholder (<schema>, X.Y.Z, *) are
skipped. Exit 1 when it finds a dead path.
"""

import argparse
import re
import sys
from pathlib import Path

PLACEHOLDER = re.compile(r"[<>*$]|X\.Y\.Z|\.\.\.|…")
CODE_SPAN = re.compile(r"`([^`]+)`")
MARKDOWN_LINK = re.compile(r"\]\(([^)#\s]+)")
PATH_TOKEN = re.compile(r"(?<![\w./-])(?:\./)?((?:\.?[\w.+-]+/)+\.?[\w.+-]+)")


def main():
    parser = argparse.ArgumentParser(description="List doc paths the tree no longer has.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--doc-folder", action="append", default=[], type=Path)
    parser.add_argument("--config", type=Path)
    parser.add_argument("files", nargs="*", type=Path)
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        sys.exit(2)

    listed = list(args.files) + list(args.doc_folder)
    if args.config:
        config = join_root(root, args.config)
        if not config.is_file():
            print(f"No such config: {config}", file=sys.stderr)
            sys.exit(2)
        for line in config.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                listed.append(Path(line))

    files = collect(root, listed)
    if not files:
        print(
            "Name the docs to check: pass FILE, --doc-folder, or --config. "
            "The list is the target repo's AGENTS.md heading 'Doc folders'. "
            "This script does not guess it.",
            file=sys.stderr,
        )
        sys.exit(2)

    dead = []
    for doc in files:
        text = doc.read_text(encoding="utf-8")
        fenced = False
        for n, line in enumerate(text.splitlines(), 1):
            if line.lstrip().startswith("```"):
                fenced = not fenced
                continue
            spans = [line] if fenced else CODE_SPAN.findall(line)
            links = [] if fenced else MARKDOWN_LINK.findall(line)
            paths = [p for span in spans for p in PATH_TOKEN.findall(span) if reportable(p, root)]
            paths += [p for p in links if reportable_link(p)]
            for path in sorted(set(paths)):
                if not resolves(path, doc, root):
                    dead.append(f"{display(doc, root)}:{n}: {path}")

    print("\n".join(dead) if dead else f"Clean: {len(files)} docs.")
    sys.exit(1 if dead else 0)


def collect(root, listed):
    files = []
    seen = set()
    for raw in listed:
        path = join_root(root, raw)
        if path.is_dir():
            found = sorted(p for p in path.rglob("*.md") if p.is_file())
            if not found:
                print(f"No markdown under: {path}", file=sys.stderr)
                sys.exit(2)
        elif path.is_file():
            found = [path]
        else:
            print(f"No such doc path: {path}", file=sys.stderr)
            sys.exit(2)
        for doc in found:
            key = doc.resolve()
            if key not in seen:
                seen.add(key)
                files.append(doc)
    return files


def join_root(root, path):
    path = path.expanduser()
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def reportable(path, root):
    if not checkable(path):
        return False
    first = path.removeprefix("./").split("/", 1)[0]
    if first in (".", ".."):
        return True
    if (root / first).exists():
        return True
    last = path.rstrip("/").rsplit("/", 1)[-1]
    return "." in last and not last.startswith(".")


def reportable_link(path):
    if not checkable(path):
        return False
    return not path.startswith(("/", "mailto:")) and "://" not in path


def checkable(path):
    return not PLACEHOLDER.search(path) and "://" not in path and not path.startswith("mailto:")


def resolves(path, doc, root):
    rel = path.removeprefix("./")
    for base in (root / rel, doc.parent / rel):
        try:
            hit = base.resolve()
        except OSError:
            continue
        if not hit.exists():
            continue
        try:
            hit.relative_to(root)
        except ValueError:
            continue
        return True
    return False


def display(doc, root):
    try:
        return str(doc.resolve().relative_to(root))
    except ValueError:
        return str(doc)


if __name__ == "__main__":
    main()
