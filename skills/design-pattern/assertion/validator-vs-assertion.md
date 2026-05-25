---
name: assertion-validator-vs-assertion
description: Pydantic Schema validator 与 Asserts 各自的边界 + 5 个不该用断言的反例
parent: ./index.md
paths:
  - "backend/**/*.py"
  - "py/**/*.py"
  - "py/schemas/**/*.py"
  - "py/asserts/**/*.py"
triggers:
  keywords: [validator, Asserts, Pydantic, Field, Schema, 校验, 断言, 反例]
effort: medium
context: inline
version: "1.0"
---

# Asserts vs Pydantic · 边界与反例

## 分工总则

| 校验类型 | 由谁负责 |
|--------|--------|
| 单字段类型 / 长度 / 范围 / 正则 | **Pydantic** `Field(max_length=, ge=, le=, pattern=)` |
| 必填字段（field=...） | **Pydantic**（不要 Asserts 重复） |
| 枚举值合法性（如 status in {...}） | **Pydantic** `Literal[...]` 或 `Enum` |
| 跨字段（如 password_confirm == password） | **Pydantic** `@field_validator` / `@model_validator` |
| **跨实体存在性**（如 textbook_id 对应的课本是否存在） | **Asserts** |
| **业务状态机**（如 outline 是否可编辑） | **Asserts** |
| **业务规则**（如积分够不够 / 是否自邀） | **Asserts** |
| 动态结构（dict[str, Any] 校验） | **Asserts** |

## 简单口诀

> **Pydantic 校验"输入本身合法"，Asserts 校验"输入对应的业务状态合法"**。

## 不该用断言的 5 个反例

### 反例 1：性能敏感的循环内

```python
# ❌ 在 10 万行 CSV 循环里每行调 Asserts
for row in rows:
    Asserts.matches(row.email, EMAIL_PATTERN, code="V001", message="...")

# ✅ 批量校验：失败的收集起来一次抛
invalid_rows = [r for r in rows if not EMAIL_PATTERN.fullmatch(r.email)]
ImportAsserts.no_invalid_emails(invalid_rows)
```

每行调 Asserts 开销大（抛异常的成本）。改批量收集。

### 反例 2：第三方库异常透传

```python
# ❌ 把 Qdrant / OpenAI / Tortoise 内部 exception 包装为 ApiException
try:
    await qdrant.search(...)
except QdrantException as e:
    raise ApiException("X009", str(e))  # 把底层错误字面量送到 UI

# ✅ 让底层异常向上传播，由 global handler 兜底 X009
```

`global_error_handler` 已经会兜底为 X009，业务层重复包装反而把底层细节泄漏给前端。

### 反例 3：I/O 错误 / 网络错误

```python
# ❌ 把 ConnectionError 当业务异常处理
try:
    response = await httpx.get(url)
except ConnectionError as e:
    raise ApiException("E001", "网络异常")

# ✅ 让其向上传播
response = await httpx.get(url)  # 失败由 global handler 处理
```

`ConnectionError` / `TimeoutError` / `asyncio.CancelledError` 属于运行时不可控错误，统一记 500。

### 反例 4：可恢复降级路径

```python
# ❌ 用断言把"找不到 → 走默认值"的路径阻断
font = await Font.get_or_none(id=font_id)
SettingsAsserts.font_exists(font)  # 找不到就抛 D001
return font

# ✅ 直接降级
font = await Font.get_or_none(id=font_id)
return font or DEFAULT_FONT
```

如果业务有"找不到也能继续"的语义，**别加断言**。

### 反例 5：Pydantic 已校验的字段

```python
class OutlineCreateReq(BaseModel):
    title: str = Field(..., max_length=200)        # 已校验长度
    slide_count: int = Field(..., ge=3, le=20)     # 已校验范围

async def generate(req: OutlineCreateReq):
    # ❌ 重复校验
    OutlineAsserts.title_within_limit(req.title)
    OutlineAsserts.slides_min_count([1] * req.slide_count)

    # ✅ Asserts 只做 Pydantic 表达不了的跨字段 / 跨实体规则
    OutlineAsserts.chapter_ids_belong_to(req.chapter_ids, chapters)
```

### 反例 6（W3.5 sweep 经验）：内部不变量

```python
# ❌ 把"客户端不该传脏数据"当业务异常
def _render_element(slide, element, theme_config):
    el_type = element.get("type")
    handler = handlers.get(el_type)
    if not handler:
        # 内部不变量违反（schema 应该提前过滤）
        raise ApiException("B008", f"未支持元素类型: {el_type}")  # 不要

# ✅ 让 ValueError 抛上去，由 global_error_handler 兜底 X009 + 加注释
if handler:
    handler(slide, element, theme_config)
else:
    # 不变量违反（schema 应该提前过滤）：让 global handler 兜底 X009
    # 不抛 ApiException 是因为这是内部 bug 信号，不该把字面量送 UI
    raise ValueError(f"Unsupported element type: {el_type}")
```

内部不变量 = "本不该发生的"。把它送 UI 等于把脏数据信号当业务错误，模糊问题归属。让 X009 兜底，开发期通过日志排查。

## 自检

- [ ] 单字段校验用 Pydantic 不用 Asserts？
- [ ] 跨实体 / 业务状态机用 Asserts 不用 Pydantic？
- [ ] 性能敏感循环改批量校验？
- [ ] 第三方库异常 / I/O 错误让其向上传播？
- [ ] 可恢复降级用 `or DEFAULT` 而非断言？
- [ ] 内部不变量保留 raise ValueError + 注释说明？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`principle.md`](./principle.md) · [`asserts-class.md`](./asserts-class.md)
- 配套：[`../../framework/fastapi/schema/pydantic-v2-base.md`](../../framework/fastapi/schema/pydantic-v2-base.md)
