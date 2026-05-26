#!/usr/bin/env python3
"""Extend short descriptions by prepending a `<category-zh> · <subdir>:` tag.

Targets files flagged by `lint_skills.py` with rule `description-length`. The
extension keeps the original semantic content and only prepends a category
breadcrumb derived from the file path — never invents new copy.

If the result is still under 30 chars (extremely terse originals), the file
is flagged for manual editing rather than padded with filler.

Usage:
    python scripts/fix_descriptions.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

DIM_LABELS = {
    "design-pattern": "设计模式",
    "framework": "框架约定",
    "habit": "习惯",
    "lang": "语言规则",
}
DESC_MIN, DESC_MAX = 30, 80


def run_lint() -> dict:
    out = subprocess.run(
        [sys.executable, "scripts/lint_skills.py", "--json"],
        capture_output=True, text=True,
    )
    return json.loads(out.stdout)


def patch_file(path: Path, new_desc: str, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^(---\s*\n)(.*?)(\n---\s*\n?)", text, re.DOTALL)
    if not m:
        return False
    fm = yaml.safe_load(m.group(2)) or {}
    fm["description"] = new_desc
    new_fm = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).rstrip()
    new_text = "---\n" + new_fm + "\n---\n" + text[m.end():]
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--root", default="skills")
    args = ap.parse_args()

    report = run_lint()
    targets = [
        fp for fp, vs in report["violations_by_file"].items()
        if any(v["rule"] == "description-length" for v in vs)
    ]
    print(f"{len(targets)} files with description-length violations", file=sys.stderr)

    root = Path(args.root)
    patched = 0
    still_short: list[tuple[str, str]] = []
    for fp in sorted(targets):
        path = root / fp
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        fm = yaml.safe_load(m.group(1)) or {}
        desc = (fm.get("description") or "").strip()
        if len(desc) > DESC_MAX:
            # too long, not our concern here
            continue
        parts = fp.split("/")
        dim_label = DIM_LABELS.get(parts[0], parts[0])
        sub = parts[1] if len(parts) > 2 else parts[0]
        new_desc = f"{dim_label} · {sub}: {desc}"
        if len(new_desc) < DESC_MIN:
            still_short.append((fp, new_desc))
            continue
        if len(new_desc) > DESC_MAX:
            new_desc = new_desc[: DESC_MAX - 1] + "…"
        if patch_file(path, new_desc, args.dry_run):
            patched += 1
            verb = "would update" if args.dry_run else "updated"
            print(f"  {verb} {fp} ({len(desc)}→{len(new_desc)}) {new_desc}", file=sys.stderr)

    if still_short:
        print(f"\n  {len(still_short)} files still under {DESC_MIN} chars — edit manually:", file=sys.stderr)
        for fp, d in still_short:
            print(f"    {fp}: {len(d)} chars: {d}", file=sys.stderr)

    print(f"\n{patched} files patched", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
