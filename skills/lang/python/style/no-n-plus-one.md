---
name: python-no-n-plus-one
description: ORM 查询禁 N+1 — 循环内单条查询必须改批量。Use when 写 Python 后端代码 / 评审涉及 `no-n-plus-one`
  的 PR。
parent: ./index.md
paths:
- backend/**/*.py
- py/**/*.py
triggers:
  keywords:
  - N+1
  - ORM
  - filter
  - in_bulk
  - 循环查询
effort: medium
context: inline
version: '1.0'
---
# Python · 禁 N+1 查询

## 规则

**禁止循环内单条 ORM 查询**。改成批量查询 + 字典映射。

## 反例

```python
# ❌ N+1：N 次数据库往返
order_ids = [1, 2, 3, ..., 100]
results = []
for oid in order_ids:
    order = await Order.filter(id=oid).first()
    results.append(order)
```

## 正例

```python
# ✅ 1 次批量查询 + dict 映射
order_ids = [1, 2, 3, ..., 100]
orders = await Order.filter(id__in=order_ids).all()
order_map = {o.id: o for o in orders}

results = [order_map.get(oid) for oid in order_ids]
```

## 关联表的 N+1

```python
# ❌ 循环里取关联
presentations = await Presentation.all()
for p in presentations:
    p.theme = await Theme.filter(id=p.theme_id).first()  # N+1
```

```python
# ✅ prefetch_related
presentations = await Presentation.all().prefetch_related("theme")
for p in presentations:
    print(p.theme.name)   # 已经预加载
```

或用 `select_related`（一对一关系）：

```python
slides = await Slide.all().select_related("presentation")
```

## 统计场景

```python
# ❌ 循环计数
total = 0
for uid in user_ids:
    total += await Order.filter(user_id=uid).count()

# ✅ GROUP BY 一次出
from tortoise.functions import Count
counts = await Order.filter(user_id__in=user_ids) \
    .group_by("user_id") \
    .annotate(c=Count("id")) \
    .values("user_id", "c")
count_map = {row["user_id"]: row["c"] for row in counts}
```

## 检测方法

开发环境开启 Tortoise SQL 日志：

```python
# core/db.py
logging.getLogger("tortoise").setLevel(logging.DEBUG)
```

观察一次请求触发了几次 SELECT。10+ 次基本就是 N+1。

## 自检

- [ ] 循环内没有 `.filter(...).first()` / `.get(...)` ？
- [ ] 用 `id__in=...` 批量查替代循环单查？
- [ ] 关联字段用 `prefetch_related` / `select_related` ？
- [ ] 统计用 `group_by + annotate` 而非循环计数？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`../../../framework/tortoise/model-class-pattern.md`](../../../framework/tortoise/model-class-pattern.md)

