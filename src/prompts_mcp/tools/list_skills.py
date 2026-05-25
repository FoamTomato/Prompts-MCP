from __future__ import annotations

from typing import Any

from ..indexes import SkillIndex


def list_skills(
    index: SkillIndex,
    dimension: str | None = None,
    parent: str | None = None,
    depth: str = "all",
    limit: int = 50,
    cursor: int = 0,
) -> dict[str, Any]:
    """Browse / enumerate skills (metadata only).

    Args:
        dimension: top-level filter — lang / framework / design-pattern / habit.
        parent: POSIX path of an index.md; returns its direct children only.
        depth: "index" → only index files; "leaf" → only leaves; "all" → both.
        limit: max items per page.
        cursor: offset for pagination.
    """
    if depth not in {"index", "leaf", "all"}:
        depth = "all"

    records = index.records
    if dimension:
        records = [r for r in records if r.dimension == dimension]

    if parent:
        prefix = parent.removesuffix("index.md").rstrip("/")
        records = [
            r
            for r in records
            if r.path != parent
            and r.path.startswith(prefix + "/")
            and "/" not in r.path[len(prefix) + 1 :].removesuffix("/index.md")
        ]

    if depth == "index":
        records = [r for r in records if r.kind in {"root", "index"}]
    elif depth == "leaf":
        records = [r for r in records if r.kind == "leaf"]

    records = sorted(records, key=lambda r: r.path)
    total = len(records)
    page = records[cursor : cursor + limit]
    next_cursor = cursor + limit if cursor + limit < total else None

    return {
        "items": [r.to_meta() for r in page],
        "total": total,
        "next_cursor": next_cursor,
    }
