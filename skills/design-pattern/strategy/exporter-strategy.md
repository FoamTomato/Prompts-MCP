---
name: strategy-exporter
description: 导出器策略 — DocxExporter / PdfExporter 可替换。Use when 写 Python 后端代码 / 评审涉及
  `exporter-strategy` 的 PR。
parent: ./index.md
paths:
- '**/services/exporters/**/*.py'
- '**/exporters/**/*.py'
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

## 典型用例

| 场景 | 策略组 | 实现 |
|------|-------|------|
| 报表导出 | OrderExporter | DocxExporter / PdfSummaryExporter / PdfDetailExporter |
| 文档渲染 | DocumentRenderer | HtmlRenderer / MarkdownRenderer |

## 订单导出器示例

```python
# exporters/order_exporter.py
from abc import ABC, abstractmethod
from io import BytesIO

class OrderExporter(ABC):
    @abstractmethod
    async def export(self, order: Order) -> bytes:
        """返回文件字节流"""

class DocxExporter(OrderExporter):
    async def export(self, order: Order) -> bytes:
        from docx import Document
        doc = Document()
        doc.add_heading(order.title, 0)
        for item in order.items:
            doc.add_paragraph(item.name)
            for attr in item.attrs:
                doc.add_paragraph(f"  {attr}")
        out = BytesIO()
        doc.save(out)
        return out.getvalue()

class PdfSummaryExporter(OrderExporter):
    """概要视图"""
    async def export(self, order: Order) -> bytes:
        return await _render_pdf(order, with_detail=False)

class PdfDetailExporter(OrderExporter):
    """完整明细"""
    async def export(self, order: Order) -> bytes:
        return await _render_pdf(order, with_detail=True)


EXPORTERS: dict[str, type[OrderExporter]] = {
    "docx":        DocxExporter,
    "pdf_summary": PdfSummaryExporter,
    "pdf_detail":  PdfDetailExporter,
}

def get_exporter(format: str) -> OrderExporter:
    if format not in EXPORTERS:
        raise ApiException(msg=f"不支持的格式: {format}", code=400)
    return EXPORTERS[format]()
```

## Service 编排

```python
class OrderService:
    async def export(self, order_id: str, format: str) -> bytes:
        order = await self.repo.find_by_id_or_raise(order_id)
        exporter = get_exporter(format)
        return await exporter.export(order)
```

## 反例

```python
# ❌ Service 内 if/else 选格式
async def export(order_id, format):
    order = await ...
    if format == "docx":
        # 50 行 docx 生成代码
    elif format == "pdf_summary":
        # 50 行 pdf 生成代码
    elif format == "pdf_detail":
        # 50 行
    # 加新格式要改这里 + 风险所有 if/else 分支

# ✅ 用策略
exporter = get_exporter(format)
return await exporter.export(order)
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

