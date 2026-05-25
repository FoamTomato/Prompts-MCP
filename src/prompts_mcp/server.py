from __future__ import annotations

import datetime as dt
import logging
import os
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .config import Settings
from .indexes import SkillIndex
from .loader import load_skills
from .tools.get_index_tree import get_index_tree as _get_index_tree
from .tools.get_skill import get_skill as _get_skill
from .tools.get_skill_bundle import get_skill_bundle as _get_skill_bundle
from .tools.list_skills import list_skills as _list_skills
from .tools.match_task_skills import match_task_skills as _match_task_skills
from .tools.pick_design_skills import pick_design_skills as _pick_design_skills
from .tools.search_skills import search_skills as _search_skills

logger = logging.getLogger(__name__)


class AppState:
    settings: Settings
    index: SkillIndex
    indexed_at: str


def build_index(settings: Settings) -> SkillIndex:
    records = load_skills(settings.skills_root)
    return SkillIndex.build(records)


def _make_mcp(state: AppState):
    """Construct a FastMCP server with all 7 tools + Resources registered."""
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("prompts-mcp", instructions=(
        "A markdown skill library. Use `get_index_tree` first for orientation, "
        "then `search_skills` (or `match_task_skills` / `pick_design_skills` "
        "for Quill-flavored flows). Fetch full content via `get_skill` / "
        "`get_skill_bundle`. Every skill is also exposed as a `skill://` Resource."
    ))

    @mcp.tool()
    def list_skills(
        dimension: str | None = None,
        parent: str | None = None,
        depth: str = "all",
        limit: int = 50,
        cursor: int = 0,
    ) -> dict[str, Any]:
        """Browse / enumerate skills (metadata only). Filter by dimension or parent."""
        return _list_skills(state.index, dimension, parent, depth, limit, cursor)

    @mcp.tool()
    def get_skill(
        path: str | None = None,
        name: str | None = None,
        include: list[str] | None = None,
    ) -> dict[str, Any]:
        """Fetch one skill's full content. Locate by `path` (POSIX) or `name`."""
        return _get_skill(state.index, path, name, include)

    @mcp.tool()
    def get_skill_bundle(paths: list[str]) -> dict[str, Any]:
        """Batch-fetch full content for multiple skills in one call."""
        return _get_skill_bundle(state.index, paths)

    @mcp.tool()
    def search_skills(
        query: str | None = None,
        keywords: list[str] | None = None,
        paths: list[str] | None = None,
        dimension: str | None = None,
        effort: str | None = None,
        top_k: int = 10,
        fields: str = "meta",
    ) -> dict[str, Any]:
        """Unified retrieval: paths-glob + keywords + free-text fuzzy. All AND-combined."""
        return _search_skills(state.index, query, keywords, paths, dimension, effort, top_k, fields)

    @mcp.tool()
    def get_index_tree(max_depth: int = 3, include_descriptions: bool = True) -> dict[str, Any]:
        """Return the full skill tree — one-shot map for cold-start agents."""
        return _get_index_tree(state.index, max_depth, include_descriptions)

    @mcp.tool()
    def pick_design_skills(topic: str, kind: str = "prd", limit: int = 6) -> dict[str, Any]:
        """Pick design-phase skills by topic. `kind`: prd / sketch / hld."""
        return _pick_design_skills(state.index, topic, kind, limit)

    @mcp.tool()
    def match_task_skills(
        artifact_paths: list[str],
        task_keywords: list[str] | None = None,
        limit: int = 5,
    ) -> dict[str, Any]:
        """Dev-phase reverse lookup: file paths × task keywords → leaf skills."""
        return _match_task_skills(state.index, artifact_paths, task_keywords, limit)

    # MCP Resources — every skill exposed as skill://<path-without-.md>
    # FastMCP 1.x uses URI templates; one handler matches all skills.
    @mcp.resource("skill://{path}", name="skill", mime_type="text/markdown")
    def _read_skill_resource(path: str) -> str:
        normalized = path if path.endswith(".md") else path + ".md"
        rec = state.index.by_path.get(normalized)
        if rec is None:
            raise KeyError(f"resource not found: skill://{path}")
        return rec.raw_markdown

    return mcp


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    logging.basicConfig(
        level=getattr(logging, settings.log_level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    )

    state = AppState()
    state.settings = settings

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info("loading skills from %s", settings.skills_root)
        state.index = build_index(settings)
        state.indexed_at = dt.datetime.utcnow().isoformat() + "Z"
        logger.info("ready — %d skills indexed", len(state.index.records))
        yield

    app = FastAPI(title="Prompts-MCP", version="0.1.0", lifespan=lifespan)

    @app.get("/health")
    def health() -> JSONResponse:
        if not hasattr(state, "index"):
            return JSONResponse({"status": "starting"}, status_code=503)
        return JSONResponse(
            {
                "status": "ok",
                "skills_count": len(state.index.records),
                "indexed_at": state.indexed_at,
                "dimensions": sorted(state.index.by_dimension),
            }
        )

    # Web viewer FIRST so its prefix wins over the catch-all MCP mount below.
    try:
        from .web.app import create_web_app
        app.mount("/web", create_web_app(state))
    except ImportError:
        logger.warning("web viewer not available")

    # Mount MCP HTTP/SSE last — catches /sse and /messages at the root.
    mcp = _make_mcp(state)
    sse_app = mcp.sse_app()
    app.mount("/", sse_app)

    return app


app = create_app()


def cli() -> None:
    import uvicorn

    settings = Settings.from_env()
    uvicorn.run(
        "prompts_mcp.server:app",
        host="0.0.0.0",
        port=settings.port,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    cli()
