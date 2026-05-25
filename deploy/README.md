# Deployment to 117.72.182.195

The image is built and published by GitHub Actions (`.github/workflows/docker.yml`)
to `ghcr.io/foamtomato/prompts-mcp:latest` on every push to `main`. The server
only pulls — no source code or build toolchain is required there beyond what
docker needs for `docker compose pull`.

A working copy of the repo is still cloned to `/opt/prompts-mcp/` because the
**skills directory** (`/opt/prompts-mcp/skills`) is mounted into the container
read-only. Updating skill content = `git pull && docker compose restart prompts-mcp`.

## One-time setup

```bash
ssh root@117.72.182.195
cd /opt
git clone https://github.com/FoamTomato/Prompts-MCP.git prompts-mcp
```

Append the `prompts-mcp:` service block from `deploy/docker-compose.prod.yml`
into `/opt/docker-compose.yml` (inside the existing top-level `services:` map,
before `networks:`). Back up first:

```bash
cp /opt/docker-compose.yml /opt/docker-compose.yml.bak.$(date +%Y%m%d-%H%M%S)
```

Append `deploy/nginx-snippet.conf` into the `server { server_name xiaohang.site; listen 443 ssl; ... }`
block of `/opt/nginx/conf.d/default.conf` (back up that file similarly).

Pull the image and bring the service up:

```bash
cd /opt
docker compose pull prompts-mcp
docker compose up -d prompts-mcp
docker compose ps prompts-mcp
docker compose logs --tail=50 prompts-mcp
```

Reload nginx:

```bash
docker compose exec nginx nginx -t
docker compose exec nginx nginx -s reload
```

## Verify

```bash
# from the server
docker exec nginx curl -fsS http://prompts-mcp:8080/health     # internal
curl -fsS https://xiaohang.site/mcp/health                    # external
curl -fsSI https://xiaohang.site/skills/ | head -3
```

## Update flow

### Update code

```bash
# locally
git push
# GitHub Actions builds and pushes a new image to GHCR
# then on the server:
ssh root@117.72.182.195 "cd /opt && docker compose pull prompts-mcp && docker compose up -d prompts-mcp"
```

### Update skill content only (no code change)

```bash
# locally edit skills/*.md
python scripts/lint_skills.py
git push
# on server:
ssh root@117.72.182.195 \
  "cd /opt/prompts-mcp && git pull && cd /opt && docker compose restart prompts-mcp"
```

The skills directory is bind-mounted into the container, so a git pull on the
server is enough — no image rebuild needed for content-only changes. Restart
takes <2s; the in-memory index rebuilds on boot.

## Troubleshooting

- `docker compose logs prompts-mcp` — startup errors show the failing skill path
- `docker exec prompts-mcp python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8080/health').read())"`
- Nginx upstream resolution: containers must share `opt_app-net`. Verify with
  `docker inspect prompts-mcp --format '{{json .NetworkSettings.Networks}}'`.
- GHCR pull denied: ensure the package visibility is set to **public** in
  https://github.com/users/FoamTomato/packages/container/prompts-mcp/settings —
  GHCR images inherit repo visibility for the *first* push only.
