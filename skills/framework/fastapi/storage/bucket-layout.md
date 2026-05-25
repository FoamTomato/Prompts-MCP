---
name: fastapi-storage-bucket
description: OSS Bucket 分桶 — assets/thumbnails/exports/backups/ai-images
parent: ./index.md
paths:
  - "backend/services/oss*.py"
  - "py/services/oss*.py"
  - "backend/core/config.py"
triggers:
  keywords: [bucket, OSS, MinIO, S3]
effort: medium
context: inline
version: "1.0"
---

# OSS · Bucket 划分

## 五桶方案

| Bucket | 用途 | 访问性 | 域名（生产） |
|--------|------|--------|---------|
| `quill-assets` | 用户上传的图片 / 视频 / 字体 | 公开读，私写 | `https://assets.quill.app` |
| `quill-thumbnails` | 视频缩略图、用户头像 | 公开读 | `https://thumbs.quill.app` |
| `quill-exports` | 导出的 .pptx / .pdf / .zip | 私有（签名读） | `https://exports.quill.app` |
| `quill-backups` | session 备份文件 .quill-backup | 私有（签名读） | `https://backups.quill.app` |
| `quill-ai-images` | AI 生图结果（独立桶便于成本核算） | 公开读 | `https://ai.quill.app` |

## 开发环境

单一 MinIO bucket `quill-dev`，目录前缀区分（`assets/` / `thumbnails/` / ...），节省配置成本。

```bash
# docker-compose.yml
minio:
  image: minio/minio
  ports:
    - "9000:9000"
    - "9001:9001"
  environment:
    MINIO_ROOT_USER: minioadmin
    MINIO_ROOT_PASSWORD: minioadmin
  command: server /data --console-address ":9001"
```

## 目录结构

```
{bucket}/
├── {session_id}/
│   ├── images/2026/05/{asset_id}.jpg
│   ├── videos/2026/05/{asset_id}.mp4
│   ├── fonts/{font_id}.woff2
│   └── ai-images/2026/05/{asset_id}.png
└── shared/
    └── system/
```

按 session 分目录，便于：
- 清理：session 过期一并清理目录
- 配额：按目录计算用量
- 隔离：session A 无法访问 session B 的目录（IAM 策略）

## 命名约定

| 资源 | 格式 |
|------|------|
| asset 文件名 | `{asset_id}.{ext}` UUID + 后缀（不保留原文件名） |
| 路径前缀 | `{session_id}/{type}/{year}/{month}/` |
| 缩略图 | `{asset_id}_thumb.jpg`（同目录） |

## 跨桶引用

```sql
-- assets 表
url VARCHAR(500)  -- 完整 URL 包含 bucket 域名
type VARCHAR(20)  -- "image" / "video" / "font" / "ai-image"
size_bytes BIGINT
```

## 自检

- [ ] 生产用 5 个独立 bucket？
- [ ] 开发用 MinIO 单 bucket + 目录前缀？
- [ ] 文件名用 UUID 不保留原名？
- [ ] 路径含 session_id 便于清理？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`signed-upload.md`](./signed-upload.md) · [`lifecycle-and-cache.md`](./lifecycle-and-cache.md) · [`unsplash-exception.md`](./unsplash-exception.md)

