from __future__ import annotations

from typing import Any

from ..indexes import SkillIndex
from ..matcher import search


def match_task_skills(
    index: SkillIndex,
    artifact_paths: list[str],
    task_keywords: list[str] | None = None,
    limit: int = 5,
) -> dict[str, Any]:
    """Two-dimensional reverse lookup for dev-phase task→skill matching.

    Mirrors Quill's `quill-dev` Step 3.0: given the file paths the agent is
    about to write/modify plus the task description keywords, return the
    most relevant leaf skills (paths-glob hits first, keyword overlap as
    a tiebreaker).
    """
    if not artifact_paths:
        return {"hits": [], "artifact_paths": [], "task_keywords": task_keywords or []}

    matches = search(
        index,
        paths=artifact_paths,
        keywords=task_keywords or None,
        top_k=limit * 2,
        kinds=["leaf"],
    )

    seen: set[str] = set()
    hits = []
    for m in matches:
        if m.record.path in seen:
            continue
        seen.add(m.record.path)
        hits.append(
            {
                "path": m.record.path,
                "name": m.record.name,
                "description": m.record.description,
                "matched_by": m.matched_by,
                "score": round(m.score, 4),
                "effort": m.record.effort,
                "dimension": m.record.dimension,
            }
        )
        if len(hits) >= limit:
            break

    return {
        "hits": hits,
        "artifact_paths": artifact_paths,
        "task_keywords": task_keywords or [],
    }
