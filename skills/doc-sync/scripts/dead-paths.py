#!/usr/bin/env python3
"""Lists repo paths that docs name but the tree no longer has.

    dead-paths.py --root ROOT [--doc-folder PATH]... [--config FILE]
                  [--code-root PATH]... [FILE...]

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
An extensionless path whose first segment is gone is skipped, even when the
last segment is defined under a code root.

A bare type name is a backtick span that is one identifier starting with an
uppercase letter and containing a lowercase letter. It is
checked only when code roots are known. --code-root sets those roots and
overrides the AGENTS.md heading `Code roots`. Without the flag, that heading's
list items are the roots. If the heading is missing and no flag is passed,
bare type names are not checked. A name is defined when a non-markdown file
under a code root has that stem, or a source line declares it. The script does
not append a file extension.

Paths holding a placeholder (<schema>, X.Y.Z, *) are skipped. Exit 1 when it
finds a dead path.
"""

import argparse
import re
import sys
from pathlib import Path

PLACEHOLDER = re.compile(r"[<>*$]|X\.Y\.Z|\.\.\.|…")
CODE_SPAN = re.compile(r"`([^`]+)`")
MARKDOWN_LINK = re.compile(r"\]\(([^)#\s]+)")
PATH_TOKEN = re.compile(r"(?<![\w./-])(?:\./)?((?:\.?[\w.+-]+/)+\.?[\w.+-]+)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$")
# A lowercase letter keeps all-caps tokens (CHANGED, URL) out of the type check.
BARE_TYPE = re.compile(r"[A-Z](?=[A-Za-z0-9]*[a-z])[A-Za-z0-9]*")
DECL_MODIFIER = r"(?:public|private|protected|internal|export|abstract|final|sealed|data|case|open|pub|async|default)"
DECL_KIND = r"(?:class|struct|enum|interface|trait|protocol|record|type|object|module|fn|func|function|def)"
MARKDOWN_SUFFIXES = {".md", ".markdown", ".mdx"}
SKIP_DIRS = {".git", "__pycache__"}
MAX_BYTES = 1_000_000


def main():
    parser = argparse.ArgumentParser(description="List doc paths the tree no longer has.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--doc-folder", action="append", default=[], type=Path)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--code-root", action="append", default=[], type=Path)
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

    code_roots = load_code_roots(root, args.code_root)
    defined = index_definitions(code_roots) if code_roots else set()

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
                if is_bare_type(path):
                    continue
                if not resolves(path, doc, root):
                    dead.append(f"{display(doc, root)}:{n}: {path}")
            if not code_roots:
                continue
            for name in sorted({bare for span in CODE_SPAN.findall(line) if (bare := bare_type(span))}):
                if name not in defined:
                    dead.append(f"{display(doc, root)}:{n}: {name}")

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


def load_code_roots(root, cli_roots):
    rels = [str(path) for path in cli_roots] if cli_roots else roots_from_agents(root)
    loaded = []
    for rel in rels:
        path = Path(rel)
        hit = path.resolve() if path.is_absolute() else (root / path).resolve()
        try:
            hit.relative_to(root)
        except ValueError:
            print(f"Code root is outside --root: {rel}", file=sys.stderr)
            sys.exit(2)
        if not hit.is_dir():
            print(f"Code root is not a directory: {rel}", file=sys.stderr)
            sys.exit(2)
        loaded.append(hit)
    return loaded


def roots_from_agents(root):
    agents = root / "AGENTS.md"
    if not agents.is_file():
        return []
    found = []
    capture = False
    for line in agents.read_text(encoding="utf-8").splitlines():
        heading = HEADING.match(line)
        if heading:
            capture = heading.group(1) == "Code roots"
            continue
        if not capture:
            continue
        item = line.strip()
        if item.startswith(("- ", "* ")):
            item = item[2:].strip()
        else:
            continue
        spans = CODE_SPAN.findall(item)
        text = spans[0] if spans else item
        text = text.strip().strip("`").split()[0].rstrip("/")
        if text and checkable(text):
            found.append(text)
    return found


def reportable(path, root):
    if not checkable(path):
        return False
    if "/" not in path.removeprefix("./"):
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


def is_bare_type(path):
    return bare_type(path) == path


def bare_type(span):
    text = span.strip()
    if BARE_TYPE.fullmatch(text):
        return text
    return ""


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


def index_definitions(code_roots):
    found = set()
    decl = re.compile(
        rf"(?m)^[ \t]*(?:{DECL_MODIFIER}\s+)*{DECL_KIND}\s+([A-Z][A-Za-z0-9]*)\b"
    )
    for code_root in code_roots:
        for path in code_root.rglob("*"):
            if not path.is_file() or any(part in SKIP_DIRS or part.startswith(".") for part in path.relative_to(code_root).parts[:-1]):
                continue
            stem = path.stem
            if path.suffix.lower() not in MARKDOWN_SUFFIXES and bare_type(stem):
                found.add(stem)
            if path.stat().st_size > MAX_BYTES or path.suffix.lower() in MARKDOWN_SUFFIXES:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            found.update(decl.findall(text))
    return found


def display(doc, root):
    try:
        return str(doc.resolve().relative_to(root))
    except ValueError:
        return str(doc)


if __name__ == "__main__":
    main()
