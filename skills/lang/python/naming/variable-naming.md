---
name: python-variable-naming
description: Python 变量命名 — snake_case + 名词性 + 布尔前缀
parent: ./index.md
paths:
  - "backend/**/*.py"
  - "py/**/*.py"
triggers:
  keywords: [变量命名, 布尔变量, snake_case]
effort: low
context: inline
version: "1.0"
---

# Python · 变量命名

## 规则

| 规则 | 示例 |
|------|------|
| snake_case 名词性 | `user_id` / `brand_list` / `outline_text` |
| 布尔变量加前缀 | `is_active` / `has_quota` / `should_retry` / `can_edit` |
| 集合复数 | `users`（list） / `user_map`（dict） / `user_set`（set） |
| 常量 UPPER_SNAKE | `MAX_RETRY_COUNT` / `DEFAULT_TTL_SEC` |
| 临时变量上下文化 | 循环用 `for user in users` 而非 `for u in users` |

## 反例

```python
# ❌ 布尔无前缀（看着像状态枚举）
active = True  # → is_active

# ❌ 单字母
for u in users: ...   # 短循环还能忍；超过 3 行就改 user

# ❌ 拼音 / 中文
yonghu_id = ...
用户列表 = ...

# ❌ 缩写
usr / pwd / cfg   # → user / password / config（仅 id / uid 等公认缩写可保留）

# ❌ 魔法值散落
if status == 1:   # 1 是什么意思？→ if status == SessionStatus.ACTIVE
```

## 与领域对象的关系

```python
# Service 函数里的局部变量优先用领域语义
async def service_create_presentation(req, user_id):
    brand = await get_brand_or_raise(req.brand_id)        # 不是 b / data
    chapter_list = await Chapter.filter(...)              # 不是 result / items
    outline_text = await build_outline(brand, chapter_list)
    return outline_text
```

## 自检

- [ ] 变量名是名词性，函数名是动词性？
- [ ] 布尔变量带 `is_/has_/should_/can_` 前缀？
- [ ] 没有 1/0/-1 等魔法值？常量已抽到 const 模块？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`function-naming.md`](./function-naming.md)
- 配套：[`../../../habit/code-quality/no-magic-values.md`](../../../habit/code-quality/no-magic-values.md)
