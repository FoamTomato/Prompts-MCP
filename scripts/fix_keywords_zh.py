#!/usr/bin/env python3
"""Append Chinese keyword candidates extracted from the description.

Strategy:
  - For each file missing a Chinese keyword, scan its `description`.
  - Pull connected CJK runs (2-6 chars). Drop common stopwords and runs that
    already appear (case-folded) in existing keywords.
  - Add the top-N (default 3) as additional `triggers.keywords` entries.

This is a best-effort batch tool. Run lint after and review the diff before
committing — descriptions sometimes contain incidental Chinese (proper nouns,
class names) that aren't useful search terms. Re-edit those manually.

Usage:
    python scripts/fix_keywords_zh.py [--dry-run] [--max 3] [--root skills]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

# Match runs of contiguous Han characters; we filter by length later
CJK_RUN_RE = re.compile(r"[一-鿿]+")
# Tokens that look like keywords but are too generic to add automatically
STOP = {
    "示范", "示例", "约定", "规则", "规范", "模板", "用法", "场景",
    "提示", "说明", "情况", "时候", "时机", "对象", "进行",
    "等等", "以及", "或者", "之后", "之前", "之间",
    "必带", "只做", "禁在", "必须", "用于", "包裹", "捕获", "中间件",
    "组件", "中文描述", "消息里", "客户端", "服务端",
    "插件", "降级", "类设计", "工厂", "独立", "分桶", "回源",
    "缓存", "重试", "变量", "系统", "圆角", "颜色", "安装",
    "禁用", "受控", "字段", "终止", "渲染", "协议",
}


def cjk_candidates(text: str, existing: set[str], strict: bool = True) -> list[str]:
    """Return CJK phrases that look like meaningful keywords.

    Accept whole CJK runs of length 2-6 as-is. For runs ≥7 chars, slide a
    2-4 char window across them (longer runs are usually mid-sentence
    fragments without natural word boundaries, so we grab the most
    informative-looking sub-spans rather than the whole thing).

    `strict=True` drops STOP-list generics. Lax fallback skips that filter.
    """
    out: list[str] = []
    seen: set[str] = {k.lower() for k in existing}

    def offer(tok: str) -> None:
        if not (2 <= len(tok) <= 6):
            return
        if strict and tok in STOP:
            return
        if tok.lower() in seen:
            return
        seen.add(tok.lower())
        out.append(tok)

    for m in CJK_RUN_RE.finditer(text):
        run = m.group()
        if 2 <= len(run) <= 6:
            offer(run)
        elif len(run) >= 7:
            # Slide 2/3/4-char windows in that order — try the most distinctive
            # 4-char chunks first, then 3, then 2.
            for win in (4, 3, 2):
                for i in range(len(run) - win + 1):
                    offer(run[i : i + win])
    return out


def run_lint() -> dict:
    out = subprocess.run(
        [sys.executable, "scripts/lint_skills.py", "--json"],
        capture_output=True, text=True,
    )
    return json.loads(out.stdout)


def patch_file(path: Path, new_keywords: list[str], dry_run: bool) -> tuple[int, str] | None:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^(---\s*\n)(.*?)(\n---\s*\n?)", text, re.DOTALL)
    if not m:
        return None
    fm_raw = m.group(2)
    fm = yaml.safe_load(fm_raw) or {}
    triggers = fm.get("triggers") or {}
    if not isinstance(triggers, dict):
        return None
    kws = triggers.get("keywords")
    if not isinstance(kws, list):
        kws = []

    # Dedup-preserve and append
    existing_lc = {str(k).lower() for k in kws}
    added = []
    for k in new_keywords:
        if k.lower() not in existing_lc:
            kws.append(k)
            existing_lc.add(k.lower())
            added.append(k)
    if not added:
        return None

    triggers["keywords"] = kws
    fm["triggers"] = triggers

    new_fm = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).rstrip()
    new_text = "---\n" + new_fm + "\n---\n" + text[m.end():]

    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return len(added), ", ".join(added)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="skills")
    ap.add_argument("--max", type=int, default=3, help="max keywords to add per file")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    report = run_lint()
    targets = [
        fp for fp, vs in report["violations_by_file"].items()
        if any(v["rule"] == "keywords-no-chinese" for v in vs)
    ]
    print(f"{len(targets)} files missing Chinese keywords", file=sys.stderr)

    root = Path(args.root)
    patched = 0
    skipped = 0
    for fp in sorted(targets):
        path = root / fp
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        fm = yaml.safe_load(m.group(1)) or {}
        desc = fm.get("description", "") or ""
        existing = (fm.get("triggers") or {}).get("keywords") or []
        existing = [str(k) for k in existing if isinstance(k, (str, int, float))]
        cands = cjk_candidates(desc, set(existing), strict=True)[: args.max]
        if not cands:
            # Fall back to permissive: take any CJK 2-6 token. Better an
            # imperfect keyword than a lint violation. The reviewer should
            # check these in the diff.
            cands = cjk_candidates(desc, set(existing), strict=False)[: args.max]
            if cands:
                print(f"  FALLBACK {fp}: lax pick {cands}", file=sys.stderr)
        if not cands:
            # Truly nothing — file's description has no CJK at all. Need
            # manual edit. Surface clearly.
            skipped += 1
            print(f"  SKIP {fp} — no CJK in desc={desc!r}", file=sys.stderr)
            continue
        result = patch_file(path, cands, args.dry_run)
        if result:
            n_added, what = result
            patched += 1
            verb = "would add" if args.dry_run else "added"
            print(f"  {verb:9s} {n_added} to {fp}: [{what}]", file=sys.stderr)
        else:
            skipped += 1
    print(f"\n{patched} files patched, {skipped} skipped", file=sys.stderr)
    return 0 if patched else 1


if __name__ == "__main__":
    sys.exit(main())
