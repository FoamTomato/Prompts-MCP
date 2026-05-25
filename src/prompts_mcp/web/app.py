from __future__ import annotations

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
                "dimensions": sorted(idx.by_dimension),
                "total": len(idx.records),
                "base": _base_path(request),
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
