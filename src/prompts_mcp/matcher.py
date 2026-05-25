from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any

from rapidfuzz import fuzz

from .indexes import SkillIndex
from .loader import SkillRecord

logger = logging.getLogger(__name__)

EFFORT_BONUS = {"low": 0.3, "medium": 0.15, "high": 0.0}
FUZZ_THRESHOLD = 75
TOKEN_RE = re.compile(r"[A-Za-z0-9_]+|[一-鿿]+")


def _tokenize(text: str) -> list[str]:
    """Split into ASCII word tokens + Chinese character runs.

    'antd 表单 校验' → ['antd', '表单', '校验']
    'JWT auth' → ['jwt', 'auth']
    Chinese is kept as multi-char runs (no jieba dependency).
    """
    return [t.lower() for t in TOKEN_RE.findall(text)]


@dataclass
class Match:
    record: SkillRecord
    score: float
    matched_by: list[str]
    snippet: str | None = None

    def to_dict(self, include_full: bool = False) -> dict[str, Any]:
        out: dict[str, Any] = {
            "path": self.record.path,
            "name": self.record.name,
            "score": round(self.score, 4),
            "matched_by": self.matched_by,
            "frontmatter": self.record.frontmatter,
        }
        if self.snippet:
            out["snippet"] = self.snippet
        if include_full:
            out["body_markdown"] = self.record.body_markdown
        return out


def _snippet_around(text: str, needle: str, width: int = 150) -> str | None:
    if not needle:
        return None
    idx = text.lower().find(needle.lower())
    if idx < 0:
        return None
    start = max(0, idx - width // 2)
    end = min(len(text), idx + len(needle) + width // 2)
    return ("…" if start > 0 else "") + text[start:end].strip() + ("…" if end < len(text) else "")


def search(
    index: SkillIndex,
    query: str | None = None,
    keywords: list[str] | None = None,
    paths: list[str] | None = None,
    dimension: str | None = None,
    effort: str | None = None,
    top_k: int = 10,
    kinds: list[str] | None = None,
) -> list[Match]:
    """Composite scoring across paths-glob (strong), keywords (medium), free-text fuzzy (weak)."""
    keywords_norm = [k.strip().lower() for k in (keywords or []) if k.strip()]
    paths_norm = [p.strip() for p in (paths or []) if p.strip()]
    query_norm = (query or "").strip()

    if paths_norm:
        path_hits = index.match_globs(paths_norm)
    else:
        path_hits = {}

    candidates: set[str]
    if paths_norm:
        candidates = set(path_hits.keys())
        if keywords_norm:
            kw_hit_paths: set[str] = set()
            for kw in keywords_norm:
                kw_hit_paths |= index.keyword_to_paths.get(kw, set())
            candidates |= kw_hit_paths
    elif keywords_norm:
        candidates = set()
        for kw in keywords_norm:
            candidates |= index.keyword_to_paths.get(kw, set())
        if not candidates and query_norm:
            candidates = set(index.by_path.keys())
    elif query_norm:
        candidates = set(index.by_path.keys())
    else:
        candidates = set(index.by_path.keys())

    matches: list[Match] = []
    for path in candidates:
        rec = index.by_path[path]

        if dimension and rec.dimension != dimension:
            continue
        if effort and rec.effort != effort:
            continue
        if kinds and rec.kind not in kinds:
            continue

        score = 0.0
        matched_by: list[str] = []
        snippet: str | None = None

        if paths_norm:
            n_globs_hit = len(path_hits.get(path, set()))
            if n_globs_hit == 0:
                if not keywords_norm and not query_norm:
                    continue
            else:
                hit_ratio = min(1.0, n_globs_hit / max(1, len(paths_norm)))
                score += 3.0 * hit_ratio
                matched_by.append("paths")

        if keywords_norm:
            rec_kw_set = set(rec.keywords)
            hits = sum(1 for k in keywords_norm if k in rec_kw_set)
            if hits == 0:
                kw_blob = index.text_corpus[path]
                substr_hits = sum(1 for k in keywords_norm if k in kw_blob)
                if substr_hits > 0:
                    score += 1.0 * (substr_hits / len(keywords_norm))
                    matched_by.append("keywords-substr")
            else:
                score += 2.0 * (hits / len(keywords_norm))
                matched_by.append("keywords")

        if query_norm:
            tokens = _tokenize(query_norm)
            if tokens:
                text_blob = index.text_corpus[path]
                desc_low = rec.description.lower()
                name_low = rec.name.lower()
                token_hits = 0
                fuzzy_acc = 0.0
                for tok in tokens:
                    if tok in name_low or tok in desc_low:
                        token_hits += 2
                    elif tok in text_blob:
                        token_hits += 1
                    else:
                        r = fuzz.partial_ratio(tok, text_blob)
                        if r >= FUZZ_THRESHOLD:
                            fuzzy_acc += r / 100.0
                if token_hits > 0:
                    score += 1.5 * (token_hits / (2 * len(tokens)))
                    matched_by.append("text")
                    snippet = _snippet_around(rec.description or rec.body_markdown, tokens[0])
                if fuzzy_acc > 0:
                    score += 0.3 * (fuzzy_acc / len(tokens))
                    if "text" not in matched_by:
                        matched_by.append("text-fuzzy")
                        if not snippet:
                            snippet = _snippet_around(rec.body_markdown, tokens[0])

        if not matched_by:
            continue

        score += EFFORT_BONUS.get(rec.effort, 0.0)

        matches.append(Match(record=rec, score=score, matched_by=matched_by, snippet=snippet))

    matches.sort(key=lambda m: m.score, reverse=True)
    return matches[:top_k]
