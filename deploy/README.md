# Deployment to 117.72.182.195

**Default flow: fully automated via GitHub Actions.**

```
git push  ──►  Actions builds amd64 image (~40s)
              ▼
              ghcr.io/foamtomato/prompts-mcp:latest
              ▼
              Actions SSHes into prod, runs `docker pull` from
              ghcr.nju.edu.cn mirror (CN egress is unreliable
              against ghcr.io direct), tags as prompts-mcp:latest,
              recreates the container, probes /health internally
              and externally.
              ▼
              live at https://xiaohang.site/mcp/sse  (total ~80s)
```

Workflow: `.github/workflows/docker.yml`.
Required GitHub Secrets:

| Secret | Value | How |
|---|---|---|
| `PROD_SSH_HOST` | `117.72.182.195` | `gh secret set PROD_SSH_HOST --repo …` |
| `PROD_SSH_USER` | `root` | same |
| `PROD_SSH_KEY` | full OpenSSH private key | **use `gh secret set PROD_SSH_KEY --repo … < ~/.ssh/your_key`** — paste into the web UI textarea sometimes corrupts the newlines and breaks ed25519 parsing |

The public half of `PROD_SSH_KEY` must be in the server's
`~/.ssh/authorized_keys`. Either reuse your personal key, or generate
a deploy-only key with `ssh-keygen -t ed25519 -f ~/.ssh/<name>` and
append the `.pub` to the server.

## What the deploy step actually does

After SSH-ing into the prod server, the script:

1. Tries `ghcr.nju.edu.cn` first, then `ghcr.mirrorify.net` as fallback.
2. Up to 3 attempts per mirror, 300s timeout per attempt.
3. Between attempts, `docker rmi` the half-pulled image (CN mirror's
   habit of EOF-truncating a layer otherwise leaves a poisoned cache).
