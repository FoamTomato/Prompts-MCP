---
name: strategy-exporter
description: 导出器策略 — DocxExporter / PdfExporter 可替换
parent: ./index.md
paths:
- backend/services/exporters/**/*.py
- py/services/exporters/**/*.py
- py/paper/**/*.py
- py/ppt/**/*.py
triggers:
  keywords:
  - Exporter
  - strategy
  - docx
  - pdf
  - 导出器策略
  - 可替换
effort: medium
context: inline
version: '1.0'
---
# Strategy · 导出器策略

## 何时用 Strategy

多种"做同一件事"的方式，运行时选一种执行。

## Quill 用例

| 模块 | 策略组 | 实现 |
|------|-------|------|
| ppt_generator M6 | PPT 渲染 | PythonPptxRenderer / SvgRenderer |
| paper_editor PE10 | 试卷导出 | DocxExporter / PdfPreviewExporter / PdfAnswerExporter |

## paper_editor 导出器示例

```python
# py/paper/exporter.py
from abc import ABC, abstractmethod
from io import BytesIO

class PaperExporter(ABC):
    @abstractmethod
    async def export(self, paper: Paper) -> bytes:
        """返回文件字节流"""

class DocxExporter(PaperExporter):
    async def export(self, paper: Paper) -> bytes:
        from docx import Document
        doc = Document()
        doc.add_heading(paper.title, 0)
        for q in paper.questions:
            doc.add_paragraph(q.stem)
            for opt in q.options:
                doc.add_paragraph(f"  {opt}")
        out = BytesIO()
        doc.save(out)
        return out.getvalue()

class PdfPreviewExporter(PaperExporter):
    """题目无答案"""
    async def export(self, paper: Paper) -> bytes:
        return await _render_pdf(paper, with_answer=False)

class PdfAnswerExporter(PaperExporter):
    """题目 + 答案"""
    async def export(self, paper: Paper) -> bytes:
        return await _render_pdf(paper, with_answer=True)


EXPORTERS: dict[str, type[PaperExporter]] = {
    "docx":        DocxExporter,
    "pdf_preview": PdfPreviewExporter,
    "pdf_answer":  PdfAnswerExporter,
}

def get_exporter(format: str) -> PaperExporter:
    if format not in EXPORTERS:
        raise ApiException(msg=f"不支持的格式: {format}", code=400)
    return EXPORTERS[format]()
```

## Service 编排

```python
class PaperService:
    async def export(self, paper_id: str, format: str) -> bytes:
        paper = await self.repo.find_by_id_or_raise(paper_id)
        exporter = get_exporter(format)
        return await exporter.export(paper)
```

## 反例

```python
# ❌ Service 内 if/else 选格式
async def export(paper_id, format):
    paper = await ...
    if format == "docx":
        # 50 行 docx 生成代码
    elif format == "pdf_preview":
        # 50 行 pdf 生成代码
    elif format == "pdf_answer":
        # 50 行
    # 加新格式要改这里 + 风险所有 if/else 分支

# ✅ 用策略
exporter = get_exporter(format)
return await exporter.export(paper)
```

## Strategy vs Factory 区别

| Strategy | Factory |
|----------|---------|
| 选哪个**算法**做事 | 选哪个**对象**创建 |
| 行为多态 | 创建多态 |
| `exporter.export(paper)` | `get_provider().__init__(...)` |

实际中两者经常一起用：Factory 创建 Strategy 实例。

## 自检

- [ ] 多个"做同一件事"的方式都继承公共抽象？
- [ ] 选择逻辑集中在工厂函数？
- [ ] 调用方只用接口不知具体类？
- [ ] 加新策略不改老代码（OCP）？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`../factory/llm-provider-factory.md`](../factory/llm-provider-factory.md)

