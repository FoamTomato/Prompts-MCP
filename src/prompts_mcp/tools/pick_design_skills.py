from __future__ import annotations

from typing import Any

from ..indexes import SkillIndex
from ..matcher import search

KIND_DIMENSIONS = {
    "prd": ["habit", "design-pattern"],
    "sketch": ["framework", "design-pattern"],
    "hld": ["framework", "design-pattern", "lang"],
}


def pick_design_skills(
    index: SkillIndex,
    topic: str,
    kind: str = "prd",
    limit: int = 6,
) -> dict[str, Any]:
    """Pick skills to inform a design-phase artifact (PRD / sketch / HLD).

    Built on top of `search_skills` with a kind→dimension preset:
      - `prd`    → habit + design-pattern (process + abstraction rules)
      - `sketch` → framework + design-pattern (UI / component rules)
      - `hld`    → framework + design-pattern + lang (interface / language rules)
    """
    dims = KIND_DIMENSIONS.get(kind.lower())
    if not dims:
        raise ValueError(f"unknown kind={kind!r}; expected one of {sorted(KIND_DIMENSIONS)}")

    all_matches = []
    seen: set[str] = set()
    per_dim_cap = max(1, limit // len(dims))
    for d in dims:
        hits = search(index, query=topic, dimension=d, top_k=per_dim_cap * 2)
        for h in hits:
            if h.record.path in seen:
                continue
            seen.add(h.record.path)
            all_matches.append(h)
            if len([m for m in all_matches if m.record.dimension == d]) >= per_dim_cap * 2:
                break

    all_matches.sort(key=lambda m: m.score, reverse=True)
    picked = all_matches[:limit]

    return {
        "skill_paths": [
            {
                "path": m.record.path,
                "name": m.record.name,
                "description": m.record.description,
                "effort": m.record.effort,
                "dimension": m.record.dimension,
                "reason": f"matched_by={','.join(m.matched_by)} score={round(m.score, 2)}",
            }
            for m in picked
        ],
        "topic": topic,
        "kind": kind,
        "dimensions_searched": dims,
    }
