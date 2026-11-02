# Stacks

Signals and pins for setup-base. Look at the root of the target repo only. Do not guess past this file.

The skills line is exactly:

```
Repo-specific skills live in `.agents/skills/`.
```

## AGENTS.md starter

```
# <directory name>

<what>

## Build & test

- Build: `<build>`
- Test: `<test>`
- Run: `<run>`

Repo-specific skills live in `.agents/skills/`.
```

`<what>` comes from the first of `README.md`, `README.rst`, and `README`. Skip a leading paragraph that is only images or badges. Use the first sentence of the next paragraph, or the first heading's text if there is no paragraph. No README: `TODO`. A sentence runs through the first `.`, `!`, or `?`, or is the whole paragraph if it has none. A `.` between two digits does not end it.

`<build>`, `<test>`, and `<run>` are one command each. A missing command is `TODO`.

A target in the root `Makefile` fills a column before the stack does. Do not read a file the Makefile includes. Build is `make build`, else `make all`. Test is `make test`, else `make check`. Run is `make run`. A target is a line whose name starts in column 1 and whose colon is not `:=`.

One stack fills whatever the Makefile did not. Two stacks leave those columns `TODO`.

| Stack | Build | Test | Run |
| --- | --- | --- | --- |
| js | runner build, else runner compile | runner test | runner start, else runner dev |
| python | `TODO` | `pytest` when that dependency is declared, or a `[tool.pytest` table exists | the only console script, else `TODO` |
| go | `go build ./...` | `go test ./...` | `go run .` when a root Go file's line is `package main`; else `go run ./cmd/<name>` when exactly one directory directly under cmd has such a file; else `TODO` |
| rust | `cargo build` | `cargo test` | `cargo run` when main.rs is in the src directory, or Cargo.toml has a `[[bin]]` table; else `TODO` |
| swift | `swift build`, or the xcodebuild line | `swift test`, or xcodebuild `test` | `swift run` when Package.swift contains `.executable`; else `TODO` |

A JS script counts only when its value is a string. `package.json` that does not parse: the JS columns are `TODO`.

JS runner, from `packageManager` (`pnpm@`, `yarn@`, `bun@`, `npm@`), else the one lockfile among `pnpm-lock.yaml`, `yarn.lock`, `bun.lock` or `bun.lockb`, and `package-lock.json`. No lockfile: npm. Two lockfiles and no `packageManager`: those columns are `TODO`.

| Runner | build / compile | test | start / dev |
| --- | --- | --- | --- |
| npm | `npm run build` / `npm run compile` | `npm test` | `npm start` / `npm run dev` |
| pnpm | `pnpm run build` / `pnpm run compile` | `pnpm test` | `pnpm start` / `pnpm run dev` |
| yarn | `yarn build` / `yarn compile` | `yarn test` | `yarn start` / `yarn dev` |
| bun | `bun run build` / `bun run compile` | `bun run test` | `bun run start` / `bun run dev` |

Python looks in `pyproject.toml` and `requirements.txt`. pytest counts when the dependency name is `pytest`, including optional, dependency-group, and poetry dependencies. Console scripts are the keys of `[project.scripts]` and `[tool.poetry.scripts]`. Prefix `uv run` when `uv.lock` exists. Otherwise prefix `poetry run` when `poetry.lock` exists or the file has a `[tool.poetry` table. Both locks: test and run are `TODO`.

Swift uses the Package.swift commands when that file exists. Otherwise, with exactly one root Xcode project or workspace and exactly one shared scheme, build is `xcodebuild -project <bundle> -scheme <scheme> build` and test is the same command with `test`. A shared scheme is an xcscheme file in that bundle's xcshareddata xcschemes directory. A workspace uses `-workspace`. Quote a name that contains a space. Any other build or test is `TODO`. Xcode run stays `TODO`.

## Hooks

Three kinds only: a formatter, a linter, and a secrets check. Prefer `.pre-commit-config.yaml`. Copy this shape. Do not add a fourth hook.

```yaml
repos:
  - repo: https://github.com/ORG/REPO
    rev: REV
    hooks:
      - id: HOOK
```

