---
name: ddd-repository-thin
description: Repository 薄 — 持久化转译，禁业务。Use when 写 Python 后端代码 / 评审涉及 `repository-thin`
  的 PR。
parent: ./index.md
paths:
- '**/repositories/**/*.py'
triggers:
  keywords:
  - Repository
  - Repo
  - 持久化
effort: medium
context: inline
version: '1.0'
---
# DDD · Repository 薄

## 规则

Repository 是**持久化转译层**。只做 ORM ↔ 领域对象的转换，不做业务判断。

## 方法签名

```python
class OrderRepo:
    async def find_by_id(self, oid: UUID) -> Order | None: ...
    async def find_by_owner(
        self,
        owner_id: UUID,
        *,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Order]: ...
    async def save(self, o: Order) -> Order: ...
    async def delete(self, oid: UUID) -> None: ...
    async def count_by_owner(self, owner_id: UUID) -> int: ...
```

## 必须满足

| 规则 | 说明 |
|------|------|
| 方法名是 `find_* / save / delete / count_*` | 无业务动词（如 `submit` / `approve`） |
| 参数是值类型或领域实体 | 不接受 dict 或 ORM Model |
| 返回领域实体或值 | 不返回 ORM Model 暴露给 Service |
| 不调其他 Repo | 除非父子聚合根 |
| 不抛业务异常 | 找不到返回 None |

## ORM ↔ Domain 转换

```python
class OrderRepo:
    async def find_by_id(self, oid: UUID) -> Order | None:
        row = await OrderModel.filter(id=str(oid)).first()
        if not row:
            return None
        return self._to_domain(row)

    async def save(self, o: Order) -> Order:
        # 创建 or 更新
        if o.id is None:
            row = await OrderModel.create(
                title=o.title,
                owner_id=str(o.owner_id),
                channel_id=str(o.channel_id) if o.channel_id else None,
            )
            return self._to_domain(row)
        else:
            await OrderModel.filter(id=str(o.id)).update(
                title=o.title,
                channel_id=str(o.channel_id) if o.channel_id else None,
                updated_at=datetime.now(),
            )
            row = await OrderModel.filter(id=str(o.id)).first()
            return self._to_domain(row)

    def _to_domain(self, row: OrderModel) -> Order:
        return Order(
            id=UUID(row.id),
            title=row.title,
            owner_id=UUID(row.owner_id),
            channel_id=UUID(row.channel_id) if row.channel_id else None,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
```

## 小型项目简化

后端规模较小时**不强制 Domain ↔ ORM 转换**，可以让 Repo 直接返回 ORM Model（用 `Adapter` 在 Service 出口转 Pydantic）。

实际形态：

```python
# services/article.py — 直接用 Tortoise Model 当"领域对象"
async def list_articles_by_category(category: str) -> list[Article]:
    return await Article.filter(category=category).all()
```

当领域规则复杂时再升级为真正的 Domain 层。

## 反例（无论简化版还是完整版）

```python
# ❌ Repo 内业务判断
async def find_publishable_orders(self, owner_id):
    rows = await Order.filter(owner_id=owner_id)
    return [r for r in rows if r.item_count >= 5]   # 业务规则在 Repo

# ❌ Repo 返回 dict
async def find_by_id(self, oid):
    row = await Order.filter(id=oid).first()
    return row.__dict__   # 丢类型信息

# ❌ Repo 调其他 Repo
async def find_with_owner(self, oid):
    o = await Order.filter(id=oid).first()
    owner = await self.user_repo.find_by_id(o.owner_id)   # 跨 Repo 调用
    return o, owner
```

## 自检

- [ ] 方法名只有 `find_* / save / delete / count_*`？
- [ ] 不写业务判断？
- [ ] 返回领域实体（或 ORM Model 简化版）而非 dict？
- [ ] 不调其他 Repo？
- [ ] 找不到返回 None 而非抛异常？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`controller-thin.md`](./controller-thin.md) · [`service-orchestration.md`](./service-orchestration.md) · [`domain-pure.md`](./domain-pure.md)
- 配套：[`../repository/usage-rule.md`](../repository/usage-rule.md) · [`../repository/no-business-in-repo.md`](../repository/no-business-in-repo.md)

