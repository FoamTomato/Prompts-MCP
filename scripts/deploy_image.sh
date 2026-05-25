#!/usr/bin/env bash
# Build, transfer, and load the prompts-mcp image onto the production server.
# Assumes ~/.ssh/config (or default key) allows `ssh root@117.72.182.195` without prompts.
#
# Usage:
#   ./scripts/deploy_image.sh              # build :latest + :0.1.0, ship to default host
#   PROD_HOST=... ./scripts/deploy_image.sh
#   IMAGE_TAG=0.2.0 ./scripts/deploy_image.sh
set -euo pipefail

PROD_HOST="${PROD_HOST:-root@117.72.182.195}"
IMAGE_NAME="${IMAGE_NAME:-prompts-mcp}"
IMAGE_TAG="${IMAGE_TAG:-$(python3 -c 'import tomllib; print(tomllib.load(open("pyproject.toml","rb"))["project"]["version"])')}"
TAR_PATH="${TAR_PATH:-/tmp/${IMAGE_NAME}.tar}"

cd "$(dirname "$0")/.."

echo "==> Building ${IMAGE_NAME}:${IMAGE_TAG} + :latest"
docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" -t "${IMAGE_NAME}:latest" .

echo "==> Saving image to ${TAR_PATH}"
docker save "${IMAGE_NAME}:${IMAGE_TAG}" "${IMAGE_NAME}:latest" -o "${TAR_PATH}"
ls -lh "${TAR_PATH}"

echo "==> Transferring to ${PROD_HOST}:${TAR_PATH}"
scp "${TAR_PATH}" "${PROD_HOST}:${TAR_PATH}"

echo "==> Loading + restarting service on ${PROD_HOST}"
ssh "${PROD_HOST}" "docker load -i ${TAR_PATH} && cd /opt && docker compose up -d prompts-mcp && docker compose ps prompts-mcp"

echo "==> Done. Verify:"
echo "   curl -fsS https://xiaohang.site/mcp/health"
