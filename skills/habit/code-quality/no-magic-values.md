---
name: code-no-magic-values
description: 无魔法值 — 1/0/-1 / 状态枚举 / 配置项全用常量
parent: ./index.md
paths:
  - "backend/**/*.py"
  - "py/**/*.py"
  - "frontend/src/**/*.ts"
  - "frontend/src/**/*.tsx"
triggers:
  keywords: [魔法值, magic number, 常量, Enum]
effort: medium
context: inline
version: "1.0"
---

# Code Quality · 无魔法值

## 规则

代码中**禁止散落数字 / 字符串字面量**。一律抽常量或枚举。

## 反例

```python
# ❌ 散落数字
if user.role == 1:   # 1 是什么？
    ...
if status == 3:      # 3 是什么？
    ...
time.sleep(60 * 60 * 24)   # 一天？为什么 sleep？

# ❌ 散落字符串
if order["status"] == "pending":   # 拼写错误难检测
    ...
```

## 正例

```python
# ✅ 常量
from enum import IntEnum, StrEnum

class UserRole(IntEnum):
    NORMAL = 1
    ADMIN = 2
    SUPER_ADMIN = 3

class OrderStatus(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"

# 使用
if user.role == UserRole.ADMIN:
    ...
if order.status == OrderStatus.PENDING:
    ...

# 时长用语义化常量
ONE_DAY_SEC = 24 * 60 * 60
time.sleep(ONE_DAY_SEC)
```

## 配置常量分类

| 类型 | 放哪里 |
|------|------|
| 业务枚举（Status / Role / Type） | `core/constants.py` 或对应 model 文件 |
| 时长（TTL / Timeout） | `core/config.py`（可从环境变量读） |
| 文案 | i18n 字典（前端） / 业务模块内（后端 ApiException 的 msg） |
| 物理常量（最大文件大小 / 重试次数） | `core/constants.py` |

## TypeScript 同理

```ts
// ❌
if (status === 1) { ... }

// ✅
const enum UserRole {
  Normal = 1,
  Admin = 2,
}
if (role === UserRole.Admin) { ... }

// 或 as const
const ORDER_STATUS = {
  Pending: "pending",
  Paid: "paid",
} as const;
type OrderStatus = (typeof ORDER_STATUS)[keyof typeof ORDER_STATUS];
```

## 唯一例外

| 例外 | 为什么 |
|------|------|
| 0 / 1（计数 / index） | 含义明显 |
| 空字符串 / null（特定语义） | 含义明显 |
| 单测里的样本数据 | 测试上下文足够清晰 |
| 数学 / 几何常量（如 PI / 1.618） | 含义已知 |

## 检测

| 工具 | 命中规则 |
|------|--------|
| Ruff `PLR2004` | 魔法数字 |
| ESLint `@typescript-eslint/no-magic-numbers` | 同上 |

## 自检

- [ ] 业务枚举值用 IntEnum / StrEnum？
- [ ] TTL / 超时用命名常量？
- [ ] 没散落 `if x == 3` 这种？
- [ ] 字符串字面量也抽（特别是 status / type 这种）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`naming-as-doc.md`](./naming-as-doc.md)
- 配套：[`../../lang/python/naming/variable-naming.md`](../../lang/python/naming/variable-naming.md)

