#!/usr/bin/env python3
"""End-to-end smoke test for a running Prompts-MCP instance.

Hits HTTP endpoints (/health, /web/, /web/api/search) and exercises each of
the 7 tools' pure functions directly. Exits non-zero on the first failure.

Usage:
    python scripts/verify.py [--base http://localhost:8080]
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))

from prompts_mcp.indexes import SkillIndex
from prompts_mcp.loader import load_skills
from prompts_mcp.tools.get_index_tree import get_index_tree
from prompts_mcp.tools.get_skill import get_skill
from prompts_mcp.tools.get_skill_bundle import get_skill_bundle
from prompts_mcp.tools.list_skills import list_skills
from prompts_mcp.tools.match_task_skills import match_task_skills
from prompts_mcp.tools.pick_design_skills import pick_design_skills
from prompts_mcp.tools.search_skills import search_skills


GREEN = "\033[32m"
RED = "\033[31m"
DIM = "\033[2m"
RESET = "\033[0m"


def _say_ok(label: str, detail: str = "") -> None:
    print(f"{GREEN}✓{RESET} {label}{DIM}  {detail}{RESET}")


def _say_fail(label: str, detail: str) -> int:
    print(f"{RED}✗{RESET} {label}\n    {detail}", file=sys.stderr)
    return 1


def check_tools(skills_root: Path) -> int:
    print(f"{DIM}--- in-process tool smoke ---{RESET}")
    failures = 0
    records = load_skills(skills_root)
    if len(records) < 100:
        failures += _say_fail("load_skills", f"only {len(records)} records — expected >100")
    else:
        _say_ok("load_skills", f"{len(records)} files")

    idx = SkillIndex.build(records)
    _say_ok("SkillIndex.build", f"dims={sorted(idx.by_dimension)}")

    tree = get_index_tree(idx, max_depth=3)
    if "children" not in tree or len(tree["children"]) < 4:
        failures += _say_fail("get_index_tree", f"tree shape unexpected: {list(tree)}")
    else:
        _say_ok("get_index_tree", f"top dims={[c['name'] for c in tree['children']]}")

    res = list_skills(idx, dimension="framework", depth="leaf", limit=5)
    if not res["items"]:
        failures += _say_fail("list_skills", "no framework leaves")
    else:
        _say_ok("list_skills", f"first={res['items'][0]['path']}")

    target_path = "framework/antd/form/validator-pattern.md"
    try:
        sk = get_skill(idx, path=target_path)
        assert sk["frontmatter"]
        _say_ok("get_skill", f"{target_path} → {len(sk['body_markdown'])} body chars")
    except Exception as exc:
        failures += _say_fail("get_skill", repr(exc))

    bundle = get_skill_bundle(idx, paths=[target_path, "nope.md"])
    if not bundle["skills"] or bundle["missing"] != ["nope.md"]:
        failures += _say_fail("get_skill_bundle", repr(bundle))
    else:
        _say_ok("get_skill_bundle", f"got 1, missing 1")

    s = search_skills(idx, query="antd 表单 校验", top_k=5)
    if not s["matches"]:
        failures += _say_fail("search_skills(zh query)", "no matches for 'antd 表单 校验'")
    else:
        _say_ok("search_skills(zh query)", f"top={s['matches'][0]['path']}")

    s2 = search_skills(idx, paths=["frontend/src/pages/User.tsx"], keywords=["button"], top_k=5)
    if not s2["matches"]:
        failures += _say_fail("search_skills(paths+kw)", "no matches")
    else:
        _say_ok("search_skills(paths+kw)", f"top={s2['matches'][0]['path']}")

    p = pick_design_skills(idx, topic="antd form 表单", kind="sketch", limit=4)
    if not p["skill_paths"]:
        failures += _say_fail("pick_design_skills", "empty for 'antd form 表单'")
    else:
        _say_ok("pick_design_skills", f"picked={len(p['skill_paths'])}")

    m = match_task_skills(idx, artifact_paths=["backend/api/user.py"], task_keywords=["jwt", "auth"])
    _say_ok("match_task_skills", f"hits={len(m['hits'])}")  # may be empty if data lacks JWT skills — informational

    return failures


def check_http(base: str) -> int:
    print(f"{DIM}--- HTTP smoke (base={base}) ---{RESET}")
    failures = 0

    def _get(path: str, accept: str = "application/json") -> tuple[int, bytes]:
        req = urllib.request.Request(base.rstrip("/") + path, headers={"Accept": accept})
        try:
            with urllib.request.urlopen(req, timeout=4) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read()
        except urllib.error.URLError as exc:
            print(f"{RED}HTTP unreachable{RESET}: {exc}", file=sys.stderr)
            return -1, b""

    status, body = _get("/health")
    if status == -1:
        return _say_fail("/health", "server not reachable (skip HTTP checks)")
    if status != 200:
        failures += _say_fail("/health", f"HTTP {status}")
    else:
        data = json.loads(body)
        if data.get("status") != "ok" or data.get("skills_count", 0) < 100:
            failures += _say_fail("/health body", repr(data))
        else:
            _say_ok("/health", f"skills_count={data['skills_count']}")

    status, body = _get("/web/", accept="text/html")
    if status != 200:
        failures += _say_fail("/web/", f"HTTP {status}")
    else:
        _say_ok("/web/", f"{len(body)} bytes HTML")

    q = urllib.parse.urlencode({"q": "antd 表单", "top_k": "5"})
    status, body = _get(f"/web/api/search?{q}")
    if status != 200:
        failures += _say_fail("/web/api/search", f"HTTP {status}")
    else:
        data = json.loads(body)
        if not data.get("matches"):
            failures += _say_fail("/web/api/search body", "no matches for 'antd 表单'")
        else:
            _say_ok("/web/api/search", f"top={data['matches'][0]['path']}")

    return failures


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://localhost:8080", help="server base URL")
    ap.add_argument("--skills-root", default="skills", help="skills directory (for in-process checks)")
    ap.add_argument("--skip-http", action="store_true", help="skip HTTP checks")
    args = ap.parse_args()

    total_fails = 0
    total_fails += check_tools(Path(args.skills_root).resolve())
    if not args.skip_http:
        total_fails += check_http(args.base)

    print()
    if total_fails:
        print(f"{RED}{total_fails} failure(s){RESET}")
        return 1
    print(f"{GREEN}all checks passed{RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
