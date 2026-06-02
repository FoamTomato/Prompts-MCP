#!/usr/bin/env bash
#
# build_bundle.sh — 打 skill bundle.tar.gz + 算 sha256 + 写 version.txt
#
# 输出（在 dist/ 下）：
#   bundle.tar.gz          # tar -czf 后的 skills/ 目录
#   bundle.tar.gz.sha256   # 单行 sha256
#   version.txt            # 单行版本字符串（git tag 或 main-<sha>）
#   SHA256SUMS             # 多文件 sha256 清单（user-friendly）
#
# 上传逻辑见 .github/workflows/bundle.yml；本脚本只负责"打包"，不负责"传输"，
# 便于本地手工兜底也能跑（CI 故障时手动 scp dist/* 到服务器）。

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST_DIR="$REPO_ROOT/dist"

cd "$REPO_ROOT"

# --- 1. 版本字符串 -----------------------------------------------------------

if VERSION="$(git describe --tags --exact-match 2>/dev/null)"; then
    : # tag 触发，version = vX.Y.Z
elif COMMIT="$(git rev-parse --short HEAD 2>/dev/null)"; then
    VERSION="main-${COMMIT}"
else
    VERSION="dev-$(date +%Y%m%d-%H%M%S)"
fi

echo "[build_bundle] version: $VERSION"

# --- 2. 准备 dist/ ----------------------------------------------------------

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# --- 3. 打包 skills/ -------------------------------------------------------

if [ ! -d "$REPO_ROOT/skills" ]; then
    echo "ERROR: skills/ directory not found at repo root" >&2
    exit 1
fi

SKILL_COUNT="$(find "$REPO_ROOT/skills" -name '*.md' -type f | wc -l | tr -d ' ')"
echo "[build_bundle] packing $SKILL_COUNT skill files"

# 排除常见杂项 + 确保 tar 内部路径以 skills/ 开头
tar \
    --exclude='.DS_Store' \
    --exclude='*.swp' \
    --exclude='__pycache__' \
    -czf "$DIST_DIR/bundle.tar.gz" \
    -C "$REPO_ROOT" \
    skills

BUNDLE_SIZE="$(du -h "$DIST_DIR/bundle.tar.gz" | awk '{print $1}')"
echo "[build_bundle] bundle size: $BUNDLE_SIZE"

# --- 4. sha256 -------------------------------------------------------------

BUNDLE_SHA="$(shasum -a 256 "$DIST_DIR/bundle.tar.gz" | awk '{print $1}')"
echo "$BUNDLE_SHA" > "$DIST_DIR/bundle.tar.gz.sha256"

# 兼容 Linux/macOS：写 SHA256SUMS 时只用相对文件名
(
    cd "$DIST_DIR"
    shasum -a 256 bundle.tar.gz > SHA256SUMS
)

echo "[build_bundle] sha256: $BUNDLE_SHA"

# --- 5. version.txt + manifest.json ---------------------------------------

echo "$VERSION" > "$DIST_DIR/version.txt"

# manifest.json — 给 plugin 端在不解 bundle 的情况下也能看到清单 + sha
cat > "$DIST_DIR/manifest.json" <<EOF
{
  "version": "$VERSION",
  "built_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "skill_count": $SKILL_COUNT,
  "bundle": {
    "filename": "bundle.tar.gz",
    "sha256": "$BUNDLE_SHA",
    "size_bytes": $(wc -c < "$DIST_DIR/bundle.tar.gz" | tr -d ' ')
  }
}
EOF

# --- 6. 报告 ---------------------------------------------------------------

echo ""
echo "=== bundle artifacts ==="
ls -la "$DIST_DIR"
echo ""
echo "=== version.txt ==="
cat "$DIST_DIR/version.txt"
echo ""
echo "=== manifest.json ==="
cat "$DIST_DIR/manifest.json"
