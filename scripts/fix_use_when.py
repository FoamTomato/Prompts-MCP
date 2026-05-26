#!/usr/bin/env python3
"""Suggest / append 'Use when ...' clause to skill descriptions missing one.

Strategy:
  - Read each leaf skill's frontmatter; skip if description already contains
    "Use when".
  - Strip the legacy "<dim> · <sub>: " breadcrumb prefix (now considered
    waste — see Matt-style description guidance).
  - Build a "Use when ..." candidate from:
      1. Verb-form templates derived from `paths` (e.g. *.tsx → "写 React 组件")
      2. Up to 2 user-facing keywords from `triggers.keywords`
      3. Generic "评审 <topic> PR" closer
  - Replace `description`. Output a unified diff in dry-run mode for review.

This produces *machine-generated* triggers — review the diff before commit.
Quality varies; for the high-value 10–20 skills you regularly hit, hand-edit
instead.

Usage:
    python scripts/fix_use_when.py --dry-run > /tmp/use-when.diff
    git apply --3way /tmp/use-when.diff      # or apply selectively
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

import yaml

BREADCRUMB_RE = re.compile(r"^(设计模式|框架约定|习惯|语言规则) · [a-z0-9-]+:\s*")

# Path glob → verb-phrase mapping for Use when 第一段
PATH_VERBS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\.tsx$"), "写 React 组件 / 改 .tsx 文件"),
    (re.compile(r"frontend/.*\.ts$"), "写 TS 业务代码"),
    (re.compile(r"backend/.*\.py$"), "写 Python 后端代码"),
    (re.compile(r"backend/services/"), "写 Service 层"),
    (re.compile(r"backend/models/"), "写 Tortoise Model"),
    (re.compile(r"backend/api/"), "写 FastAPI router"),
    (re.compile(r"\.sql$"), "写 SQL / 迁移脚本"),
    (re.compile(r"\.java$"), "写 Java 代码"),
    (re.compile(r"\.js$"), "写 JavaScript 代码"),
    (re.compile(r"project-index/modules/"), "改子模块 PRD"),
    (re.compile(r"\.github/"), "改 CI / workflow"),
    (re.compile(r"skills/"), "新建或修改 skill"),
]


def derive_use_when(fm: dict, file_name: str = "") -> str:
    """Build a Use when candidate phrase from frontmatter paths + name.

    Conservative — generates only safe, well-formed verb phrases. Anything
    that needs domain-specific phrasing should be hand-edited.
    """
    parts: list[str] = []

    # 1. paths-based verb phrase (most reliable signal)
    paths = fm.get("paths") or []
    verb_phrases = []
    for p in paths:
        for pat, phrase in PATH_VERBS:
            if pat.search(str(p)):
                if phrase not in verb_phrases:
                    verb_phrases.append(phrase)
                break
    if verb_phrases:
        parts.append(verb_phrases[0])

    # 2. file-name-derived second clause (kebab-case → human phrase).
    # Skip if the name is too short to be meaningful.
    if file_name:
        # strip directory and suffix
        stem = Path(file_name).stem
        if "-" in stem and len(stem) >= 6:
            parts.append(f"评审涉及 `{stem}` 的 PR")
            return "Use when " + " / ".join(parts) + "。"

    # 3. generic closer
    parts.append("评审 PR 时")
    return "Use when " + " / ".join(parts) + "。"


def upgrade_description(fm: dict, file_name: str) -> tuple[str, str] | None:
    """Return (old_desc, new_desc) or None if no change."""
    desc = (fm.get("description") or "").strip()
    if not desc:
        return None
    if "Use when" in desc:
        return None
    # Strip breadcrumb prefix
    desc_clean = BREADCRUMB_RE.sub("", desc).rstrip("。").rstrip()
    use_when = derive_use_when(fm, file_name)
    new = f"{desc_clean}。{use_when}"
    # Don't blow past lint cap
    if len(new) > 150:
        # Drop the file-name reference if it pushed us over
        new = f"{desc_clean}。Use when 评审 PR 时。"
    return desc, new


def process(path: Path, dry_run: bool) -> tuple[str, str, str] | None:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^(---\s*\n)(.*?)(\n---\s*\n?)", text, re.DOTALL)
    if not m:
        return None
    fm = yaml.safe_load(m.group(2)) or {}
    pair = upgrade_description(fm, path.name)
    if not pair:
        return None
    old_desc, new_desc = pair
    fm["description"] = new_desc
    new_fm = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).rstrip()
    new_text = "---\n" + new_fm + "\n---\n" + text[m.end():]
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return path.as_posix(), old_desc, new_desc


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="skills")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=999, help="cap files processed")
    args = ap.parse_args()

    root = Path(args.root)
    targets = sorted(root.rglob("*.md"))
    targets = [p for p in targets if not p.name.endswith((".examples.md", ".reference.md"))]
    targets = [p for p in targets if p.name != "index.md"]

    processed = 0
    skipped = 0
    for path in targets:
        if processed >= args.limit:
            break
        result = process(path, args.dry_run)
        if not result:
            skipped += 1
            continue
        rel, old, new = result
        verb = "would update" if args.dry_run else "updated"
        print(f"\n{verb} {rel}")
        print(f"  - {old}")
        print(f"  + {new}")
        processed += 1

    print(f"\n{processed} files {'previewed' if args.dry_run else 'patched'}, {skipped} skipped.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
