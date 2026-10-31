#!/usr/bin/env python3
"""Require name and description in every SKILL.md. name matches its folder.

Run from the repo root. Exits 1 when a skill fails.
"""

import sys
from pathlib import Path


def main():
    root = Path.cwd()
    files = sorted(path for path in root.rglob("SKILL.md") if ".git" not in path.parts)
    if not files:
        print("No SKILL.md files.", file=sys.stderr)
        sys.exit(1)

    errors = []
    for path in files:
        shown = path.relative_to(root)
        lines = frontmatter(path.read_text(encoding="utf-8"))
        if lines is None:
            errors.append(f"{shown}: no frontmatter")
            continue
        name = field(lines, "name")
        description = field(lines, "description")
        if not name:
            errors.append(f"{shown}: name missing")
        elif name != path.parent.name:
            errors.append(f"{shown}: name {name!r} != folder {path.parent.name!r}")
        if not description:
            errors.append(f"{shown}: description missing")

    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print(f"ok: {len(files)} skills")


def frontmatter(text):
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index]
    return None


def field(lines, key):
    prefix = f"{key}:"
    for index, line in enumerate(lines):
        if not line.startswith(prefix):
            continue
        rest = line[len(prefix):].strip()
        if is_block(rest):
            chunks = []
            for nxt in lines[index + 1:]:
                if nxt.startswith((" ", "\t")):
                    chunks.append(nxt.strip())
                elif nxt.strip() == "":
                    continue
                else:
                    break
            return " ".join(chunk for chunk in chunks if chunk).strip()
        return unquote(rest).strip()
    return None


def is_block(rest):
    if not rest:
        return False
    token = rest.split()[0]
    if token[:1] not in ">|":
        return False
    body = token[1:]
    if body[:1] in "+-":
        body = body[1:]
    return body == "" or body.isdigit()


def unquote(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


if __name__ == "__main__":
    main()
