from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


@dataclass
class SkillRecord:
    """One markdown file under skills/."""

    path: str                       # POSIX relative to skills root, e.g. "framework/antd/form/index.md"
    name: str                       # frontmatter.name, falls back to derived
    kind: str                       # "root" | "index" | "leaf"
    dimension: str | None           # top-level dir: lang / framework / design-pattern / habit (None for root)
    parent: str | None              # POSIX relative parent path, or None
    description: str
    frontmatter: dict[str, Any]
    body_markdown: str
    raw_markdown: str

    # Derived helpers
    paths: list[str] = field(default_factory=list)              # globs
    keywords: list[str] = field(default_factory=list)           # triggers.keywords lower-cased
    effort: str = "medium"

    @property
    def uri(self) -> str:
        return "skill://" + self.path.removesuffix(".md")

    def to_meta(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "path": self.path,
            "kind": self.kind,
            "dimension": self.dimension,
            "parent": self.parent,
            "description": self.description,
            "effort": self.effort,
            "version": self.frontmatter.get("version"),
            "uri": self.uri,
        }


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as exc:
        logger.warning("invalid YAML frontmatter: %s", exc)
        return {}, text
    if not isinstance(fm, dict):
        return {}, text
    body = text[m.end():]
    return fm, body


def _kind_of(rel_path: str) -> str:
    if rel_path == "index.md":
        return "root"
    if rel_path.endswith("/index.md"):
        return "index"
    return "leaf"


def _dimension_of(rel_path: str) -> str | None:
    parts = rel_path.split("/")
    if rel_path == "index.md":
        return None
    return parts[0]


def _norm_keywords(raw: Any) -> list[str]:
    if not isinstance(raw, dict):
        return []
    kws = raw.get("keywords")
    if not isinstance(kws, list):
        return []
    return [str(k).strip().lower() for k in kws if str(k).strip()]


def load_skills(root: Path) -> list[SkillRecord]:
    """Walk root/**/*.md and return parsed SkillRecord list.

    Files that fail to parse are skipped with a warning rather than aborting startup.
    """
    if not root.exists():
        raise FileNotFoundError(f"skills root does not exist: {root}")

    records: list[SkillRecord] = []
    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root).as_posix()
        try:
            raw = md.read_text(encoding="utf-8")
        except OSError as exc:
            logger.warning("cannot read %s: %s", rel, exc)
            continue
        fm, body = _parse_frontmatter(raw)

        kind = _kind_of(rel)
        name = str(fm.get("name") or _derive_name(rel)).strip()
        parent = fm.get("parent")
        parent_rel: str | None
        if isinstance(parent, str) and parent:
            resolved = (md.parent / parent).resolve()
            try:
                parent_rel = resolved.relative_to(root).as_posix()
            except ValueError:
                parent_rel = None
        else:
            parent_rel = None

        description = str(fm.get("description") or "").strip()
        paths = fm.get("paths")
        if not isinstance(paths, list):
            paths = []
        else:
            paths = [str(p).strip() for p in paths if str(p).strip()]

        effort = str(fm.get("effort") or "medium").strip().lower()
        if effort not in {"low", "medium", "high"}:
            effort = "medium"

        records.append(
            SkillRecord(
                path=rel,
                name=name,
                kind=kind,
                dimension=_dimension_of(rel),
                parent=parent_rel,
                description=description,
                frontmatter=fm,
                body_markdown=body,
                raw_markdown=raw,
                paths=paths,
                keywords=_norm_keywords(fm.get("triggers")),
                effort=effort,
            )
        )
    logger.info("loaded %d skill files from %s", len(records), root)
    return records


def _derive_name(rel_path: str) -> str:
    stem = Path(rel_path).stem
    if stem == "index":
        parent = Path(rel_path).parent.name or "root"
        return f"{parent}-index"
    return stem
