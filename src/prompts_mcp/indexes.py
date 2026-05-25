from __future__ import annotations

import fnmatch
import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .loader import SkillRecord

logger = logging.getLogger(__name__)


def _compile_glob(pattern: str) -> re.Pattern[str]:
    """Compile a `**/*.ext` style glob into a regex.

    fnmatch.translate handles `*` and `?` but `**` becomes `*` which loses the
    directory-spanning semantic — so we replace `**` with a sentinel first.
    """
    SENTINEL = "\x00DOUBLESTAR\x00"
    p = pattern.replace("**", SENTINEL)
    regex = fnmatch.translate(p).replace(re.escape(SENTINEL), ".*")
    return re.compile(regex)


@dataclass
class TreeNode:
    name: str
    path: str
    kind: str
    description: str = ""
    children: list[TreeNode] = field(default_factory=list)

    def to_dict(self, include_descriptions: bool = True, max_depth: int = 10, depth: int = 0) -> dict[str, Any]:
        out: dict[str, Any] = {
            "name": self.name,
            "path": self.path,
            "kind": self.kind,
        }
        if include_descriptions and self.description:
            out["description"] = self.description
        if self.children and depth < max_depth:
            out["children"] = [
                c.to_dict(include_descriptions, max_depth, depth + 1) for c in self.children
            ]
        return out


@dataclass
class SkillIndex:
    """Aggregated in-memory indexes built once at startup."""

    records: list[SkillRecord]
    by_path: dict[str, SkillRecord]
    by_name: dict[str, SkillRecord]
    by_dimension: dict[str, list[SkillRecord]]
    keyword_to_paths: dict[str, set[str]]
    glob_index: list[tuple[re.Pattern[str], str, str]]   # (compiled, original_glob, owner_path)
    tree: TreeNode
    text_corpus: dict[str, str]

    @classmethod
    def build(cls, records: list[SkillRecord]) -> SkillIndex:
        by_path = {r.path: r for r in records}
        by_name: dict[str, SkillRecord] = {}
        for r in records:
            if r.name in by_name:
                logger.warning("duplicate skill name %r at %s and %s", r.name, by_name[r.name].path, r.path)
            by_name.setdefault(r.name, r)

        by_dimension: dict[str, list[SkillRecord]] = defaultdict(list)
        for r in records:
            if r.dimension:
                by_dimension[r.dimension].append(r)

        keyword_to_paths: dict[str, set[str]] = defaultdict(set)
        for r in records:
            for kw in r.keywords:
                keyword_to_paths[kw].add(r.path)

        glob_index: list[tuple[re.Pattern[str], str, str]] = []
        for r in records:
            for g in r.paths:
                try:
                    glob_index.append((_compile_glob(g), g, r.path))
                except re.error as exc:
                    logger.warning("bad glob %r in %s: %s", g, r.path, exc)

        tree = cls._build_tree(records, by_path)

        text_corpus: dict[str, str] = {}
        for r in records:
            corpus_parts = [r.name, r.description]
            kw_blob = " ".join(r.keywords)
            corpus_parts.append(kw_blob)
            body_head = r.body_markdown[:500]
            corpus_parts.append(body_head)
            text_corpus[r.path] = "\n".join(corpus_parts).lower()

        return cls(
            records=records,
            by_path=by_path,
            by_name=by_name,
            by_dimension=dict(by_dimension),
            keyword_to_paths=dict(keyword_to_paths),
            glob_index=glob_index,
            tree=tree,
            text_corpus=text_corpus,
        )

    @staticmethod
    def _build_tree(records: list[SkillRecord], by_path: dict[str, SkillRecord]) -> TreeNode:
        root = TreeNode(name="root", path="", kind="root")
        node_by_path: dict[str, TreeNode] = {"": root}

        for r in sorted(records, key=lambda x: x.path):
            parts = r.path.split("/")
            if r.kind == "root":
                root.description = r.description
                root.name = r.name or "root"
                continue
            parent_path = "/".join(parts[:-1])
            parent_node = node_by_path.get(parent_path)
            if parent_node is None:
                acc = []
                cursor = root
                for seg in parts[:-1]:
                    acc.append(seg)
                    candidate_path = "/".join(acc)
                    if candidate_path not in node_by_path:
                        idx_path = candidate_path + "/index.md"
                        idx_rec = by_path.get(idx_path)
                        inner = TreeNode(
                            name=idx_rec.name if idx_rec else seg,
                            path=candidate_path,
                            kind="folder",
                            description=idx_rec.description if idx_rec else "",
                        )
                        cursor.children.append(inner)
                        node_by_path[candidate_path] = inner
                    cursor = node_by_path[candidate_path]
                parent_node = cursor

            if r.kind == "index":
                folder_path = "/".join(parts[:-1])
                folder_node = node_by_path.get(folder_path)
                if folder_node:
                    folder_node.description = folder_node.description or r.description
                    if r.name:
                        folder_node.name = r.name
                continue

            parent_node.children.append(
                TreeNode(name=r.name, path=r.path, kind="leaf", description=r.description)
            )

        return root

    def match_globs(self, caller_paths: list[str]) -> dict[str, set[str]]:
        """Return {skill_path: {globs that matched}} for any caller path hitting a skill's frontmatter.paths."""
        out: dict[str, set[str]] = defaultdict(set)
        for cp in caller_paths:
            cp_norm = cp.lstrip("./")
            for regex, original_glob, owner in self.glob_index:
                if regex.match(cp_norm):
                    out[owner].add(original_glob)
        return dict(out)
