---
name: fastapi-storage-bucket
description: OSS Bucket 分桶 — assets/thumbnails/exports/backups/ai-images。Use when
  写 Python 后端代码 / 评审涉及 `bucket-layout` 的 PR。
parent: ./index.md
paths:
- backend/services/oss*.py
- '**/services/oss*.py'
- backend/core/config.py
triggers:
  keywords:
  - bucket
  - OSS
  - MinIO
  - S3
  - 分桶
effort: medium
context: inline
version: '1.0'
---
# OSS · Bucket 划分

## 五桶方案

| Bucket | 用途 | 访问性 | 域名（生产） |
|--------|------|--------|---------|
| `app-assets` | 用户上传的图片 / 视频 / 字体 | 公开读，私写 | `https://assets.example.com` |
| `app-thumbnails` | 视频缩略图、用户头像 | 公开读 | `https://thumbs.example.com` |
| `app-exports` | 导出的 .pptx / .pdf / .zip | 私有（签名读） | `https://exports.example.com` |
| `app-backups` | tenant 备份文件 .backup | 私有（签名读） | `https://backups.example.com` |
| `app-ai-images` | AI 生图结果（独立桶便于成本核算） | 公开读 | `https://ai.example.com` |

## 开发环境

单一 MinIO bucket `app-dev`，目录前缀区分（`assets/` / `thumbnails/` / ...），节省配置成本。

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
├── {tenant_id}/
│   ├── images/2026/05/{asset_id}.jpg
│   ├── videos/2026/05/{asset_id}.mp4
│   ├── fonts/{font_id}.woff2
│   └── ai-images/2026/05/{asset_id}.png
└── shared/
    └── system/
```

按 tenant 分目录，便于：
- 清理：tenant 过期一并清理目录
- 配额：按目录计算用量
- 隔离：tenant A 无法访问 tenant B 的目录（IAM 策略）

## 命名约定

| 资源 | 格式 |
|------|------|
| asset 文件名 | `{asset_id}.{ext}` UUID + 后缀（不保留原文件名） |
| 路径前缀 | `{tenant_id}/{type}/{year}/{month}/` |
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
- [ ] 路径含 tenant_id 便于清理？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`signed-upload.md`](./signed-upload.md) · [`lifecycle-and-cache.md`](./lifecycle-and-cache.md) · [`unsplash-exception.md`](./unsplash-exception.md)
