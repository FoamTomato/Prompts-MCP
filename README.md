# Prompts-MCP

A remote MCP server that exposes a structured markdown skill library to any LLM client (Claude Desktop, Cursor, Cline, custom agents). Backed by an in-memory index over `frontmatter.paths` globs and `triggers.keywords` — no vector store, no external API.

**Public endpoints**
- MCP: `https://xiaohang.site/mcp/sse`
- Web viewer: `https://xiaohang.site/skills/`

## Tools exposed (7)

Primitives:
- `list_skills(dimension?, parent?, depth?, limit?, cursor?)` — browse / enumerate (meta only)
- `get_skill(path | name, include?)` — full content of one skill
- `get_skill_bundle(paths)` — batch fetch full content
- `search_skills(query?, keywords?, paths?, dimension?, effort?, top_k?, fields?)` — unified retrieval
- `get_index_tree(max_depth?, include_descriptions?)` — full tree map for cold-start agents

Flow sugars:
- `pick_design_skills(topic, kind, max?)` — design-phase skill pickup
- `match_task_skills(artifact_paths, task_keywords, max?)` — dev-phase 2-D reverse lookup

Plus MCP Resources: every skill registered as `skill://<dim>/<.../leaf>` for clients that support Resources.

## Quick start

### Local

```bash
pip install -e ".[dev]"
cp .env.example .env
uvicorn prompts_mcp.server:app --reload --port 8080
# open http://localhost:8080/web/
```

### Docker

```bash
docker compose up -d
```

### Connect from Claude Desktop / Cursor

```json
{
  "mcpServers": {
    "prompts-mcp": {
      "url": "https://xiaohang.site/mcp/sse"
    }
  }
}
```

## Skill quality standard

See [CONTRIBUTING.md](CONTRIBUTING.md). Every skill file's frontmatter must include `name`, `description` (30–80 chars), `parent`, `paths` (globs), `triggers.keywords` (bilingual, ≥3), `effort`, `version`. Run `python scripts/lint_skills.py` before committing.

## License

MIT
