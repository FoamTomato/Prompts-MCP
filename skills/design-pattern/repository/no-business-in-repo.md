---
name: repository-no-business
description: 禁在 Repo 写业务规则 — 业务校验在 Service。Use when 写 Python 后端代码 / 评审涉及 `no-business-in-repo`
  的 PR。
parent: ./index.md
paths:
- backend/repositories/**/*.py
- py/repositories/**/*.py
triggers:
  keywords:
  - Repository
  - 业务规则
  - 校验
effort: medium
context: inline
version: '1.0'
---
# Repository · 禁业务逻辑

## 规则

Repo 内**只能有 ORM 调用与字段映射**。任何 if / for 业务判断都属于"业务逻辑下沉"，必须搬到 Service。

## 反例 → 正例

```python
# ❌ Repo 写业务规则
class PresentationRepo:
    async def find_owned_publishable(self, owner_id: UUID) -> list[Presentation]:
        items = await Presentation.filter(owner_id=owner_id).all()
        # 业务判断：什么算 "publishable"
        return [p for p in items if p.slide_count >= 5 and p.theme_id is not None]

# ✅ Repo 只提供查询能力，业务判断在 Service
class PresentationRepo:
    async def find_by_owner_with_min_slides(
        self,
        owner_id: UUID,
        *,
        min_slides: int = 0,
        require_theme: bool = False,
    ) -> list[Presentation]:
        q = Presentation.filter(owner_id=owner_id, slide_count__gte=min_slides)
        if require_theme:
            q = q.filter(theme_id__isnull=False)
        return await q.all()

class PresentationService:
    async def list_publishable(self, owner_id: UUID) -> list[Presentation]:
        # 业务定义 "publishable" = slide_count >= 5 AND has theme
        return await self.repo.find_by_owner_with_min_slides(
            owner_id, min_slides=5, require_theme=True,
        )
```

差别：业务规则"什么算 publishable"在 Service，Repo 只提供原子查询能力。

## 哪些算业务规则

| 是 | 不是 |
|----|------|
| "slide_count >= 5" 表示完整 | id 大于 0 |
| "is_paid 才能导出" | created_at < now() |
| "重复购买拦截" | unique 约束 |
| 跨字段组合判断 | 单字段精确匹配 |

## Repo 允许做的"业务无关"过滤

```python
# ✅ 通用查询参数
async def find_by_owner(
    self,
    owner_id: UUID,
    *,
    limit: int = 20,
    offset: int = 0,
    order_by: str = "-created_at",
    include_deleted: bool = False,    # 软删除 — 是技术细节而非业务
) -> list[Presentation]: ...
```

包含 / 排除软删除是技术约束，不算业务。

## 自检

- [ ] Repo 方法体内无 if / for 业务判断？
- [ ] 业务定义（什么叫"completed"、"publishable"）在 Service？
- [ ] Repo 提供"参数化"的原子查询能力，让 Service 组合？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`crud-contract.md`](./crud-contract.md)

