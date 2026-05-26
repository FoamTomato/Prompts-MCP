---
name: fastapi-storage-signed-upload
description: 签名直传流程 — 客户端拿 STS / 预签名 URL → 直传 OSS。Use when 写 Python 后端代码 / 评审涉及 `signed-upload`
  的 PR。
parent: ./index.md
paths:
- backend/services/oss*.py
- '**/services/oss*.py'
triggers:
  keywords:
  - signed
  - STS
  - presigned
  - upload
  - 签名直传流程
  - 客户端拿
  - 预签名
effort: medium
context: inline
version: '1.0'
---
# OSS · 签名直传

## 规则

**前端用预签名 URL 直接上传到 OSS**，不经过 backend 中转。

## 流程

```
1. 前端 → backend POST /api/assets/upload-url （含 fileName, mimeType, size）
2. backend 校验配额 / mimeType / size，生成 OSS 预签名 URL，返回前端
3. 前端 PUT 文件到该 URL（直传 OSS）
4. 前端 → backend POST /api/assets/confirm （含 OSS 路径 + 元数据）
5. backend 写 DB，返回 asset_id
```

## backend 实现

```python
# backend/services/oss.py
import oss2
import uuid
from datetime import datetime
from core.config import settings

bucket = oss2.Bucket(
    oss2.Auth(settings.oss_access_key, settings.oss_secret_key),
    settings.oss_endpoint,
    "app-assets",
)

async def generate_upload_url(
    tenant_id: str,
    file_name: str,
    mime_type: str,
    size_bytes: int,
) -> dict:
    # 校验
    if size_bytes > 50 * 1024 * 1024:   # 50MB
        raise ApiException(msg="单文件不超过 50MB", code=413)

    if mime_type.startswith("image/"):
        ext = mime_type.split("/")[1]
        type_dir = "images"
    elif mime_type.startswith("video/"):
        ext = "mp4"
        type_dir = "videos"
    else:
        raise ApiException(msg="不支持的文件类型", code=400)

    # 生成路径
    now = datetime.now()
    asset_id = str(uuid.uuid4())
    object_key = f"{tenant_id}/{type_dir}/{now.year}/{now.month:02d}/{asset_id}.{ext}"

    # 签名（30 分钟有效）
    url = bucket.sign_url("PUT", object_key, 30 * 60, headers={"Content-Type": mime_type})

    return {
        "upload_url": url,
        "object_key": object_key,
        "asset_id": asset_id,
        "expires_in": 30 * 60,
    }
```

## 前端调用

```ts
// 1. 拿预签名 URL
const { upload_url, object_key, asset_id } = await api.post("/assets/upload-url", {
  fileName: file.name,
  mimeType: file.type,
  size: file.size,
});

// 2. 直传 OSS
await fetch(upload_url, {
  method: "PUT",
  headers: { "Content-Type": file.type },
  body: file,
});

// 3. 确认入库
await api.post("/assets/confirm", { asset_id, object_key, name: file.name });
```

## 为什么不走 backend 中转

| 直传 | 中转 |
|------|------|
| backend 无负载 | backend CPU/带宽双重消耗 |
| 大文件不超时 | 大文件易超时 |
| 简单 | 复杂（流式接收 / 转发） |

## STS 临时凭证（更安全）

如果对 IAM 严格，可让前端用临时 STS 凭证（每次过期），直接调 OSS SDK。预签名 URL 通常已够用。

## 自检

- [ ] 前端直传，不经 backend？
- [ ] 预签名 URL 过期时间 ≤ 1 小时？
- [ ] backend 校验 size / mimeType / 配额？
- [ ] object_key 含 tenant_id / type / 日期？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`bucket-layout.md`](./bucket-layout.md) · [`lifecycle-and-cache.md`](./lifecycle-and-cache.md)
