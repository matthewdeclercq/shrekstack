#!/usr/bin/env python3
"""Proves repeats.py flags a README/AGENTS.md repeat, a root/nested repeat, and a pointer line.

It must not flag a short line, a heading, a line in a skipped README, or a
nested README against the root AGENTS.md.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("repeats.py")


def run(root, *args):
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root), *args],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write(root / "AGENTS.md", "# Repo\n\n## Build\n\n- Run `make test` before every push.\n- Short line.\n")
        write(root / "api" / "AGENTS.md", "## Build\n\n* run `make test` before every push!\n- Deploy with `fly deploy` from api.\n")
        write(root / "api" / "README.md", "# api\n\n- Deploy with `fly deploy` from api.\n- Short line.\n")
        write(root / "web" / "README.md", "- Run `make test` before every push.\n- See web/AGENTS.md for the commands.\n")
        write(root / "ext" / "README.md", "- Please read the AGENTS.md first.\n")

        code, out, err = run(root, "--skip", "ext")
        lines = out.splitlines()
        assert code == 1, (code, out, err)
        assert any(l.startswith("api/AGENTS.md:3: repeats AGENTS.md:5:") for l in lines), out
        assert any(l.startswith("api/README.md:3: repeats api/AGENTS.md:4:") for l in lines), out
        assert any(l.startswith("web/README.md:2: pointer:") for l in lines), out
        assert "Short line" not in out, out
        assert "ext/" not in out, out
        assert not any(l.startswith("web/README.md:1:") for l in lines), out
        assert len(lines) == 3, out

        code, out, err = run(root, "--skip", "ext", "--skip", "api", "--skip", "web")
        assert code == 0 and out.startswith("Clean: 1 files."), (code, out, err)

    print("ok")


if __name__ == "__main__":
    main()
