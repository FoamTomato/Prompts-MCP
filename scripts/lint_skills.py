#!/usr/bin/env python3
"""Lint skill markdown files against the Prompts-MCP frontmatter standard.

Run: python scripts/lint_skills.py [--json] [--root <path>]
Exit code 0 if clean, 1 if any violations found.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)

LEAF_REQUIRED_FIELDS = ["name", "description", "parent", "paths", "triggers", "effort", "version"]
INDEX_REQUIRED_FIELDS = ["name", "description", "parent", "children"]
EFFORT_VALUES = {"low", "medium", "high"}
DESC_MIN, DESC_MAX = 30, 80
KEYWORDS_MIN = 3
CHINESE_RE = re.compile(r"[一-鿿]")
ENGLISH_RE = re.compile(r"[A-Za-z]{2,}")


@dataclass
class Violation:
    path: str
    rule: str
    detail: str

    def __str__(self) -> str:
        return f"  [{self.rule}] {self.detail}"


@dataclass
class Report:
    total_files: int = 0
    leaf_files: int = 0
    index_files: int = 0
    violations: list[Violation] = field(default_factory=list)

    def add(self, path: Path, rule: str, detail: str, root: Path) -> None:
        rel = path.relative_to(root).as_posix()
        self.violations.append(Violation(path=rel, rule=rule, detail=detail))

    @property
    def clean(self) -> bool:
        return not self.violations

    def to_dict(self) -> dict:
        by_file: dict[str, list[dict]] = {}
        for v in self.violations:
            by_file.setdefault(v.path, []).append({"rule": v.rule, "detail": v.detail})
        return {
            "total_files": self.total_files,
            "leaf_files": self.leaf_files,
            "index_files": self.index_files,
            "violation_count": len(self.violations),
            "files_with_violations": len(by_file),
            "violations_by_file": by_file,
        }


def parse_frontmatter(text: str) -> tuple[dict | None, str | None]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, "missing frontmatter (no leading `---` block)"
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        return None, f"invalid YAML: {e}"
    if not isinstance(data, dict):
        return None, "frontmatter is not a YAML mapping"
    return data, None


def lint_leaf(path: Path, fm: dict, report: Report, root: Path) -> None:
    for f in LEAF_REQUIRED_FIELDS:
        if f not in fm:
            report.add(path, "missing-field", f"required field `{f}` is absent", root)

    desc = fm.get("description")
    if isinstance(desc, str):
        length = len(desc.strip())
        if length < DESC_MIN or length > DESC_MAX:
            report.add(
                path,
                "description-length",
                f"description is {length} chars; must be {DESC_MIN}-{DESC_MAX}",
                root,
            )

    triggers = fm.get("triggers") or {}
    keywords = triggers.get("keywords") if isinstance(triggers, dict) else None
    if not isinstance(keywords, list):
        report.add(path, "keywords-missing", "triggers.keywords must be a list", root)
    else:
        if len(keywords) < KEYWORDS_MIN:
            report.add(
                path,
                "keywords-too-few",
                f"only {len(keywords)} keyword(s); need ≥{KEYWORDS_MIN}",
                root,
            )
        has_zh = any(CHINESE_RE.search(str(k)) for k in keywords)
        has_en = any(ENGLISH_RE.search(str(k)) for k in keywords)
        if not has_zh:
            report.add(path, "keywords-no-chinese", "no Chinese term in triggers.keywords", root)
        if not has_en:
            report.add(path, "keywords-no-english", "no English term in triggers.keywords", root)

    effort = fm.get("effort")
    if effort not in EFFORT_VALUES:
        report.add(path, "effort-invalid", f"effort=`{effort}`; must be one of {sorted(EFFORT_VALUES)}", root)

    paths = fm.get("paths")
    if not isinstance(paths, list) or not paths:
        report.add(path, "paths-empty", "`paths` must be a non-empty list of globs", root)

    parent = fm.get("parent")
    if parent and isinstance(parent, str):
        resolved = (path.parent / parent).resolve()
        if not resolved.exists():
            report.add(path, "parent-missing", f"parent `{parent}` does not resolve", root)


def lint_index(path: Path, fm: dict, report: Report, root: Path) -> None:
    for f in INDEX_REQUIRED_FIELDS:
        if f not in fm:
            report.add(path, "missing-field", f"required field `{f}` is absent", root)

    children = fm.get("children")
    if not isinstance(children, list):
        return

    declared = set()
    for ch in children:
        if not isinstance(ch, dict):
            report.add(path, "children-bad-entry", f"child is not a mapping: {ch!r}", root)
            continue
        cp = ch.get("path")
        if not cp:
            report.add(path, "children-missing-path", f"child has no `path`: {ch!r}", root)
            continue
        declared.add(cp)
        resolved = (path.parent / cp).resolve()
        if not resolved.exists():
            report.add(path, "child-not-found", f"declared child `{cp}` does not exist on disk", root)

    actual: set[str] = set()
    for entry in path.parent.iterdir():
        if entry.name.startswith(".") or entry.name == "index.md":
            continue
        if entry.is_dir():
            actual.add(f"{entry.name}/index.md")
        elif entry.suffix == ".md":
            actual.add(entry.name)

    missing_in_decl = actual - declared
    extra_in_decl = declared - actual
    for m in sorted(missing_in_decl):
        report.add(path, "children-out-of-sync", f"disk has `{m}` not declared in children", root)
    for e in sorted(extra_in_decl):
        report.add(path, "children-out-of-sync", f"children declares `{e}` not on disk", root)


def lint_file(path: Path, report: Report, root: Path) -> None:
    report.total_files += 1
    is_index = path.name == "index.md"
    if is_index:
        report.index_files += 1
    else:
        report.leaf_files += 1

    text = path.read_text(encoding="utf-8")
    fm, err = parse_frontmatter(text)
    if fm is None:
        report.add(path, "frontmatter", err or "unknown parse error", root)
        return

    if is_index:
        lint_index(path, fm, report, root)
    else:
        lint_leaf(path, fm, report, root)


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint skill markdown files")
    ap.add_argument("--root", default="skills", help="path to skills root (default: skills)")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"skills root not found: {root}", file=sys.stderr)
        return 2

    report = Report()
    for md in sorted(root.rglob("*.md")):
        lint_file(md, report, root)

    if args.json:
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(
            f"Scanned {report.total_files} files "
            f"({report.leaf_files} leaf, {report.index_files} index)."
        )
        if report.clean:
            print("All clean.")
        else:
            by_file: dict[str, list[Violation]] = {}
            for v in report.violations:
                by_file.setdefault(v.path, []).append(v)
            for fpath, vs in sorted(by_file.items()):
                print(f"\n{fpath}")
                for v in vs:
                    print(str(v))
            print(
                f"\n{len(report.violations)} violations across {len(by_file)} files."
            )

    return 0 if report.clean else 1


if __name__ == "__main__":
    sys.exit(main())
