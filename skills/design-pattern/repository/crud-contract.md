---
name: repository-usage-rule
description: Repository 只做 CRUD — find_by / save / delete，禁业务判断。Use when 写 Python
  后端代码 / 评审涉及 `usage-rule` 的 PR。
parent: ./index.md
paths:
- '**/repositories/**/*.py'
- '**/services/**/*.py'
triggers:
  keywords:
  - Repository
  - Repo
  - DAO
  - find_by
  - 禁业务判断
effort: medium
context: inline
version: '1.0'
---
# Repository · 使用规则

## 一句话定义

Repository = **持久化层的薄壳**。只翻译"业务对象 ↔ 数据库行"，不做任何业务决策。

## 必须满足的形态

```python
# repositories/order_repo.py
class OrderRepo:
    async def find_by_id(self, oid: UUID) -> Order | None: ...
    async def find_by_owner(self, owner_id: UUID, *, limit: int = 20) -> list[Order]: ...
    async def save(self, o: Order) -> Order: ...
    async def delete(self, oid: UUID) -> None: ...
```

特征：方法名都是 `find_* / save / delete / count_*`，参数都是值类型或领域实体，返回也是领域实体或值。

## 禁止行为（命中 = 重构）

1. **禁在 Repo 写业务判断**
   ```python
   # ❌
   async def find_active_orders(self, owner_id):
       items = await Order.filter(owner_id=owner_id)
       return [o for o in items if o.item_count >= 5 and o.channel_id]  # 业务规则
   ```

2. **禁 Repo 调用 Repo**（除非父子聚合根）— 事务边界会模糊
3. **禁返回 dict / tuple** — 一律返回领域实体或值对象
4. **禁抛业务异常** — 找不到记录返回 `None`，由 Service 决定抛 `NotFoundError`

## 典型目录布局

- `<service>/repositories/` — HTTP 主后端的 Repo
- `<worker>/repositories/` — 工作进程（种子脚本 / 后台任务）的 Repo

## Service 与 Repo 的协作

```python
class OrderService:
    def __init__(self, repo: OrderRepo, channel_repo: ChannelRepo):
        self._repo = repo
        self._channel_repo = channel_repo

    async def create_for_cart(self, cart: Cart, channel_id: UUID) -> Order:
        # 1. 业务校验在 Service
        channel = await self._channel_repo.find_by_id(channel_id)
        if channel is None:
            raise ChannelNotFoundError(channel_id)   # 业务异常

        # 2. 领域对象创建
        o = Order.from_cart(cart, channel)

        # 3. 持久化交给 Repo
        return await self._repo.save(o)
```

## 自检

- [ ] Repo 方法名是 `find_* / save / delete / count_*`？
- [ ] Repo 不写 if 业务判断？
- [ ] Repo 不调用其他 Repo（除非聚合根）？
- [ ] Repo 不抛业务异常？
- [ ] Repo 返回领域实体而非 dict？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`no-business-in-repo.md`](./no-business-in-repo.md)
- 配套：[`../ddd-layering/repository-thin.md`](../ddd-layering/repository-thin.md) · [`../ddd-layering/service-orchestration.md`](../ddd-layering/service-orchestration.md)