4. On success, retags as `prompts-mcp:latest` (compose file references
   the plain tag so a `docker compose up -d` doesn't re-pull on restart).
5. `docker compose up -d --force-recreate prompts-mcp`.
6. Probes the container's `/health` endpoint internally; then the
   Actions runner probes the public `https://xiaohang.site/mcp/health`
   externally with 5 retries.

Total time: ~40s build + ~40s mirror pull + ~5s restart ≈ **80s end-to-end**.

## Skill content updates (no code change)

For skill data edits only — `skills/*.md` — you don't need a rebuild.
The skills directory is bind-mounted into the running container; pulling
fresh skill files on the server and restarting is enough:

```bash
# locally edit skills/*.md
python scripts/lint_skills.py
git push
ssh root@117.72.182.195 \
  "cd /opt/prompts-mcp && git pull && cd /opt && docker compose restart prompts-mcp"
```

Restart takes <2s. Index rebuilds on boot.

If you don't want to think about the two-flow distinction, `git push`
is always safe — Actions will rebuild and redeploy, which costs a
minute but produces the same outcome.

## Skill bundle (static download for quill-plugin)

Plugin clients (e.g. [quill-plugin](https://github.com/foamtomato/quill-plugin))
need a plain `curl`-able tarball of `skills/` for first-run and auto-update.
That's served at `https://xiaohang.site/skills/bundle/` and built by a
**separate** workflow: `.github/workflows/bundle.yml`.

```
git push (skills/*.md or scripts/build_bundle.sh)
   │
   ▼
Actions: scripts/build_bundle.sh →
   dist/{bundle.tar.gz, bundle.tar.gz.sha256, version.txt, manifest.json, SHA256SUMS}
   │
   ▼
SCP to prod:/var/www/skills-bundle/releases/<timestamp>/
   │
   ▼  (atomic symlink swap inside that dir)
nginx serves /skills/bundle/<file>  →  alias /var/www/skills-bundle/
   │
   ▼
plugin: curl https://xiaohang.site/skills/bundle/bundle.tar.gz
```

### Why a separate workflow

Skill content commits are frequent and cheap (no docker build). Coupling
the bundle into `docker.yml` would force a 60s container rebuild on every
typo fix. `bundle.yml` runs in ~15s and only touches `skills/`-relevant
paths (see `on.push.paths`).

### One-time server setup (do this once, then `git push` is enough)

```bash
# 1. Create the static dir & seed the symlink targets so nginx has something to alias on first request.
ssh root@117.72.182.195 'mkdir -p /var/www/skills-bundle/releases && touch /var/www/skills-bundle/version.txt'

# 2. Append the nginx block (see deploy/nginx-bundle-snippet.conf) into
#    /opt/nginx/conf.d/default.conf, inside the xiaohang.site server block,
#    BEFORE the existing `location /skills/` so the more specific prefix wins.
ssh root@117.72.182.195
cd /opt
cp nginx/conf.d/default.conf nginx/conf.d/default.conf.bak.$(date +%Y%m%d-%H%M%S)
vi nginx/conf.d/default.conf   # paste deploy/nginx-bundle-snippet.conf content
docker compose exec nginx nginx -t
docker compose exec nginx nginx -s reload
exit

# 3. Trigger the bundle workflow (or push any skills/ commit) so the first
#    bundle lands on disk.
gh workflow run bundle.yml --repo foamtomato/Prompts-MCP

# 4. Verify
curl -fsS https://xiaohang.site/skills/bundle/version.txt
curl -fsS https://xiaohang.site/skills/bundle/manifest.json | jq
curl -fsSI https://xiaohang.site/skills/bundle/bundle.tar.gz | head -5
```

### Atomic publish semantics

Each push lands in `/var/www/skills-bundle/releases/<YYYYMMDD-HHMMSS>/`,
then `ln -sfn` + `mv -Tf` swap the top-level pointers atomically. A
client mid-`curl` either:

- Already started streaming the old tarball — finishes against the old
  file (the inode is still alive until its fd closes).
- Hasn't connected yet — next request reads the new symlink.

There's no partial-file race; the plugin's `sha256` check is belt-and-
suspenders against transit corruption only.

Releases older than the 10 most recent are auto-pruned by the workflow.

### Local bundle build (emergency / dry-run)

```bash
bash scripts/build_bundle.sh
ls -la dist/    # bundle.tar.gz, version.txt, manifest.json, SHA256SUMS
# scp dist/* root@117.72.182.195:/var/www/skills-bundle/releases/manual-$(date +%Y%m%d-%H%M%S)/
# (and then ln -sfn + mv -Tf the symlinks by hand)
```

## Emergency fallback: local build + scp

If GitHub is down, or both GHCR mirrors are EOF-broken, or you need to
deploy without going through Actions:

```bash
./scripts/deploy_image.sh
```

This builds amd64 locally (requires Docker Hub reachable via your dev
machine's proxy), saves a ~200MB tar, scps it to the server, docker-
loads it, recreates the container. Slower (~5min total) but completely
independent of Actions, GHCR, and mirrors.

After scp deploy the compose file ends up referencing `prompts-mcp:latest`
locally. The next Actions deploy will pull from the mirror, retag to
the same name, and `--force-recreate`, which is a clean no-op switch.

## One-time setup (if redeploying from scratch)

```bash
ssh root@117.72.182.195 'cd /opt && git clone https://github.com/FoamTomato/Prompts-MCP.git prompts-mcp'
ssh root@117.72.182.195 'cp /opt/docker-compose.yml /opt/docker-compose.yml.bak.$(date +%Y%m%d-%H%M%S)'
# Append the snippet from deploy/docker-compose.prod.yml into /opt/docker-compose.yml
# Append deploy/nginx-snippet.conf into /opt/nginx/conf.d/default.conf, then `nginx -s reload`
```

After that, a `git push` to main is the only command you need.

## Verify

```bash
curl -fsS https://xiaohang.site/mcp/health | jq
ssh root@117.72.182.195 'docker inspect prompts-mcp --format "{{.Image}}  created={{.Created}}"'
```

The `Created` timestamp on the container should be within a couple
of minutes of your last `git push`.

## Troubleshooting

- **Deploy step fails at "Set up SSH" with libcrypto error** —
  PROD_SSH_KEY was corrupted by the web textarea. Re-upload with
  `gh secret set PROD_SSH_KEY --repo … < ~/.ssh/your_key`.
- **Deploy step fails with "All mirrors failed"** — Both nju and
  mirrorify ate it today. Run `./scripts/deploy_image.sh` locally.
- **Container up but `/mcp/health` 502** — Nginx upstream resolution.
  Check `docker inspect prompts-mcp --format '{{json .NetworkSettings.Networks}}'`
  has `opt_app-net` in it.
- **Container restart loop** — `docker compose logs prompts-mcp`; the
  failing skill path is usually in the last 5 lines.
