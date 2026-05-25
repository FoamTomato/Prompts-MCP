from __future__ import annotations

from typing import Any

from ..indexes import SkillIndex
from ..matcher import search


def search_skills(
    index: SkillIndex,
    query: str | None = None,
    keywords: list[str] | None = None,
    paths: list[str] | None = None,
    dimension: str | None = None,
    effort: str | None = None,
    top_k: int = 10,
    fields: str = "meta",
) -> dict[str, Any]:
    """Unified retrieval over the skill library.

    Composite scoring: glob hits on `paths` (strong) + keyword hits on
    `triggers.keywords` (medium) + token-level free-text match on `query`
    (weak, with rapidfuzz fallback). All filters are AND-combined.

    Args:
        query: natural-language search string; tokenised on whitespace + CJK runs.
        keywords: exact-keyword matches against frontmatter.triggers.keywords
                  (and substring fallback against the indexed text corpus).
        paths: caller's file paths; matched against each skill's frontmatter.paths globs.
        dimension: lang / framework / design-pattern / habit.
        effort: low / medium / high.
        top_k: max results.
        fields: "meta" (default) or "full" (include body markdown).
    """
    matches = search(
        index,
        query=query,
        keywords=keywords,
        paths=paths,
        dimension=dimension,
        effort=effort,
        top_k=top_k,
    )
    include_full = fields == "full"
    return {
        "matches": [m.to_dict(include_full=include_full) for m in matches],
        "total": len(matches),
    }
