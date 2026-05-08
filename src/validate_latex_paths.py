"""
Validate that report .tex files stay self-contained inside reports/.

The reports/ directory is intended to be portable: a collaborator should be
able to copy reports/ alone and compile the LaTeX docs. This requires:

  1. No `../` parent-directory traversal in .tex paths.
  2. No `_output/` references (those should resolve via reports/output/).
  3. No `_data/` references (raw data has no place in a paper).

The check ignores LaTeX comments and fails the build on any violation.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = REPO_ROOT / "reports"

TEX_FILES = [
    REPORTS_DIR / "draft_ftsfr.tex",
    REPORTS_DIR / "slides_ftsfr.tex",
    REPORTS_DIR / "internet_appendix.tex",
]

# Forbidden path-like markers. Trailing `/` keeps us from flagging
# legitimate identifiers like `_dataset`, `get_data_requirements`,
# or URLs like `time_series_data_2018/` (where `_data` is followed by
# `_2018`, not `/`). `../` blocks any parent-directory traversal so
# reports/ stays self-contained.
FORBIDDEN_TOKENS = ["../", "_output/", "_data/"]


def strip_comments_line(line: str) -> str:
    """Strip everything after an unescaped `%` on a single line."""
    out = []
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == "\\" and i + 1 < len(line):
            out.append(line[i : i + 2])
            i += 2
            continue
        if ch == "%":
            break
        out.append(ch)
        i += 1
    return "".join(out)


def check_file(tex_path: Path) -> list[tuple[int, str, str]]:
    """Return list of (lineno, token, line) hits in `tex_path`."""
    hits: list[tuple[int, str, str]] = []
    if not tex_path.exists():
        return hits
    for lineno, line in enumerate(
        tex_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        code = strip_comments_line(line)
        for token in FORBIDDEN_TOKENS:
            if token in code:
                hits.append((lineno, token, line.rstrip()))
                break
    return hits


def main() -> int:
    failures: list[tuple[Path, list[tuple[int, str, str]]]] = []
    for tex in TEX_FILES:
        hits = check_file(tex)
        if hits:
            failures.append((tex, hits))

    if failures:
        print(
            "ERROR: report .tex files reference forbidden paths.",
            file=sys.stderr,
        )
        for tex, hits in failures:
            rel = tex.relative_to(REPO_ROOT)
            for lineno, token, line in hits:
                print(f"  {rel}:{lineno}  contains '{token}': {line}", file=sys.stderr)
        print(
            "\nThe reports/ directory should be self-contained. Cache artifacts\n"
            "into reports/output/ and reports/docs_src/ via:\n"
            "    python src/cache_latex_artifacts.py\n"
            "and reference them from .tex files using \\PathToOutput (=./output)\n"
            "and \\PathToAssets (=./docs_src).",
            file=sys.stderr,
        )
        return 1

    checked = ", ".join(t.name for t in TEX_FILES if t.exists())
    forbidden = ", ".join(repr(t) for t in FORBIDDEN_TOKENS)
    print(f"OK: no {forbidden} references in {checked}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
