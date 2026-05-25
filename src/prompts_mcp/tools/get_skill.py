from __future__ import annotations

from typing import Any

from ..indexes import SkillIndex


def get_skill(
    index: SkillIndex,
    path: str | None = None,
    name: str | None = None,
    include: list[str] | None = None,
) -> dict[str, Any]:
    """Fetch one skill's full content (frontmatter + body).

    Locate by `path` (POSIX relative to skills root) or by `name` (frontmatter.name).
    `include` controls which sections to return: any of "frontmatter" / "body" / "raw".
    Default returns all three.
    """
    if not path and not name:
        raise ValueError("either `path` or `name` is required")

    rec = None
    if path:
        rec = index.by_path.get(path)
    if rec is None and name:
        rec = index.by_name.get(name)
    if rec is None:
        raise KeyError(f"skill not found (path={path!r}, name={name!r})")

    include_set = set(include) if include else {"frontmatter", "body", "raw"}
    out: dict[str, Any] = {
        "name": rec.name,
        "path": rec.path,
        "kind": rec.kind,
        "dimension": rec.dimension,
        "uri": rec.uri,
    }
    if "frontmatter" in include_set:
        out["frontmatter"] = rec.frontmatter
    if "body" in include_set:
        out["body_markdown"] = rec.body_markdown
    if "raw" in include_set:
        out["raw_markdown"] = rec.raw_markdown
    return out
