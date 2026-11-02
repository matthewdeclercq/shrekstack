#!/usr/bin/env python3
"""Installs the shrekstack base rule and starter files into a repo.

    setup_base.py --root REPO

Writes the base rule for Cursor and Claude Code, an AGENTS.md starter (or the
missing pieces of an existing one), a CLAUDE.md symlink, and starter hooks.
Prints one line per change, then one line per thing it left alone. Running it
again changes nothing but the two rule files, which it always overwrites.

Never edits product code. Needs Python 3.11 or later for tomllib.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "base.md"

CURSOR_FRONTMATTER = """---
description: Generic rules for a repo that adopts this library. Project lists, commands, and paths stay in that repo's AGENTS.md.
alwaysApply: true
---
"""

SKILLS_LINE = "Repo-specific skills live in `.agents/skills/`."

# The headings shrekstack skills read. A body that starts with TODO counts as missing.
HEADINGS = [
    ("Build & test", None),
    ("Entry points", "TODO: where reachability starts, such as mains, routes, and jobs."),
    ("Proof traps", "TODO: contracts to confirm before deleting code, such as persistence keys, reflection, and public APIs."),
    ("File layout", "TODO: the disjoint areas of the repo, one list item each."),
    ("Code roots", "TODO: path prefixes that hold code, one list item each."),
    ("Doc folders", "TODO: doc files and directories that doc-sync checks, one list item each."),
    ("Planning docs", "TODO: docs agents report against and never edit."),
    ("Architecture doc", "TODO: the one doc that says how the parts connect."),
    ("Testing defaults", "TODO: What to test, Where tests go, and which invariants are owner-rank."),
]

STACKS = ["js", "python", "go", "rust", "swift"]
SIGNALS = {
    "js": ["package.json"],
    "python": ["pyproject.toml", "setup.py", "setup.cfg", "requirements.txt"],
    "go": ["go.mod"],
    "rust": ["Cargo.toml"],
    "swift": ["Package.swift"],
}

GITLEAKS = ("gitleaks/gitleaks", "v8.30.1", [("gitleaks", [])])
HOOKS = {
    "js": [
        ("rbubley/mirrors-prettier", "v3.9.10", [("prettier", [])]),
        ("pre-commit/mirrors-eslint", "v10.14.0", [("eslint", ["files: '\\.[jt]sx?$'", "types: [file]"])]),
        GITLEAKS,
    ],
    "python": [("astral-sh/ruff-pre-commit", "v0.17.3", [("ruff-format", []), ("ruff-check", [])]), GITLEAKS],
    "go": [("golangci/golangci-lint", "v2.15.0", [("golangci-lint-fmt", []), ("golangci-lint", [])]), GITLEAKS],
    "rust": [("doublify/pre-commit-rust", "v1.0", [("fmt", []), ("clippy", [])]), GITLEAKS],
    "swift": [
        ("swiftlang/swift-format", "604.0.0", [("swift-format", [])]),
        ("realm/SwiftLint", "0.65.1", [("swiftlint", [])]),
        GITLEAKS,
    ],
}

HUSKY_PRE_COMMIT = """#!/bin/sh
npx lint-staged
gitleaks git --pre-commit --staged --redact --no-banner
"""
LINT_STAGED = [
    ("*.{js,jsx,ts,tsx,json,css,md,yml,yaml}", "prettier --write"),
    ("*.{js,jsx,ts,tsx}", "eslint --fix"),
]

INSTALL_FILES = [
    ".pre-commit-config.yaml",
    ".pre-commit-config.yml",
    "lefthook.yml",
    "lefthook.yaml",
    "lefthook.toml",
    ".lefthook.yml",
    ".simple-git-hooks.json",
]
KINDS = [
    ("formatter", r"ruff-format|prettier|golangci-lint-fmt|swift-format(?!-lint)|\bblack\b|gofmt|go-fmt|rustfmt|cargo fmt|(?<![\w-])fmt(?![\w-])|\bbiome\b"),
    ("linter", r"ruff-check|(?<![\w-])ruff(?![\w-])|eslint|swiftlint|swift-format-lint|clippy|flake8|pylint|golangci-lint(?!-fmt)|\bbiome\b"),
    ("secrets check", r"gitleaks|detect-secrets|trufflehog"),
]

MD_HEADING = re.compile(r"^ {0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
ADORNMENT = re.compile(r"^([=\-~^\"'`*+#:.])\1{2,}\s*$")
MAKE_TARGET = re.compile(r"^([^\s#:=][^:#=]*?)\s*::?(?![:=])")


def main():
    parser = argparse.ArgumentParser(description="Install the shrekstack base rule and starters.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        sys.exit(2)
    if not BASE.is_file():
        print(f"base.md is not beside this skill: {BASE}", file=sys.stderr)
        sys.exit(2)

    done, notes = [], []
    base = BASE.read_text(encoding="utf-8")
    write(root / ".cursor" / "rules" / "shrekstack-base.mdc", CURSOR_FRONTMATTER + "\n" + base)
    write(root / ".claude" / "rules" / "shrekstack-base.md", base)
    done.append("wrote .cursor/rules/shrekstack-base.mdc and .claude/rules/shrekstack-base.md")

    agents = agents_md(root, done, notes)
    if agents:
        claude_md(root, agents, done, notes)
    hooks(root, done, notes)

    print("\n".join(done + notes))


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read(path):
    return path.read_text(encoding="utf-8", errors="replace")


def inside(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


# AGENTS.md


def agents_md(root, done, notes):
    path = root / "AGENTS.md"
    if not os.path.lexists(path):
        write(path, starter(root))
        done.append("wrote the AGENTS.md starter")
        return path.resolve()

    resolved = path.resolve()
    if path.is_symlink() and resolved.exists() and not inside(resolved, root):
        notes.append(f"AGENTS.md is a symlink to {os.readlink(path)} outside the repo; left it")
        return None
    if not resolved.is_file():
        notes.append("AGENTS.md is not a file in the repo; left it")
        return None

    text = read(resolved)
    new, extras = skills_line(text)
    if extras < 0:
        done.append("added the skills line to AGENTS.md")
    elif extras:
        done.append(f"removed {extras} duplicate skills line(s) from AGENTS.md")
    missing = [name for name, _ in HEADINGS if name not in headings(new)]
    if missing:
        new = new.rstrip("\n") + "\n\n" + "\n\n".join(section(root, name) for name in missing) + "\n"
        done.append("added TODO headings to AGENTS.md: " + ", ".join(missing))
    if new != text:
        resolved.write_text(new, encoding="utf-8")
    return resolved


def starter(root):
    parts = [f"# {root.name}", readme_sentence(root), SKILLS_LINE]
    parts += [section(root, name) for name, _ in HEADINGS]
    return "\n\n".join(parts) + "\n"


def section(root, name):
    body = dict(HEADINGS)[name]
    if body is None:
        cmds = commands(root)
        body = "\n".join(f"- {label}: `{cmds[key]}`" for label, key in (("Build", "build"), ("Test", "test"), ("Run", "run")))
    return f"## {name}\n\n{body}"


def skills_line(text):
    """Returns the text with the skills line exactly once, and how many it removed (-1 when it added one)."""
    lines = text.splitlines(keepends=True)
    hits = [i for i, line in enumerate(lines) if line.rstrip("\r\n") == SKILLS_LINE]
    if len(hits) > 1:
        for i in reversed(hits[1:]):
            del lines[i]
            if i < len(lines) and not lines[i].strip() and (i == 0 or not lines[i - 1].strip()):
                del lines[i]
        return "".join(lines), len(hits) - 1
    if hits:
        return text, 0
    at = next((i for i, kind in outside_fences(lines) if kind and kind >= 2), None)
    if at is None:
        return text.rstrip("\n") + "\n\n" + SKILLS_LINE + "\n", -1
    lines[at:at] = [SKILLS_LINE + "\n", "\n"]
    return "".join(lines), -1


def outside_fences(lines):
    """Yields (index, heading level or 0) for each line outside a fenced block."""
    fenced = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if not fenced:
            match = MD_HEADING.match(line.rstrip("\r\n"))
            yield i, len(match.group(1)) if match else 0


def headings(text):
    lines = text.splitlines()
    return {MD_HEADING.match(lines[i]).group(2) for i, level in outside_fences(lines) if level}


# README sentence


def readme_sentence(root):
    for name in ("README.md", "README.rst", "README"):
        path = root / name
        if path.is_file():
            text = read(path)
            break
    else:
        return "TODO"

    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    heading = None
    seen_paragraph = False
    for block in blocks(text):
        para = []
        i = 0
        while i < len(block):
            line = block[i]
            match = MD_HEADING.match(line)
            if match:
                heading = heading or match.group(2)
            elif i + 1 < len(block) and ADORNMENT.match(block[i + 1]) and not ADORNMENT.match(line):
                heading = heading or line.strip()
                i += 1
            elif not ADORNMENT.match(line):
                para.append(line.strip())
            i += 1
        if not para:
            continue
        joined = " ".join(para)
        if not seen_paragraph:
            seen_paragraph = True
            if only_images(joined):
                continue
        return first_sentence(joined)
    return heading or "TODO"


def blocks(text):
    found, current, fenced = [], [], False
    for line in text.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced:
            continue
        if line.strip():
            current.append(line)
        elif current:
            found.append(current)
            current = []
    if current:
        found.append(current)
    return found


def only_images(text):
    for pattern in (
        r"!\[[^\]]*\]\([^)]*\)",
        r"!\[[^\]]*\]\[[^\]]*\]",
        r"\[\s*\]\([^)]*\)",
        r"\[\s*\]\[[^\]]*\]",
        r"<[^>]+>",
        r"\.\. (?:image|figure)::\S*",
        r":target:\s*\S*",
        r"\|[^|]+\|",
    ):
        text = re.sub(pattern, "", text)
    return not text.strip()


def first_sentence(text):
    text = " ".join(text.split())
    for i, char in enumerate(text):
        if char not in ".!?":
            continue
        if char == "." and 0 < i < len(text) - 1 and text[i - 1].isdigit() and text[i + 1].isdigit():
            continue
        return text[: i + 1]
    return text


# Commands


def commands(root):
    cmds = {"build": None, "test": None, "run": None}
    targets = make_targets(root)
    cmds["build"] = next((f"make {t}" for t in ("build", "all") if t in targets), None)
    cmds["test"] = next((f"make {t}" for t in ("test", "check") if t in targets), None)
    cmds["run"] = "make run" if "run" in targets else None

    stacks = detect_stacks(root)
    if len(stacks) == 1:
        found = STACK_COMMANDS[stacks[0]](root)
        for key in cmds:
            cmds[key] = cmds[key] or found.get(key)
    return {key: value or "TODO" for key, value in cmds.items()}


def make_targets(root):
    path = root / "Makefile"
    if not path.is_file():
        return set()
    targets = set()
    for line in read(path).splitlines():
        match = MAKE_TARGET.match(line)
        if match:
            targets.update(match.group(1).split())
    return targets


def detect_stacks(root):
    found = []
    for stack in STACKS:
        hit = any((root / name).is_file() for name in SIGNALS[stack])
        if stack == "swift":
            hit = hit or bool(xcode_bundles(root))
        if hit:
            found.append(stack)
    return found


def xcode_bundles(root):
    return sorted(p for p in root.iterdir() if p.is_dir() and p.suffix in (".xcodeproj", ".xcworkspace"))


def load_json(path):
    try:
        data = json.loads(read(path))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def load_toml(path):
    try:
        return tomllib.loads(read(path))
    except (OSError, tomllib.TOMLDecodeError):
        return None


def table(data, *keys):
    for key in keys:
        data = data.get(key) if isinstance(data, dict) else None
    return data if isinstance(data, dict) else {}


def js_commands(root):
    pkg = load_json(root / "package.json")
    if pkg is None:
        return {}
    runner = js_runner(root, pkg)
    if runner is None:
        return {}
    scripts = table(pkg, "scripts")

    def cmd(script):
        if not isinstance(scripts.get(script), str):
            return None
        if runner in ("npm", "pnpm"):
            return f"{runner} {script}" if script in ("test", "start") else f"{runner} run {script}"
        return f"yarn {script}" if runner == "yarn" else f"bun run {script}"

    return {
        "build": cmd("build") or cmd("compile"),
        "test": cmd("test"),
        "run": cmd("start") or cmd("dev"),
    }


def js_runner(root, pkg):
    manager = pkg.get("packageManager")
    if isinstance(manager, str):
        for runner in ("pnpm", "yarn", "bun", "npm"):
            if manager.startswith(runner + "@"):
                return runner
    locks = {
        "pnpm": ["pnpm-lock.yaml"],
        "yarn": ["yarn.lock"],
        "bun": ["bun.lock", "bun.lockb"],
        "npm": ["package-lock.json"],
    }
    found = [runner for runner, names in locks.items() if any((root / n).is_file() for n in names)]
    if not found:
        return "npm"
    return found[0] if len(found) == 1 else None


def python_commands(root):
    data = {}
    if (root / "pyproject.toml").is_file():
        data = load_toml(root / "pyproject.toml")
        if data is None:
            return {}
    project = table(data, "project")
    poetry = table(data, "tool", "poetry")

    deps = []
    deps += strings(project.get("dependencies"))
    for group in table(project, "optional-dependencies").values():
        deps += strings(group)
    for group in table(data, "dependency-groups").values():
        deps += strings(group)
    deps += list(table(poetry, "dependencies")) + list(table(poetry, "dev-dependencies"))
    for group in table(poetry, "group").values():
        deps += list(table(group, "dependencies"))
    if (root / "requirements.txt").is_file():
        deps += [line for line in read(root / "requirements.txt").splitlines() if not line.strip().startswith(("#", "-"))]
    names = {dep_name(dep) for dep in deps}
    pytest = "pytest" in names or "pytest" in table(data, "tool")

    scripts = list(dict.fromkeys(list(table(project, "scripts")) + list(table(poetry, "scripts"))))

    uv = (root / "uv.lock").is_file()
    poetry_lock = (root / "poetry.lock").is_file()
    if uv and poetry_lock:
        return {}
    prefix = "uv run " if uv else "poetry run " if poetry_lock or "poetry" in table(data, "tool") else ""
    return {
        "test": prefix + "pytest" if pytest else None,
        "run": prefix + scripts[0] if len(scripts) == 1 else None,
    }


def strings(value):
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []


def dep_name(text):
    match = re.match(r"\s*([A-Za-z0-9][A-Za-z0-9._-]*)", text)
    return re.sub(r"[-_.]+", "-", match.group(1)).lower() if match else ""


def go_commands(root):
    run = None
    if any(is_main(path) for path in root.glob("*.go")):
        run = "go run ."
    elif (root / "cmd").is_dir():
        mains = [d for d in sorted((root / "cmd").iterdir()) if d.is_dir() and any(is_main(p) for p in d.glob("*.go"))]
        if len(mains) == 1:
            run = f"go run ./cmd/{mains[0].name}"
    return {"build": "go build ./...", "test": "go test ./...", "run": run}


def is_main(path):
    return path.is_file() and any(line.strip() == "package main" for line in read(path).splitlines())


def rust_commands(root):
    cargo = load_toml(root / "Cargo.toml") or {}
    runs = (root / "src" / "main.rs").is_file() or isinstance(cargo.get("bin"), list)
    return {"build": "cargo build", "test": "cargo test", "run": "cargo run" if runs else None}


def swift_commands(root):
    package = root / "Package.swift"
    if package.is_file():
        return {"build": "swift build", "test": "swift test", "run": "swift run" if ".executable" in read(package) else None}
    bundles = xcode_bundles(root)
    if len(bundles) != 1:
        return {}
    bundle = bundles[0]
    schemes = sorted((bundle / "xcshareddata" / "xcschemes").glob("*.xcscheme"))
    if len(schemes) != 1:
        return {}
    flag = "-workspace" if bundle.suffix == ".xcworkspace" else "-project"
    base = f"xcodebuild {flag} {quote(bundle.name)} -scheme {quote(schemes[0].stem)}"
    return {"build": f"{base} build", "test": f"{base} test"}


def quote(name):
    return f'"{name}"' if " " in name else name


STACK_COMMANDS = {
    "js": js_commands,
    "python": python_commands,
    "go": go_commands,
    "rust": rust_commands,
    "swift": swift_commands,
}


# CLAUDE.md


def claude_md(root, agents, done, notes):
    path = root / "CLAUDE.md"
    if not os.path.lexists(path):
        os.symlink("AGENTS.md", path)
        done.append("linked CLAUDE.md to AGENTS.md")
    elif path.is_symlink():
        if path.resolve() != agents:
            notes.append(f"CLAUDE.md is a symlink to {os.readlink(path)}; left it")
    elif path.is_dir():
        notes.append("CLAUDE.md is a directory; left it")
    else:
        notes.append("CLAUDE.md is a regular file; left it")


# Hooks


def hooks(root, done, notes):
    pkg = load_json(root / "package.json") if (root / "package.json").is_file() else None
    installed, texts = existing_hooks(root, pkg, notes)
    if installed:
        if texts:
            joined = "\n".join(texts)
            notes += [f"no {kind}" for kind, pattern in KINDS if not re.search(pattern, joined)]
        return

    stacks = detect_stacks(root)
    if not stacks:
        notes.append("hooks not written; no stack detected")
        return
    if len(stacks) > 1:
        notes.append("hooks not written; saw " + ", ".join(stacks))
        return
    if stacks[0] == "js" and pkg and depends(pkg, "husky") and depends(pkg, "lint-staged"):
        husky(root, done, notes)
        return
    write(root / ".pre-commit-config.yaml", pre_commit_config(stacks[0]))
    done.append(f"wrote .pre-commit-config.yaml for {stacks[0]}")


def existing_hooks(root, pkg, notes):
    installed, texts = False, []
    for name in INSTALL_FILES:
        if (root / name).is_file():
            installed = True
            texts.append(read(root / name))
    if (root / ".husky").is_dir():
        installed = True
        texts += files_in(root / ".husky")
    for key in ("lint-staged", "simple-git-hooks"):
        if pkg and key in pkg:
            installed = True
            texts.append(json.dumps(pkg[key]))

    hooks_path = git(root, "config", "--get", "core.hooksPath")
    if hooks_path:
        installed = True
        where = (root / Path(hooks_path).expanduser()).resolve()
        if inside(where, root):
            texts += files_in(where)
        else:
            notes.append("hooks path is outside the repo; left it")

    common = git(root, "rev-parse", "--git-common-dir")
    git_hooks = (root / common / "hooks") if common else root / ".git" / "hooks"
    sample_free = [p for p in git_hooks.iterdir() if p.is_file() and not p.name.endswith(".sample")] if git_hooks.is_dir() else []
    if sample_free:
        installed = True
        texts += [read(p) for p in sample_free]
    return installed, texts


def files_in(directory):
    return [read(p) for p in sorted(directory.iterdir()) if p.is_file()] if directory.is_dir() else []


def git(root, *args):
    try:
        proc = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    except OSError:
        return ""
    return proc.stdout.strip() if proc.returncode == 0 else ""


def depends(pkg, name):
    return any(name in table(pkg, section) for section in ("dependencies", "devDependencies"))


def pre_commit_config(stack):
    lines = ["repos:"]
    for repo, rev, ids in HOOKS[stack]:
        lines += [f"  - repo: https://github.com/{repo}", f"    rev: {rev}", "    hooks:"]
        for hook_id, extras in ids:
            lines.append(f"      - id: {hook_id}")
            lines += [f"        {extra}" for extra in extras]
    return "\n".join(lines) + "\n"


def husky(root, done, notes):
    path = root / "package.json"
    text = read(path)
    end = text.rstrip().rfind("}")
    before = text[:end].rstrip()
    match = re.search(r'^([ \t]+)"', text, re.M)
    indent = match.group(1) if match else "  "
    entries = ",\n".join(f'{indent * 2}{json.dumps(glob)}: {json.dumps(cmd)}' for glob, cmd in LINT_STAGED)
    comma = "" if before.endswith("{") else ","
    new = f'{before}{comma}\n{indent}"lint-staged": {{\n{entries}\n{indent}}}\n{text[end:]}'
    old, parsed = json.loads(text), load_json_text(new)
    if parsed is None or {k: v for k, v in parsed.items() if k != "lint-staged"} != old:
        notes.append("hooks not written; could not add lint-staged to package.json without changing other lines")
        return

    hook = root / ".husky" / "pre-commit"
    write(hook, HUSKY_PRE_COMMIT)
    hook.chmod(0o755)
    path.write_text(new, encoding="utf-8")
    done.append("wrote .husky/pre-commit and the lint-staged key in package.json")
    if git(root, "rev-parse", "--is-inside-work-tree") == "true" and not git(root, "config", "--get", "core.hooksPath"):
        git(root, "config", "core.hooksPath", ".husky")
        done.append("set core.hooksPath to .husky")


def load_json_text(text):
    try:
        data = json.loads(text)
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


if __name__ == "__main__":
    main()
