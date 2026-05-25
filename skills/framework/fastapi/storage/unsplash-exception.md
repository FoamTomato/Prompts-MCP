---
name: fastapi-storage-unsplash
description: Unsplash 例外 — 不入 OSS，直接转链 + 缓存元数据
parent: ./index.md
paths:
  - "backend/services/oss*.py"
  - "py/services/oss*.py"
  - "backend/services/asset*.py"
triggers:
  keywords: [Unsplash, 图片, 转链]
effort: medium
context: inline
version: "1.0"
---

# OSS · Unsplash 例外

## 规则

**Unsplash 图片不入 OSS，直接转链 + 缓存元数据**。

## 为什么

1. Unsplash 已经有 CDN（imgix），性能好
2. Unsplash 许可证要求保留来源链接
3. 节省存储成本
4. 不与原作者关系混淆

## 数据模型

```python
# assets 表
class Asset(Model):
    id = fields.UUIDField(pk=True)
    session_id = fields.CharField(max_length=64, index=True)
    type = fields.CharField(max_length=20)         # "image" / "unsplash" / ...
    source = fields.CharField(max_length=20)       # "user-upload" / "unsplash" / "ai-gen"
    url = fields.CharField(max_length=500)         # OSS URL 或 unsplash CDN URL
    width = fields.IntField()
    height = fields.IntField()
    size_bytes = fields.BigIntField(null=True)     # unsplash 可空

    # Unsplash 特有
    unsplash_id = fields.CharField(max_length=64, null=True, index=True)
    unsplash_author = fields.CharField(max_length=200, null=True)
    unsplash_author_link = fields.CharField(max_length=500, null=True)

    class Meta:
        table = "assets"
```

## Service 流程

```python
# backend/services/asset.py

async def add_unsplash_asset(session_id: str, photo: dict) -> Asset:
    """photo 来自 unsplash API 返回"""
    return await Asset.create(
        session_id=session_id,
        type="image",
        source="unsplash",
        url=photo["urls"]["regular"],     # 直接用 Unsplash CDN URL
        width=photo["width"],
        height=photo["height"],
        unsplash_id=photo["id"],
        unsplash_author=photo["user"]["name"],
        unsplash_author_link=photo["user"]["links"]["html"],
    )
```

## 前端展示

```tsx
function AssetThumb({ asset }: { asset: Asset }) {
  return (
    <div className="asset-thumb">
      <img src={asset.url} alt="" />
      {asset.source === "unsplash" && (
        <a
          href={asset.unsplash_author_link}
          target="_blank"
          rel="noopener"
          className="credit"
        >
          Photo by {asset.unsplash_author} on Unsplash
        </a>
      )}
    </div>
  );
}
```

## 反例

```python
# ❌ 把 Unsplash 图片下载到自己 OSS
photo_bytes = await fetch_unsplash(photo_url)
await oss_upload(photo_bytes, "...")
# 1. 浪费存储 / 带宽
# 2. 失去 author credit 链接
# 3. 违反许可证
```

## 自检

- [ ] Unsplash 图直接转链，不入 OSS？
- [ ] 保留 author / author_link 字段？
- [ ] 前端展示 Author Credit？
- [ ] CHECK 约束：`source='unsplash' AND unsplash_id IS NOT NULL`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`bucket-layout.md`](./bucket-layout.md)

