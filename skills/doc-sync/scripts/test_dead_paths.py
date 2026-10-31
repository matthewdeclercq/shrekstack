#!/usr/bin/env python3
"""Proves bare-type lookup and the skipped missing-directory path.

`Widget` is declared as `class Widget` in src/models.py. There is no file
named Widget and no extension is appended. `MissingType` has no declaration.
`GoneDir/Weather` stays unreported even though that path does not exist.
`--code-root` overrides the AGENTS.md `Code roots` list. With neither, bare
type names are not checked.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("dead-paths.py")


def run(root, *args):
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root), *args],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def main():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "src").mkdir()
        (root / "other").mkdir()
        (root / "src" / "models.py").write_text("class Widget:\n    pass\n", encoding="utf-8")
        (root / "docs").mkdir()
        (root / "docs" / "guide.md").write_text(
            "\n".join(
                [
                    "Defined `Widget`.",
                    "Missing `MissingType`.",
                    "Gone directory `GoneDir/Weather`.",
                    "Live `src/models.py`.",
                    "Dead file `src/missing.py`.",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        (root / "AGENTS.md").write_text(
            "# Notes\n\n## Code roots\n\n- src\n\n## Other\n\n- not-a-root\n",
            encoding="utf-8",
        )

        code, out, err = run(root, "--doc-folder", "docs")
        assert code == 1, (code, out, err)
        assert "Widget" not in out.split(), out
        assert any(line.endswith(": MissingType") for line in out.splitlines()), out
        assert "GoneDir/Weather" not in out, out
        assert "src/models.py" not in out, out
        assert "src/missing.py" in out, out
        assert list((root / "src").glob("Widget.*")) == []

        code_over, out_over, err_over = run(root, "--doc-folder", "docs", "--code-root", "other")
        assert code_over == 1, (code_over, out_over, err_over)
        assert any(line.endswith(": Widget") for line in out_over.splitlines()), out_over
        assert "GoneDir/Weather" not in out_over, out_over

        agents = (root / "AGENTS.md").read_text(encoding="utf-8")
        (root / "AGENTS.md").write_text(agents.replace("## Code roots\n\n- src\n\n", ""))
        code_none, out_none, err_none = run(root, "--doc-folder", "docs")
        assert code_none == 1, (code_none, out_none, err_none)
        assert "MissingType" not in out_none, out_none
        assert "Widget" not in out_none, out_none
        assert "src/missing.py" in out_none, out_none
        assert "GoneDir/Weather" not in out_none, out_none

    print("ok")


if __name__ == "__main__":
    main()
