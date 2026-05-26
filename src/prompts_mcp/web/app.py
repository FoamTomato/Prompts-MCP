from __future__ import annotations

import re
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from markdown_it import MarkdownIt
from starlette.requests import Request

from ..matcher import search

WEB_DIR = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(WEB_DIR / "templates"))
md_renderer = MarkdownIt("commonmark", {"html": False, "linkify": True, "typographer": True}).enable("table")


def create_web_app(state) -> FastAPI:
    """Build the markdown-viewer sub-application.

    Mounted at `/web` by the main app. `state` is the shared AppState holding
    the lazy-loaded SkillIndex (built in the parent lifespan).

    The viewer is reachable via two host paths:
      - locally:  http://localhost:8080/web/         (no BASE_URL_PREFIX)
      - prod:     https://xiaohang.site/skills/      (nginx → /web on container)
    All in-page links use a single `base` template var so the same templates
    work in both modes.
    """
    web = FastAPI(title="Prompts-MCP Viewer")
    web.mount("/static", StaticFiles(directory=str(WEB_DIR / "static")), name="static")

    def _require_index():
        idx = getattr(state, "index", None)
        if idx is None:
            raise HTTPException(503, "index not ready")
        return idx

    def _base_path(request: Request) -> str:
        """The external prefix as seen by the browser.

        Honors `X-Forwarded-Prefix` (set by nginx) — falls back to the local
        mount point '/web' when not behind a proxy.
        """
        fwd = request.headers.get("x-forwarded-prefix")
        if fwd:
            return fwd.rstrip("/")
        return "/web"

    def _body_is_redundant_with_children(body_md: str) -> bool:
        """An index file body is "redundant" if it only contains a heading
        and one markdown table — the same info the children-card already
        renders structured. We hide such bodies to avoid duplication.

        Conservative check: strip blank lines and a leading H1, then
        whatever remains must be a single GFM table (lines starting with `|`
        and a separator row). If any other content (prose, list, code, more
        headings) is present, keep the body.
        """
        lines = [l for l in body_md.splitlines() if l.strip()]
        # Strip leading H1
        if lines and lines[0].lstrip().startswith("# "):
            lines = lines[1:]
        if not lines:
            return True
        # Every remaining line must be a table line (starts with `|`).
        return all(l.lstrip().startswith("|") for l in lines)

    def _summarise_description(desc: str, note: str) -> str:
        """Pick the most informative *short* blurb for a child row.

        Prefer the part of the description before "Use when ..." (which is
        the trigger half — useful in the child's own page, noisy in a parent
        table). Fall back to the parent-declared note.
        """
        if desc:
            # Split off Use when …
            first = re.split(r"\.\s*Use when\b|。\s*Use when\b", desc, maxsplit=1)[0]
            first = first.rstrip("。").rstrip(".").strip()
            if first:
                return first
        return note

    def _build_children_view(rec, idx, base: str) -> list[dict]:
        """For an index/root skill, resolve its frontmatter.children into
        clickable view objects {name, href, blurb, tag, exists}.

        Children declared in frontmatter but missing on disk are still shown
        with exists=False so the UI can flag broken references.
        """
        children = rec.frontmatter.get("children") if rec.frontmatter else None
        if not isinstance(children, list):
            return []
        # rec.path is POSIX, e.g. "habit/code-quality/index.md"
        # Children paths are relative to rec.path's directory.
        parent_dir = rec.path.rsplit("/", 1)[0] if "/" in rec.path else ""
        out = []
        for ch in children:
            if not isinstance(ch, dict):
                continue
            name = str(ch.get("name") or "").strip()
            cp = str(ch.get("path") or "").strip()
            if not name or not cp:
                continue
            # Resolve relative path
            full_path = f"{parent_dir}/{cp}" if parent_dir else cp
            target = idx.by_path.get(full_path)
            # Build href: strip .md, web router accepts both
            href_path = full_path.removesuffix(".md")
            note = str(ch.get("note") or "").strip()
            child_desc = target.description if target else ""
            out.append({
                "name": name,
                "href": f"{base}/skill/{href_path}",
                "blurb": _summarise_description(child_desc, note),
                "tag": str(ch.get("tag") or "").strip(),
                "exists": target is not None,
            })
        return out

    @web.get("/", response_class=HTMLResponse)
    def index(request: Request) -> HTMLResponse:
        idx = _require_index()
        tree = idx.tree.to_dict(include_descriptions=True, max_depth=10)
        return TEMPLATES.TemplateResponse(
            request,
            "layout.html",
            {
                "tree": tree,
                "active_path": None,
                "rendered_html": None,
                "skill": None,
                "children_view": [],
                "dimensions": sorted(idx.by_dimension),
                "total": len(idx.records),
                "base": _base_path(request),
            },
        )

    @web.get("/skill/{skill_path:path}", response_class=HTMLResponse)
    def view_skill(request: Request, skill_path: str) -> HTMLResponse:
        idx = _require_index()
        normalized = skill_path if skill_path.endswith(".md") else skill_path + ".md"
        rec = idx.by_path.get(normalized)
        if rec is None:
            raise HTTPException(404, f"skill not found: {skill_path}")

        base = _base_path(request)
        is_index = rec.kind in {"index", "root"}
        children_view = _build_children_view(rec, idx, base) if is_index else []

        # On an index page, if the markdown body is just a duplicate of the
        # children-card (heading + table), skip rendering it entirely.
        # Otherwise (the body has extra prose/decision-tables/links), render.
        if is_index and children_view and _body_is_redundant_with_children(rec.body_markdown):
            rendered = ""
        else:
            rendered = md_renderer.render(rec.body_markdown)

        tree = idx.tree.to_dict(include_descriptions=True, max_depth=10)
        return TEMPLATES.TemplateResponse(
            request,
            "layout.html",
            {
                "tree": tree,
                "active_path": rec.path,
                "rendered_html": rendered,
                "skill": rec,
                "children_view": children_view,
                "dimensions": sorted(idx.by_dimension),
                "total": len(idx.records),
                "base": base,
            },
        )

    @web.get("/api/search")
    def api_search(
        q: str = Query("", description="search query"),
        dimension: str | None = None,
        top_k: int = 20,
    ) -> JSONResponse:
        idx = _require_index()
        q = q.strip()
        if not q:
            return JSONResponse({"matches": []})
        matches = search(idx, query=q, dimension=dimension, top_k=top_k)
        return JSONResponse(
            {
                "matches": [
                    {
                        "path": m.record.path,
                        "name": m.record.name,
                        "description": m.record.description,
                        "dimension": m.record.dimension,
                        "score": round(m.score, 3),
                        "matched_by": m.matched_by,
                    }
                    for m in matches
                ]
            }
        )

    return web
