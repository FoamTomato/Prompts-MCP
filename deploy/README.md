# Deployment to 117.72.182.195

The production server pulls from a **GHCR mirror** (`ghcr.nju.edu.cn`,
南京大学开源镜像站) because direct `ghcr.io` pulls from this server's CN
egress are unreliably slow (>10 minutes observed). The mirror cuts that to
~40s for a cold pull and ~3s when layers are cached.

GitHub Actions still publishes to `ghcr.io/foamtomato/prompts-mcp:latest`;
the mirror re-serves the same image transparently — no extra publishing
step. Both mirrors below are interchangeable:

| Mirror | Speed observed |
|--------|----------------|
| `ghcr.nju.edu.cn/foamtomato/prompts-mcp:latest` | ~40s cold (primary) |
| `ghcr.mirrorify.net/foamtomato/prompts-mcp:latest` | ~40s cold (backup) |
| `ghcr.io/foamtomato/prompts-mcp:latest` | >10min (do not use) |

Swap the host prefix in `/opt/docker-compose.yml`'s `image:` line if the
primary is down. The `latest` tag and image digest match across mirrors.

If both mirrors fail, fall back to **build-locally + scp + docker load** —
fully automated by `scripts/deploy_image.sh`. This requires the dev
machine to be able to reach Docker Hub (proxy configured).

A working copy of the repo is also cloned to `/opt/prompts-mcp/` because
the **skills directory** (`/opt/prompts-mcp/skills`) is bind-mounted into
the container read-only. Updating skill content alone is a `git pull` +
restart, no image rebuild needed.

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

# 4. pull image + bring up:
ssh root@117.72.182.195 'cd /opt && docker compose pull prompts-mcp && docker compose up -d prompts-mcp'

# 5. reload nginx:
ssh root@117.72.182.195 'cd /opt && docker compose exec nginx nginx -t && docker compose exec nginx nginx -s reload'
```

## Verify

```bash
ssh root@117.72.182.195 'docker exec nginx curl -fsS http://prompts-mcp:8080/health'
curl -fsS https://xiaohang.site/mcp/health
curl -fsSI https://xiaohang.site/skills/ | head -3
```

## Update flow

### Code change (rebuild image)

```bash
git push                       # CI builds + publishes to GHCR (mirrored automatically)
ssh root@117.72.182.195 'cd /opt && docker compose pull prompts-mcp && docker compose up -d prompts-mcp'
```

Typical end-to-end: 60s for Actions build + ~40s mirror pull on cold start ≈ **under 2 minutes**.

### Skill content only (no code change)

```bash
# locally edit skills/*.md
python scripts/lint_skills.py
git push
ssh root@117.72.182.195 \
  "cd /opt/prompts-mcp && git pull && cd /opt && docker compose restart prompts-mcp"
```

Restart takes <2s; the in-memory index rebuilds on boot. No image pull needed.

### Emergency fallback — direct scp

If both mirrors are down:

```bash
./scripts/deploy_image.sh
```

Builds amd64 locally (needs working proxy to Docker Hub), saves a 200MB
tar, scps it up, docker-loads it, and recreates the container. Slower
(~5min total) but completely independent of GHCR.

## Troubleshooting

- `docker compose logs prompts-mcp` — startup errors show the failing skill path
- `docker exec prompts-mcp python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8080/health').read())"`
- Nginx upstream resolution: containers must share `opt_app-net`. Verify with
  `docker inspect prompts-mcp --format '{{json .NetworkSettings.Networks}}'`.
- Mirror down: edit `/opt/docker-compose.yml`, swap `ghcr.nju.edu.cn` →
  `ghcr.mirrorify.net`, re-run `docker compose pull && up -d`.
- Both mirrors down: run `./scripts/deploy_image.sh` from the dev machine.
