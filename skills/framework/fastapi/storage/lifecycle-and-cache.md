---
name: fastapi-storage-lifecycle
description: OSS 生命周期与缓存 — TTL / 回源 / CDN。Use when 写 Python 后端代码 / 评审涉及 `lifecycle-and-cache`
  的 PR。
parent: ./index.md
paths:
- backend/services/oss*.py
- '**/services/oss*.py'
triggers:
  keywords:
  - lifecycle
  - TTL
  - cache
  - CDN
  - 生命周期
  - 命周期与
  - 周期与缓
effort: medium
context: inline
version: '1.0'
---
# OSS · 生命周期与缓存

## Bucket 生命周期规则

| Bucket | 规则 |
|--------|------|
| `app-assets` | tenant 删除 90 天后清理；最大 5GB / tenant |
| `app-thumbnails` | 跟随源资产；源删除时一并删 |
| `app-exports` | 7 天后清理（用户已下载） |
| `app-backups` | 90 天后清理；保留最近 30 个版本 |
| `app-ai-images` | tenant 删除 90 天后清理；最大 1GB / tenant |

## OSS 控制台配置（lifecycle.xml）

```xml
<LifecycleConfiguration>
  <Rule>
    <ID>delete-orphan-after-90d</ID>
    <Status>Enabled</Status>
    <Prefix></Prefix>
    <Tag>
      <Key>tenant-status</Key>
      <Value>deleted</Value>
    </Tag>
    <Expiration>
      <Days>90</Days>
    </Expiration>
  </Rule>
</LifecycleConfiguration>
```

tenant 删除时**给 OSS 对象打 tag** `tenant-status=deleted`，OSS 自动 90 天后清理。

## CDN 缓存

| 资源 | CDN cache TTL |
|------|--------------|
| `app-assets` 图片 | 30 天（不变） |
| `app-thumbnails` | 30 天 |
| `app-ai-images` | 30 天 |
| `app-exports` | 不走 CDN（私有签名） |
| `app-backups` | 不走 CDN |

## URL 拼接

```python
def get_asset_url(object_key: str, transform: str | None = None) -> str:
    base = f"https://assets.example.com/{object_key}"
    if transform:
        return f"{base}?x-oss-process={transform}"
    return base

# 缩略图按需生成
thumb_url = get_asset_url(
    "tenant_abc/images/2026/05/uuid.jpg",
    "image/resize,w_400,h_300/format,webp",
)
```

OSS 自带按需图像处理（resize / crop / format），不需要 backend 生成。

## 缓存失效

```python
# 用户更新封面时，旧 URL 缓存仍有效（30 天）
# 解法 1：URL 含版本号（推荐）
url = f"{base}?v={asset.updated_at.timestamp()}"

# 解法 2：用 OSS 刷新 API（贵 + 慢）
client.refresh_object(object_key)
```

## 私有读签名

```python
def get_export_signed_url(object_key: str, expires_sec: int = 600) -> str:
    bucket = get_bucket("app-exports")
    return bucket.sign_url("GET", object_key, expires_sec)
```

10 分钟有效的私有下载链接。

## 自检

- [ ] 每个 bucket 有 lifecycle 规则？
- [ ] tenant 删除时打 tag 触发自动清理？
- [ ] 公开 bucket 走 CDN，私有不走？
- [ ] URL 含版本号或 timestamp 避免缓存？
- [ ] 私有读用签名 URL？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`bucket-layout.md`](./bucket-layout.md) · [`signed-upload.md`](./signed-upload.md)
