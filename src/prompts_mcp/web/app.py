from __future__ import annotations

import logging
import re
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound
from starlette.requests import Request

from ..matcher import search

logger = logging.getLogger(__name__)

WEB_DIR = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(WEB_DIR / "templates"))

# Pygments formatter — emits just the token spans (no outer <div class="highlight">,
# no outer <pre>) because markdown-it-py already wraps highlight() output in
# <pre><code>...</code></pre>. Double-wrapping caused double borders earlier.
# `nowrap=True` strips the div/pre; CSS targets `.highlight .k` etc., so we
# instead style the bare tokens via `pre code .k`.
_PYG_FORMATTER = HtmlFormatter(nowrap=True)


def _highlight(code: str, lang: str, _attrs: str) -> str:
    """markdown-it highlight callback.

    Returns inner HTML (token spans) — markdown-it wraps in <pre><code>.

    Language resolution (per user preference):
      1. If the fence specifies a language and Pygments knows it, use it.
      2. Otherwise try `python` as the default.
      3. If that fails (Pygments not installed), fall back to `sql`.
      4. If even that fails, return "" so markdown-it falls back to the
         default no-highlight escape path.
    """
    lang = (lang or "").strip().lower()
    lexer = None
    if lang:
        try:
            lexer = get_lexer_by_name(lang, stripnl=False)
        except ClassNotFound:
            logger.debug("unknown code-fence language %r — falling back", lang)
    if lexer is None:
        for fallback in ("python", "sql"):
            try:
                lexer = get_lexer_by_name(fallback, stripnl=False)
                break
            except ClassNotFound:
                continue
    if lexer is None:
        return ""
    # rstrip trailing newline — markdown-it already provides one via </pre>.
    return highlight(code, lexer, _PYG_FORMATTER).rstrip("\n")


md_renderer = (
    MarkdownIt("commonmark", {"html": False, "linkify": True, "typographer": True, "highlight": _highlight})
    .enable("table")
)


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
        # Comma-separated lists for sub-agent / curl use:
        #   ?paths=frontend/src/Card.tsx,frontend/src/App.tsx
        #   ?keywords=Card,hover,onClick
        paths: str | None = Query(None, description="comma-separated artifact paths"),
        keywords: str | None = Query(None, description="comma-separated keywords"),
        dimension: str | None = None,
        effort: str | None = None,
        kinds: str | None = Query(None, description="comma-separated kinds (leaf/index/root)"),
        top_k: int = 10,
    ) -> JSONResponse:
        """Search endpoint usable both by the Web UI (q only) and by external
        callers like the Quill quill-dev sub-agent (paths × keywords two-D
        reverse lookup, no MCP client needed — just curl).
        """
        idx = _require_index()
        q = (q or "").strip()
        paths_list = [s.strip() for s in (paths or "").split(",") if s.strip()] or None
        kw_list = [s.strip() for s in (keywords or "").split(",") if s.strip()] or None
        kinds_list = [s.strip() for s in (kinds or "").split(",") if s.strip()] or None

        if not q and not paths_list and not kw_list:
            return JSONResponse({"matches": []})

        matches = search(
            idx,
            query=q or None,
            keywords=kw_list,
            paths=paths_list,
            dimension=dimension,
            effort=effort,
            top_k=top_k,
            kinds=kinds_list,
        )
        return JSONResponse(
            {
                "matches": [
                    {
                        "path": m.record.path,
                        "name": m.record.name,
                        "description": m.record.description,
                        "dimension": m.record.dimension,
                        "effort": m.record.effort,
                        "score": round(m.score, 3),
                        "matched_by": m.matched_by,
                    }
                    for m in matches
                ]
            }
        )

    @web.get("/api/skill/{skill_path:path}")
    def api_get_skill(skill_path: str, include: str = Query("body", description="frontmatter|body|raw")) -> JSONResponse:
        """Return one skill's content as JSON. Mirrors the MCP get_skill
        tool — easier to consume from a sub-agent's `Bash` curl call than
        an MCP stdio client.

        ?include=body (default) returns just the markdown body for direct
        pasting into context. include=raw returns the full file content
        including frontmatter. include=frontmatter returns parsed yaml only.
        Multiple values can be comma-separated.
        """
        idx = _require_index()
        normalized = skill_path if skill_path.endswith(".md") else skill_path + ".md"
        rec = idx.by_path.get(normalized)
        if rec is None:
            raise HTTPException(404, f"skill not found: {skill_path}")
        want = {p.strip() for p in include.split(",") if p.strip()}
        out: dict = {
            "name": rec.name,
            "path": rec.path,
            "kind": rec.kind,
            "dimension": rec.dimension,
            "uri": rec.uri,
        }
        if "frontmatter" in want:
            out["frontmatter"] = rec.frontmatter
        if "body" in want:
            out["body_markdown"] = rec.body_markdown
        if "raw" in want:
            out["raw_markdown"] = rec.raw_markdown
        return JSONResponse(out)

    @web.get("/api/bundle")
    def api_bundle(paths: str = Query("", description="comma-separated skill paths")) -> JSONResponse:
        """Batch fetch full body markdown for multiple skills. Mirrors the
        MCP get_skill_bundle tool. Usage:
          curl 'https://xiaohang.site/skills/api/bundle?paths=habit/x.md,habit/y.md'
        """
        idx = _require_index()
        path_list = [p.strip() for p in paths.split(",") if p.strip()]
        out_skills, missing = [], []
        for p in path_list:
            normalized = p if p.endswith(".md") else p + ".md"
            rec = idx.by_path.get(normalized)
            if rec is None:
                missing.append(p)
                continue
            out_skills.append({
                "path": rec.path,
                "name": rec.name,
                "kind": rec.kind,
                "description": rec.description,
                "body_markdown": rec.body_markdown,
            })
        return JSONResponse({"skills": out_skills, "missing": missing})

    return web
