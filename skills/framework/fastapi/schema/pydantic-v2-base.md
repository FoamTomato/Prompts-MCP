---
name: fastapi-schema-pydantic
description: Pydantic v2 BaseModel 模板 — Field description / ge/le
parent: ./index.md
paths:
- backend/schemas/**/*.py
- py/schemas/**/*.py
triggers:
  keywords:
  - Pydantic
  - BaseModel
  - Field
  - 模板
effort: medium
context: inline
version: '1.0'
---
# FastAPI Schema · Pydantic v2

## 标准模板

```python
# backend/schemas/textbook.py
from pydantic import BaseModel, Field

class TextbookCreateReq(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="课本名称")
    subject: str = Field(..., max_length=20, description="学科")
    grade: str = Field(..., max_length=20, description="年级")
    publisher: str | None = Field(None, max_length=50, description="出版社")

class TextbookResp(BaseModel):
    id: str = Field(..., description="课本 ID（UUID）")
    name: str = Field(..., description="课本名称")
    subject: str = Field(..., description="学科")
    grade: str = Field(..., description="年级")
    publisher: str | None = Field(None, description="出版社")
    created_at: str = Field(..., description="创建时间 ISO8601")

class TextbookListResp(BaseModel):
    items: list[TextbookResp] = Field(..., description="课本列表")
    total: int = Field(..., ge=0, description="总数")
```

## 命名约定

| 类型 | 后缀 | 例 |
|------|------|------|
| 请求模型 | `*Req` | `TextbookCreateReq` |
| 响应模型 | `*Resp` | `TextbookResp` |
| 列表响应 | `*ListResp` | `TextbookListResp` |
| 嵌套子结构 | 无后缀 | `Chapter` / `SlideElement` |
| LLM 结构化输出 | `*List` 包装 | `OutlineSectionList` |

## Field 必填项

| 字段类型 | 必带 |
|---------|------|
| 任何字段 | `description` |
| 字符串 | `max_length` |
| 数值 | `ge` / `le` |
| 列表 | `min_length` / `max_length` |
| 嵌套结构 | 单独类，不内联 |

## Optional 写法

```python
# Py 3.10+
publisher: str | None = Field(None, description="出版社")

# 或者
from typing import Optional
publisher: Optional[str] = Field(None, description="出版社")
```

`None` default + `description` 必填。

## 嵌套对象

```python
class Chapter(BaseModel):
    id: str = Field(..., description="章节 ID")
    title: str = Field(..., description="章节标题")

class TextbookDetailResp(BaseModel):
    id: str = Field(..., description="课本 ID")
    chapters: list[Chapter] = Field(..., description="章节列表")
```

## LLM 结构化输出

```python
class OutlineSection(BaseModel):
    title: str = Field(..., description="幻灯片标题")
    body: str = Field(..., description="正文")

class OutlineSectionList(BaseModel):
    """用于 LLM with_structured_output — 必须用包装模型而非裸 list"""
    sections: list[OutlineSection] = Field(..., description="按顺序的章节")
```

裸 `list[X]` 在 LLM 结构化输出中不稳定，必须包装。

## 自检

- [ ] 所有字段有 `description`？
- [ ] 字符串有 `max_length`？
- [ ] 数值有 `ge` / `le`？
- [ ] Optional 显式 `= Field(None, description=...)`？
- [ ] LLM 列表输出包装成专用类？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`response-model-required.md`](./response-model-required.md)
- 配套：[`../../../lang/python/typing/pydantic-v2-field.md`](../../../lang/python/typing/pydantic-v2-field.md)

