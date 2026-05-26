---
name: code-naming-as-doc
description: '习惯 · code-quality: 命名即文档 — 函数/变量/类名直接表达意图，少注释'
parent: ./index.md
paths:
- backend/**/*.py
- py/**/*.py
- frontend/src/**/*.ts
- frontend/src/**/*.tsx
triggers:
  keywords:
  - 命名
  - naming
  - 可读性
effort: medium
context: inline
version: '1.0'
---
# Code Quality · 命名即文档

## 核心思想

**函数 / 变量 / 类名要直接表达意图**，让阅读代码 = 阅读文档。少注释。

## 反例 → 正例

```python
# ❌ 注释解释烂命名
def proc(d, t):
    # 处理订单，t 是 type
    if t == 1:
        ...

# ✅ 命名表达
def process_order(order_data: OrderDto, order_type: OrderType):
    if order_type == OrderType.URGENT:
        ...

# ❌
async def get(id):     # get 什么？
    return await User.filter(id=id).first()

# ✅
async def get_user_by_id(uid: int) -> User | None:
    return await User.filter(id=uid).first()
```

## 命名层次

| 范围 | 长度 |
|------|------|
| 局部循环变量 | 1-3 字（`i` / `idx` / `row`） |
| 函数内局部变量 | 2-5 字（`user` / `order_list`） |
| 函数参数 | 完整名（`user_id` / `order_dto`） |
| 公开函数 | 完整动词 + 名词（`fetch_user_by_id`） |
| 类 | 完整名词（`UserService`） |
| 模块 | 简单名词（`user.py`） |

## 抛异常的暗示

```python
# ✅ _or_raise 后缀
def get_user_or_raise(uid: int) -> User: ...

# ✅ 返回 None
async def find_user(uid: int) -> User | None: ...
```

## 布尔变量带前缀

```python
# ✅
is_active = True
has_quota = check_quota(user)
should_retry = error.is_transient()
can_edit = user.has_permission("edit")

# ❌
active = True
quota = True
retry = True
edit = True   # 是动作还是状态？
```

## 缩写约定

| 允许的缩写 | 含义 |
|----------|------|
| `id` / `uid` / `pid` | identifier |
| `tx` / `ctx` | transaction / context |
| `req` / `resp` | request / response |
| `cfg` / `conf` | config |
| `e` / `err` | error / exception |
| `i` / `j` / `k` | 循环索引 |

**不要**自创缩写：

```python
# ❌
hdl  → handler
proc → processor
mgr  → manager
```

## 单字母变量

只允许：

- `i` / `j` / `k` 循环索引
- `e` / `err` 异常 catch
- 数学公式中的 `x` / `y` / `z`

其他场景：用完整命名。

## 反例

```python
# ❌ 拼音
def huoqu_user(uid): ...

# ❌ 中文
def 获取用户(uid): ...

# ❌ 缩写
def proc(d): ...

# ❌ 单字母（业务变量）
for x in users: ...
```

## 与注释的边界

| 写 | 不写 |
|----|------|
| 业务上下文（"为什么扣 bonus 优先"） | 解释命名（已自解释） |
| 引用规范 / Issue（"按 X 实现"） | 重复代码语义 |
| 临时 TODO / HACK | 永久状态注释 |

```python
# ❌ 重复
# 计算总价
total = sum(items)

# ✅ 业务上下文
# 价格规则：bonus 优先扣减，超出部分扣 base（按 referral PRD R5）
remaining = cost - min(credits.bonus, cost)
```

## 自检

- [ ] 函数 / 变量 / 类名一眼能看懂意图？
- [ ] 抛异常的函数加 `_or_raise` 后缀？
- [ ] 布尔变量带 `is_/has_/should_/can_`？
- [ ] 没拼音 / 中文标识符？
- [ ] 没缩写（除允许列表）？
- [ ] 注释不重复代码语义？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`no-magic-values.md`](./no-magic-values.md)
- 配套：[`../../lang/python/naming/function-naming.md`](../../lang/python/naming/function-naming.md) · [`../../lang/python/naming/variable-naming.md`](../../lang/python/naming/variable-naming.md)

