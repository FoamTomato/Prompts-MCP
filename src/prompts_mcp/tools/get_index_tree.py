from __future__ import annotations

from typing import Any

from ..indexes import SkillIndex


def get_index_tree(
    index: SkillIndex,
    max_depth: int = 3,
    include_descriptions: bool = True,
) -> dict[str, Any]:
    """Return the full skill tree (root → dimension → index → leaf).

    Cold-start map for unfamiliar agents — one call to learn the whole library.
    """
    return index.tree.to_dict(include_descriptions=include_descriptions, max_depth=max_depth)
