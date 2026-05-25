# Deployment to 117.72.182.195

## One-time setup

```bash
ssh root@117.72.182.195
cd /opt
git clone https://github.com/FoamTomato/Prompts-MCP.git prompts-mcp
```

Append the `prompts-mcp:` service block from `deploy/docker-compose.prod.yml` into `/opt/docker-compose.yml` under the existing `services:` map. Make sure the `app-net` network reference matches whatever the file declares (usually `app-net` aliased to `opt_app-net`).

```bash
cd /opt
docker compose up -d --build prompts-mcp
docker compose ps prompts-mcp
docker compose logs --tail=50 prompts-mcp
```

Append `deploy/nginx-snippet.conf` into the `server { server_name xiaohang.site; ... }` block of `/opt/nginx/conf.d/default.conf` (back up first: `cp default.conf default.conf.bak.$(date +%Y%m%d-%H%M%S)`), then:

```bash
docker compose exec nginx nginx -t
docker compose exec nginx nginx -s reload
```

## Verify

```bash
curl -fsS https://xiaohang.site/mcp/health | jq
curl -fsSI https://xiaohang.site/skills/ | head -3
```

## Update flow

Editing skills locally:

```bash
# 1. edit skills/*.md locally
python scripts/lint_skills.py
git commit && git push
# 2. on server:
ssh root@117.72.182.195 \
  "cd /opt/prompts-mcp && git pull && cd /opt && docker compose restart prompts-mcp"
```

Restart takes <2s; the in-memory index rebuilds on boot.

## Troubleshooting

- `docker compose logs prompts-mcp` — startup errors will show the failing skill path
- `docker compose exec prompts-mcp curl -s localhost:8080/health` — health from inside container
- Nginx upstream resolution: containers must share `opt_app-net`; if not, `docker network connect opt_app-net prompts-mcp`
