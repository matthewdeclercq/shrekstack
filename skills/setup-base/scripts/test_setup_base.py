#!/usr/bin/env python3
"""Runs setup_base.py against throwaway repos and checks what it writes and leaves."""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("setup_base.py")
BASE = Path(__file__).resolve().parent.parent / "base.md"
SKILLS_LINE = "Repo-specific skills live in `.agents/skills/`."


def run(root):
    proc = subprocess.run([sys.executable, str(SCRIPT), "--root", str(root)], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    return proc.stdout


def repo(tmp, name, files, git=False):
    root = Path(tmp) / name
    root.mkdir()
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    if git:
        subprocess.run(["git", "init", "-q", str(root)], check=True)
    return root


def agents(root):
    return (root / "AGENTS.md").read_text(encoding="utf-8")


def python_starter(tmp):
    root = repo(tmp, "widgets", {
        "README.md": "# Widgets\n\n[![ci](https://x/badge.svg)](https://x)\n\nWidgets for v1.2 users. More text.\n",
        "pyproject.toml": '[project]\nname = "w"\n[project.scripts]\nwidget = "w:main"\n[dependency-groups]\ndev = ["pytest>=8"]\n',
        "uv.lock": "",
    }, git=True)
    out = run(root)
    base = BASE.read_text(encoding="utf-8")
    assert (root / ".claude/rules/shrekstack-base.md").read_text() == base
    cursor = (root / ".cursor/rules/shrekstack-base.mdc").read_text()
    assert cursor.startswith("---\ndescription: ") and cursor.endswith("---\n\n" + base), cursor[:200]

    text = agents(root)
    assert text.startswith("# widgets\n\nWidgets for v1.2 users.\n\n" + SKILLS_LINE + "\n"), text
    assert "- Test: `uv run pytest`" in text and "- Run: `uv run widget`" in text and "- Build: `TODO`" in text, text
    for heading in ("Entry points", "Code roots", "Testing defaults"):
        assert f"## {heading}\n\nTODO:" in text, heading
    assert os.readlink(root / "CLAUDE.md") == "AGENTS.md"
    config = (root / ".pre-commit-config.yaml").read_text()
    assert "id: ruff-format" in config and "id: ruff-check" in config and "id: gitleaks" in config, config

    again = run(root)
    assert agents(root) == text
    assert "AGENTS.md" not in again and "pre-commit" not in again, again
    assert "wrote the AGENTS.md starter" in out


def existing_agents(tmp):
    root = repo(tmp, "existing", {
        "AGENTS.md": f"# Existing\n\nIntro.\n\n## Entry points\n\n- app/main.py\n\n{SKILLS_LINE}\n\n{SKILLS_LINE}\n",
        "CLAUDE.md": "mine\n",
    })
    out = run(root)
    text = agents(root)
    assert text.count(SKILLS_LINE) == 1, text
    assert text.count("## Entry points") == 1 and "- app/main.py" in text, text
    assert "## Proof traps\n\nTODO:" in text, text
    assert "CLAUDE.md is a regular file; left it" in out, out
    assert (root / "CLAUDE.md").read_text() == "mine\n"
    assert "hooks not written; no stack detected" in out, out

    plain = repo(tmp, "plain", {"AGENTS.md": "# Plain\n\nIntro.\n\n## Git\n\nRules.\n"})
    run(plain)
    assert agents(plain).startswith(f"# Plain\n\nIntro.\n\n{SKILLS_LINE}\n\n## Git\n"), agents(plain)


def agents_outside(tmp):
    elsewhere = Path(tmp) / "elsewhere.md"
    elsewhere.write_text("x\n")
    root = repo(tmp, "outside", {})
    os.symlink(elsewhere, root / "AGENTS.md")
    out = run(root)
    assert "outside the repo; left it" in out, out
    assert not os.path.lexists(root / "CLAUDE.md")
    assert elsewhere.read_text() == "x\n"


def two_stacks_and_make(tmp):
    root = repo(tmp, "mixed", {
        "package.json": "{}",
        "go.mod": "module x\n",
        "Makefile": "X := a:b\nbuild:\n\tgo build\ntest check::\n\tgo test\n",
    })
    out = run(root)
    text = agents(root)
    assert "- Build: `make build`" in text and "- Test: `make test`" in text and "- Run: `TODO`" in text, text
    assert "hooks not written; saw js, go" in out, out


def existing_hooks(tmp):
    root = repo(tmp, "hooked", {
        "pyproject.toml": "",
        ".pre-commit-config.yaml": "repos:\n  - repo: https://github.com/psf/black\n    hooks:\n      - id: black\n",
    })
    out = run(root)
    assert "no linter" in out and "no secrets check" in out and "no formatter" not in out, out
    assert "black" in (root / ".pre-commit-config.yaml").read_text()


def husky(tmp):
    pkg = '{\n  "name": "web",\n  "packageManager": "pnpm@9.0.0",\n  "scripts": {"build": "vite build", "dev": "vite", "test": 3},\n  "devDependencies": {"husky": "9", "lint-staged": "15"}\n}\n'
    root = repo(tmp, "web", {"package.json": pkg}, git=True)
    out = run(root)
    hook = root / ".husky" / "pre-commit"
    assert os.access(hook, os.X_OK) and "gitleaks git --pre-commit --staged" in hook.read_text()
    new = (root / "package.json").read_text()
    assert new.startswith(pkg.rstrip()[:-1].rstrip()), new
    assert "lint-staged" in json.loads(new) and json.loads(new)["name"] == "web"
    hooks_path = subprocess.run(["git", "-C", str(root), "config", "core.hooksPath"], capture_output=True, text=True).stdout.strip()
    assert hooks_path == ".husky", hooks_path
    text = agents(root)
    assert "- Build: `pnpm run build`" in text and "- Test: `TODO`" in text and "- Run: `pnpm run dev`" in text, text
    again = run(root)
    assert "no formatter" not in again and "no linter" not in again and "no secrets check" not in again, again
    assert (root / "package.json").read_text() == new
    assert "set core.hooksPath" in out


def go_cmd(tmp):
    root = repo(tmp, "svc", {"go.mod": "module svc\n", "cmd/server/main.go": "package main\n", "cmd/lib/x.go": "package lib\n"})
    run(root)
    assert "- Run: `go run ./cmd/server`" in agents(root), agents(root)


def xcode(tmp):
    root = repo(tmp, "ios", {"My App.xcodeproj/xcshareddata/xcschemes/App.xcscheme": "<Scheme/>"})
    run(root)
    text = agents(root)
    assert '- Build: `xcodebuild -project "My App.xcodeproj" -scheme App build`' in text, text
    assert "swift-format" in (root / ".pre-commit-config.yaml").read_text()


def two_lockfiles(tmp):
    root = repo(tmp, "locks", {"package.json": '{"scripts": {"test": "jest"}}', "yarn.lock": "", "package-lock.json": ""})
    run(root)
    assert "- Test: `TODO`" in agents(root), agents(root)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        for case in (python_starter, existing_agents, agents_outside, two_stacks_and_make, existing_hooks, husky, go_cmd, xcode, two_lockfiles):
            case(tmp)
    print("ok")


if __name__ == "__main__":
    main()