| Stack | Signal | Formatter | Linter | Secrets |
| --- | --- | --- | --- | --- |
| js | package.json | pre-commit/mirrors-prettier v3.1.0, id prettier | pre-commit/mirrors-eslint v10.14.0, id eslint, `files: '\.[jt]sx?$'`, `types: [file]` | gitleaks/gitleaks v8.30.1, id gitleaks |
| python | pyproject.toml, setup.py, setup.cfg, or requirements.txt | astral-sh/ruff-pre-commit v0.17.3, id ruff-format | same repo, id ruff-check | gitleaks/gitleaks v8.30.1, id gitleaks |
| go | go.mod | golangci/golangci-lint v2.15.0, id golangci-lint-fmt | same repo, id golangci-lint | gitleaks/gitleaks v8.30.1, id gitleaks |
| rust | Cargo.toml | doublify/pre-commit-rust v1.0, id fmt | same repo, id clippy | gitleaks/gitleaks v8.30.1, id gitleaks |
| swift | Package.swift, or a root Xcode project or workspace | swiftlang/swift-format 604.0.0, id swift-format | realm/SwiftLint 0.65.1, id swiftlint | gitleaks/gitleaks v8.30.1, id gitleaks |

The repo URL is `https://github.com/` plus the path in the cell. One repo entry holds both ids when the cell says same repo. Write formatter, then linter, then secrets.

No signal: write no config. Say `hooks not written; no stack detected`. More than one stack: write no config. Say `hooks not written; saw <stacks>` with the stack names in the table's order.

A JS repo whose parsed `package.json` depends on both `husky` and `lint-staged`, under `dependencies` or `devDependencies`, and that has no hook install, gets husky instead of the yaml. Write an executable `.husky/pre-commit`:

```
#!/bin/sh
npx lint-staged
gitleaks protect --staged --redact --no-banner
```

Add a `lint-staged` key and change no other key or line:

```json
"*.{js,jsx,ts,tsx,json,css,md,yml,yaml}": "prettier --write",
"*.{js,jsx,ts,tsx}": "eslint --fix"
```

In a git checkout, set `core.hooksPath` to `.husky` when it is empty.

## Already installed

Leave the install. Do not write another config. Report each missing kind, in this order: `no formatter`, `no linter`, `no secrets check`.

An install is any of these: `.pre-commit-config.yaml`, `.pre-commit-config.yml`, `lefthook.yml`, `lefthook.yaml`, `lefthook.toml`, `.lefthook.yml`, `.simple-git-hooks.json`, a `.husky` directory, a `lint-staged` or `simple-git-hooks` key in `package.json`, a non-empty `core.hooksPath`, or a file in `.git/hooks` whose name does not end in `.sample`. A sample hook is not an install.

Search only those files, the two `package.json` values, and the hooks directory when `core.hooksPath` resolves inside the repo. When that path is outside the repo, leave it, say `hooks path is outside the repo; left it`, and do not read it. If that was the only hook text, do not report a missing kind.

```
formatter: ruff-format|prettier|golangci-lint-fmt|swift-format(?!-lint)|\bblack\b|gofmt|go-fmt|rustfmt|cargo fmt|(?<![\w-])fmt(?![\w-])|\bbiome\b
linter: ruff-check|(?<![\w-])ruff(?![\w-])|eslint|swiftlint|swift-format-lint|clippy|flake8|pylint|golangci-lint(?!-fmt)|\bbiome\b
secrets: gitleaks|detect-secrets|trufflehog
```

## Edges

`CLAUDE.md` is missing only when that path has no directory entry. Create the link from the repo root, with target text `AGENTS.md`, so `readlink` prints `AGENTS.md`. Do not pass `-f`. A link that resolves to the repo's `AGENTS.md` is already correct, including `./AGENTS.md` and an absolute path. Do not retarget it.

`AGENTS.md` gets a starter only when that path has no directory entry. A file, or a symlink to a file inside the repo, is edited only to add or dedupe the skills line. Write back through the symlink; do not replace the symlink with a new file. A directory, a broken symlink, or a symlink that resolves outside the repo is left in place, and `CLAUDE.md` is not created. Say `AGENTS.md is not a file in the repo; left it`, or `AGENTS.md is a symlink to <target> outside the repo; left it`. `<target>` is `readlink`.

A regular `CLAUDE.md`: `CLAUDE.md is a regular file; left it`. A symlink to anything else: `CLAUDE.md is a symlink to <target>; left it`. A directory: `CLAUDE.md is a directory; left it`.
