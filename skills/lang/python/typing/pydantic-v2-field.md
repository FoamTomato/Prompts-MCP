---
name: python-pydantic-v2-field
description: Pydantic Field 必带 description + 约束（ge/le/max_length）。Use when 写 Python
  后端代码 / 评审涉及 `pydantic-v2-field` 的 PR。
parent: ./index.md
paths:
- backend/schemas/**/*.py
- py/schemas/**/*.py
triggers:
  keywords:
  - Pydantic
  - Field
  - BaseModel
  - schema
  - 约束
effort: medium
context: inline
version: '1.0'
---
# Python · Pydantic v2 Field

## 规则

每个 BaseModel 的字段**必须用 Field 显式声明**，且必带 `description`。数值字段必带 `ge` / `le`，字符串字段必带 `max_length`。

## 请求模型模板

```python
from pydantic import BaseModel, Field

class PresentationCreateReq(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="课件标题")
    textbook_id: str = Field(..., description="关联课本 ID（UUID）")
    chapter_ids: list[str] = Field(
        ..., min_length=1, max_length=20, description="章节 ID 列表"
    )
    slide_count: int = Field(
        10, ge=5, le=30, description="目标幻灯片数量"
    )
    theme_id: str | None = Field(None, description="主题 ID，留空使用默认")
```

## 响应模型模板

```python
class PresentationResponse(BaseModel):
    id: str = Field(..., description="课件 ID")
    title: str = Field(..., description="课件标题")
    slide_count: int = Field(..., description="实际幻灯片数量")
    created_at: str = Field(..., description="创建时间 ISO8601")
```

## 嵌套 / 结构化输出

```python
class SlideContent(BaseModel):
    title: str = Field(..., description="幻灯片标题")
    body: str = Field(..., description="幻灯片正文")
    image_query: str | None = Field(None, description="建议的图片搜索关键词")

class SlideList(BaseModel):
    """用于 LLM with_structured_output"""
    slides: list[SlideContent] = Field(..., description="幻灯片列表，按顺序")
```

LLM 输出包装成专门的 List 模型，**不要直接让 LLM 返回 list**——结构化输出对单层对象更稳定。

## 反例

```python
# ❌ 缺 description
class Req(BaseModel):
    title: str
    pages: int

# ❌ 字符串无 max_length（潜在 DoS）
class Req(BaseModel):
    title: str = Field(..., description="...")

# ❌ 数值无范围约束
slide_count: int = Field(..., description="...")  # 用户传 99999 怎么办？
```

## 校验顺序

Pydantic 在 endpoint 解析时自动校验。Service 不需要再校验已经被 Pydantic 校验过的字段。**Service 只做业务规则校验**（如 "用户有权操作这个课件吗"）。

## 自检

- [ ] 每个字段有 `description`？
- [ ] 字符串有 `max_length`？
- [ ] 数值有 `ge` / `le`？
- [ ] List 类型的输出用包装模型？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`../../../framework/fastapi/schema/pydantic-v2-base.md`](../../../framework/fastapi/schema/pydantic-v2-base.md)

