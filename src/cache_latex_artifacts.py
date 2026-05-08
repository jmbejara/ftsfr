"""
Cache LaTeX-referenced artifacts into reports/output/ and reports/docs_src/.

The reports/ directory is intended to be self-contained and shareable: a
collaborator can copy reports/ alone and compile the LaTeX documents without
the rest of the repo. This script extracts the set of files actually
referenced by reports/*.tex (via \\input{...} and \\includegraphics{...})
and copies them from the source-of-truth locations:

  ./_output/   (gitignored pipeline output)  ->  ./reports/output/
  ./docs_src/  (committed static images)     ->  ./reports/docs_src/

Only the referenced subset is cached; stale files in the cache are pruned.

Run this after a full pipeline refresh, before committing changes to
reports/output/ and reports/docs_src/.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = REPO_ROOT / "reports"
SOURCE_OUTPUT = REPO_ROOT / "_output"
SOURCE_DOCS_SRC = REPO_ROOT / "docs_src"
CACHE_OUTPUT = REPORTS_DIR / "output"
CACHE_DOCS_SRC = REPORTS_DIR / "docs_src"

TEX_FILES = [
    REPORTS_DIR / "draft_ftsfr.tex",
    REPORTS_DIR / "slides_ftsfr.tex",
    REPORTS_DIR / "internet_appendix.tex",
]

# Extensions LaTeX probes when \includegraphics has no extension.
GRAPHICS_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg"]

NEWCOMMAND_RE = re.compile(
    r"\\newcommand\*?\s*\{\\(?P<name>[A-Za-z]+)\}\s*\{(?P<value>[^}]*)\}"
)
INPUT_RE = re.compile(r"\\input\s*\{([^}]+)\}")
INCLUDEGRAPHICS_RE = re.compile(
    r"\\includegraphics\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}"
)


def strip_comments(tex: str) -> str:
    """Drop LaTeX comments so commented-out references don't pollute the cache.

    Treat a `%` as a comment introducer unless escaped as `\\%`.
    """
    out_lines = []
    for line in tex.splitlines():
        stripped = []
        i = 0
        while i < len(line):
            ch = line[i]
            if ch == "\\" and i + 1 < len(line):
                stripped.append(line[i : i + 2])
                i += 2
                continue
            if ch == "%":
                break
            stripped.append(ch)
            i += 1
        out_lines.append("".join(stripped))
    return "\n".join(out_lines)


def parse_path_macros(tex: str) -> dict[str, str]:
    """Return {macro_name: value} for \\newcommand definitions in the file."""
    return {m.group("name"): m.group("value") for m in NEWCOMMAND_RE.finditer(tex)}


def expand_macros(path: str, macros: dict[str, str]) -> str:
    """Expand `\\Foo` and `\\Foo/...` macro references in a path string."""
    for _ in range(8):  # bounded loop in case of nested defs
        before = path
        for name, value in macros.items():
            path = re.sub(rf"\\{name}\b", value, path)
        if path == before:
            break
    return path


def resolve_path(raw: str, tex_path: Path, macros: dict[str, str]) -> Path:
    """Resolve a raw \\input/\\includegraphics target to an absolute path.

    The .tex files reference reports/output/ and reports/docs_src/ (the
    caches), but the source-of-truth artifacts live in ./_output/ and
    ./docs_src/ respectively. Rewrite the cache paths back to the source so
    the extractor reads from the live artifacts, not from a stale cache
    copy of itself.
    """
    expanded = expand_macros(raw, macros).strip()
    p = Path(expanded)
    if not p.is_absolute():
        p = (tex_path.parent / p).resolve()
    if is_under(p, CACHE_OUTPUT):
        p = SOURCE_OUTPUT / p.relative_to(CACHE_OUTPUT)
    elif is_under(p, CACHE_DOCS_SRC):
        p = SOURCE_DOCS_SRC / p.relative_to(CACHE_DOCS_SRC)
    return p


def find_with_extension(path: Path) -> Path | None:
    """If `path` exists, return it; otherwise probe known graphics extensions."""
    if path.suffix and path.exists():
        return path
    if not path.suffix:
        for ext in GRAPHICS_EXTENSIONS:
            candidate = path.with_suffix(ext)
            if candidate.exists():
                return candidate
    if path.exists():
        return path
    return None


def collect_references(
    tex_path: Path, visited: set[Path] | None = None
) -> tuple[list[Path], list[str]]:
    """Walk a .tex file (and recursively any \\input'd .tex files) for refs.

    Returns (resolved_paths, missing_raw_targets).
    """
    if visited is None:
        visited = set()
    if tex_path in visited:
        return [], []
    visited.add(tex_path)

    if not tex_path.exists():
        return [], [f"{tex_path} (tex file not found)"]

    raw_text = tex_path.read_text(encoding="utf-8")
    text = strip_comments(raw_text)
    macros = parse_path_macros(raw_text)

    resolved: list[Path] = []
    missing: list[str] = []

    for match in INPUT_RE.finditer(text):
        target = match.group(1)
        path = resolve_path(target, tex_path, macros)
        # \input may omit .tex extension
        if not path.suffix:
            path = path.with_suffix(".tex")
        if path.exists():
            resolved.append(path)
            if path.suffix == ".tex":
                sub_resolved, sub_missing = collect_references(path, visited)
                resolved.extend(sub_resolved)
                missing.extend(sub_missing)
        else:
            missing.append(f"{target}  (resolved: {path})  in {tex_path.name}")

    for match in INCLUDEGRAPHICS_RE.finditer(text):
        target = match.group(1)
        path = resolve_path(target, tex_path, macros)
        found = find_with_extension(path)
        if found is not None:
            resolved.append(found)
        else:
            missing.append(f"{target}  (resolved: {path})  in {tex_path.name}")

    return resolved, missing


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def copy_file(src: Path, rel: Path, dest_root: Path) -> Path:
    dest = dest_root / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    return dest


def clear_stale(cache_root: Path, kept: set[Path]) -> list[Path]:
    """Remove files in cache_root not present in `kept`. Prune empty dirs."""
    removed: list[Path] = []
    if not cache_root.exists():
        return removed
    for path in sorted(cache_root.rglob("*")):
        if path.is_file() and path not in kept:
            path.unlink()
            removed.append(path)
    # prune empty directories bottom-up
    for path in sorted(cache_root.rglob("*"), reverse=True):
        if path.is_dir() and not any(path.iterdir()):
            path.rmdir()
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would be copied without writing.",
    )
    args = parser.parse_args()

    if not SOURCE_OUTPUT.exists():
        print(
            f"ERROR: source directory {SOURCE_OUTPUT} does not exist. "
            "Run the data/forecasting pipeline before refreshing the cache.",
            file=sys.stderr,
        )
        return 2
    if not SOURCE_DOCS_SRC.exists():
        print(
            f"ERROR: source directory {SOURCE_DOCS_SRC} does not exist.",
            file=sys.stderr,
        )
        return 2

    all_resolved: list[tuple[Path, Path]] = []  # (source_tex, resolved_target)
    all_missing: list[str] = []
    for tex in TEX_FILES:
        resolved, missing = collect_references(tex)
        for r in resolved:
            all_resolved.append((tex, r))
        all_missing.extend(missing)

    if all_missing:
        print("ERROR: unresolved LaTeX references:", file=sys.stderr)
        for m in all_missing:
            print(f"  - {m}", file=sys.stderr)
        return 1

    # Bucket each resolved path by which cache it belongs to.
    output_pairs: list[tuple[Path, Path]] = []   # (source, rel) for reports/output/
    docs_src_pairs: list[tuple[Path, Path]] = [] # (source, rel) for reports/docs_src/
    for tex, path in all_resolved:
        if is_under(path, SOURCE_OUTPUT):
            output_pairs.append((path, path.relative_to(SOURCE_OUTPUT)))
        elif is_under(path, SOURCE_DOCS_SRC):
            docs_src_pairs.append((path, path.relative_to(SOURCE_DOCS_SRC)))
        elif is_under(path, REPORTS_DIR):
            # Files already in reports/ (logos, bibliography) need no caching.
            continue
        else:
            print(
                f"WARNING: reference outside _output/, docs_src/, reports/: {path}",
                file=sys.stderr,
            )

    # De-duplicate (a file referenced by both draft and slides).
    def dedupe(pairs: list[tuple[Path, Path]]) -> list[tuple[Path, Path]]:
        seen: dict[Path, Path] = {}
        for src, rel in pairs:
            seen[rel] = src
        return sorted(seen.items(), key=lambda kv: kv[0])

    output_unique = dedupe(output_pairs)
    docs_src_unique = dedupe(docs_src_pairs)

    if args.dry_run:
        print(
            f"Would copy {len(output_unique)} files to {CACHE_OUTPUT}/:"
        )
        for rel, src in output_unique:
            print(f"  {src}  ->  {CACHE_OUTPUT / rel}")
        print(
            f"Would copy {len(docs_src_unique)} files to {CACHE_DOCS_SRC}/:"
        )
        for rel, src in docs_src_unique:
            print(f"  {src}  ->  {CACHE_DOCS_SRC / rel}")
        return 0

    def populate(
        cache_root: Path, pairs: list[tuple[Path, Path]]
    ) -> tuple[int, list[Path]]:
        cache_root.mkdir(parents=True, exist_ok=True)
        kept: set[Path] = set()
        for rel, src in pairs:
            dest = copy_file(src, rel, cache_root)
            kept.add(dest.resolve())
        removed = clear_stale(cache_root, kept)
        return len(pairs), removed

    n_out, removed_out = populate(CACHE_OUTPUT, output_unique)
    n_docs, removed_docs = populate(CACHE_DOCS_SRC, docs_src_unique)

    print(f"Cached {n_out} files into {CACHE_OUTPUT}/")
    print(f"Cached {n_docs} files into {CACHE_DOCS_SRC}/")
    for cache_root, removed in (
        (CACHE_OUTPUT, removed_out),
        (CACHE_DOCS_SRC, removed_docs),
    ):
        if removed:
            print(f"Removed {len(removed)} stale files from {cache_root}/:")
            for r in removed:
                print(f"  - {r.relative_to(cache_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
