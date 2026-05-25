# Deployment to 117.72.182.195

The production server has no outbound proxy, so pulling images from GHCR is
unreliably slow. The canonical workflow is **build locally, save tar, scp,
docker load** — fully automated by `scripts/deploy_image.sh`.

GitHub Actions still publishes the same image to
`ghcr.io/foamtomato/prompts-mcp:latest` for any other host with reliable
outbound internet — but the production server here always goes through scp.

A working copy of the repo is also cloned to `/opt/prompts-mcp/` because the
**skills directory** (`/opt/prompts-mcp/skills`) is bind-mounted into the
container read-only. Updating skill content alone is a `git pull` + restart,
no image rebuild needed.

## One-time setup

```bash
# 1. clone the repo on the server (for skills/ volume + reference manifests)
ssh root@117.72.182.195 'cd /opt && git clone https://github.com/FoamTomato/Prompts-MCP.git prompts-mcp'

# 2. append the prompts-mcp service block from deploy/docker-compose.prod.yml
#    into /opt/docker-compose.yml (inside the existing top-level services: map,
#    before networks:). Back up first:
ssh root@117.72.182.195 'cp /opt/docker-compose.yml /opt/docker-compose.yml.bak.$(date +%Y%m%d-%H%M%S)'

# 3. append deploy/nginx-snippet.conf into the
#    `server { listen 443 ssl; server_name xiaohang.site; ... }`
#    block of /opt/nginx/conf.d/default.conf. Back up similarly.

# 4. ship the image:
./scripts/deploy_image.sh

# 5. reload nginx:
ssh root@117.72.182.195 'cd /opt && docker compose exec nginx nginx -t && docker compose exec nginx nginx -s reload'
```

## Verify

```bash
# from the server
ssh root@117.72.182.195 'docker exec nginx curl -fsS http://prompts-mcp:8080/health'
# from anywhere
curl -fsS https://xiaohang.site/mcp/health
curl -fsSI https://xiaohang.site/skills/ | head -3
```

## Update flow

### Code change (rebuild image)

```bash
git push                       # CI builds + publishes to GHCR (informational)
./scripts/deploy_image.sh      # build locally, scp, load, restart
```

### Skill content only (no code change)

```bash
# locally edit skills/*.md
python scripts/lint_skills.py
git push
ssh root@117.72.182.195 \
  "cd /opt/prompts-mcp && git pull && cd /opt && docker compose restart prompts-mcp"
```

Restart takes <2s; the in-memory index rebuilds on boot.

## Troubleshooting

- `docker compose logs prompts-mcp` — startup errors show the failing skill path
- `docker exec prompts-mcp python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8080/health').read())"`
- Nginx upstream resolution: containers must share `opt_app-net`. Verify with
  `docker inspect prompts-mcp --format '{{json .NetworkSettings.Networks}}'`.
- Nginx `host not found in upstream "prompts-mcp"` after editing default.conf —
  start the `prompts-mcp` container first, *then* `nginx -s reload`.
