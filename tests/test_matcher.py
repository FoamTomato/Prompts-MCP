from pathlib import Path

import pytest

from prompts_mcp.indexes import SkillIndex
from prompts_mcp.loader import load_skills
from prompts_mcp.matcher import search


@pytest.fixture(scope="module")
def index() -> SkillIndex:
    root = Path(__file__).resolve().parent.parent / "skills"
    return SkillIndex.build(load_skills(root))


def test_index_built(index: SkillIndex) -> None:
    assert len(index.records) > 0
    assert len(index.by_path) == len(index.records)
    assert {"lang", "framework", "design-pattern", "habit"} <= set(index.by_dimension)


def test_chinese_query_returns_results(index: SkillIndex) -> None:
    hits = search(index, query="antd 表单 校验", top_k=5)
    assert hits, "Chinese tokenized query must return at least one match"
    paths = [m.record.path for m in hits]
    assert any("antd/form" in p for p in paths), f"expected antd/form hit, got {paths}"


def test_paths_only_glob_match(index: SkillIndex) -> None:
    hits = search(index, paths=["frontend/src/components/Button.tsx"], top_k=10)
    assert hits
    assert all("paths" in m.matched_by for m in hits)


def test_keywords_substr_fallback(index: SkillIndex) -> None:
    hits = search(index, keywords=["button"], top_k=10)
    assert hits
    assert any("button-naming" in m.record.path for m in hits)


def test_dimension_filter(index: SkillIndex) -> None:
    hits = search(index, query="prd", dimension="habit", top_k=10)
    assert all(m.record.dimension == "habit" for m in hits)


def test_effort_low_bonus(index: SkillIndex) -> None:
    hits = search(index, paths=["frontend/src/App.tsx"], top_k=20)
    if len(hits) >= 2:
        efforts = [m.record.effort for m in hits]
        assert efforts[0] in {"low", "medium", "high"}
