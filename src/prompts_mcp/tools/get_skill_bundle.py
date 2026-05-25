from __future__ import annotations

from typing import Any

from ..indexes import SkillIndex


def get_skill_bundle(index: SkillIndex, paths: list[str]) -> dict[str, Any]:
    """Batch-fetch full content for multiple skills in one call.

    Unknown paths appear in `missing` rather than raising.
    """
    if not paths:
        return {"skills": [], "missing": []}

    skills = []
    missing = []
    for p in paths:
        rec = index.by_path.get(p)
        if rec is None:
            missing.append(p)
            continue
        skills.append(
            {
                "path": rec.path,
                "name": rec.name,
                "kind": rec.kind,
                "frontmatter": rec.frontmatter,
                "body_markdown": rec.body_markdown,
                "uri": rec.uri,
            }
        )
    return {"skills": skills, "missing": missing}
