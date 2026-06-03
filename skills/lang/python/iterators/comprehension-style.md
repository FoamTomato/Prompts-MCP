---
name: py-comprehension-style
description: 列表/字典/集合推导式写法、海象 := 复用，以及推导式与生成器表达式的内存权衡。Use when 写推导式 / 选列表推导还是生成器 / 用海象避免重复计算。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 推导式
  - 海象运算符
  - comprehension
  - walrus
  - 生成器表达式
effort: medium
context: inline
version: '1.0'
---
# Python · 推导式风格

## 规则

| 你想 | 写法 |
|------|------|
| 由可迭代构造 list | `[f(x) for x in it if cond(x)]` |
| 构造 dict | `{k: v for k, v in pairs}` |
| 构造 set / 去重 | `{f(x) for x in it}` |
| 只遍历一次/喂给聚合 | `(f(x) for x in it)` 生成器表达式 |
| 推导内复用一次计算的结果 | 海象 `:=`：`[y for x in it if (y := f(x)) > 0]` |

选型：结果要**多次用/索引/取 len** → 列表推导；只**遍历一次**（`sum`/`any`/`max`/直接传函数）或**结果集很大** → 生成器表达式，省内存。推导式只在逻辑简单时用——嵌套超过两层或带复杂分支，改写普通 `for` 更可读。

## 正例

```python
# 列表推导：过滤 + 映射
active_ids = [u.id for u in users if u.is_active]

# 字典推导：反转映射
id_to_name = {u.id: u.name for u in users}

# 集合推导：去重
domains = {email.split("@")[1] for email in emails}

# 生成器表达式喂聚合：不建中间 list
total = sum(o.amount for o in orders if o.paid)

# 海象 := 复用计算结果，避免调用两次 expensive(x)
results = [y for x in data if (y := expensive(x)) is not None]
```

## 反例

```python
# ❌ 推导式塞副作用（print/append/调接口），只为循环而推导
[print(x) for x in items]          # 建了个没人用的 list，纯浪费
# ✅ 有副作用就老实写 for
for x in items:
    print(x)

# ❌ 三层嵌套 + 多条件，没人读得懂
[f(x, y, z) for x in xs for y in ys if p(y) for z in zs if q(x, z)]
# ✅ 拆成普通 for + 生成器函数

# ❌ 大结果集用列表推导，峰值内存翻倍
data = [transform(row) for row in fetch_millions()]
total = sum(d.size for d in data)
# ✅ 一次性消费就用生成器表达式
total = sum(transform(row).size for row in fetch_millions())
```

理由：推导式的价值是「表达式构造容器」，塞副作用违背其语义且白建容器；嵌套过深时可读性比简洁更重要；只消费一次的大数据用生成器表达式避免物化。

## 自检

- [ ] 推导式里没有 `print` / `append` / 接口调用等副作用？
- [ ] 嵌套 ≤2 层、条件简单；复杂逻辑改回普通 `for`？
- [ ] 只遍历一次或结果很大时用 `(...)` 生成器表达式而非 `[...]`？
- [ ] 需要复用一次计算结果时用海象 `:=`，没有重复调用同一函数？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`generator-lazy.md`](./generator-lazy.md) · [`iterator-protocol.md`](./iterator-protocol.md) · [`yield-from-delegation.md`](./yield-from-delegation.md)
