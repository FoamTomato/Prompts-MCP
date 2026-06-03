---
name: assertion-asserts-class
description: 场景化 Asserts 类设计 — 命名约定 / 错误码绑定 / 真实示范（TextbookAsserts / OutlineAsserts）。Use
  when 评审涉及 `asserts-class` 的 PR。
parent: ./index.md
paths:
- py/asserts/**/*.py
- py/services/**/*.py
- py/routers/**/*.py
triggers:
  keywords:
  - Asserts
  - TextbookAsserts
  - OutlineAsserts
  - SessionAsserts
  - PaperAsserts
  - ReferralAsserts
  - KnowledgeAsserts
  - PresentationAsserts
  - 场景化
  - 命名约定
  - 错误码绑定
effort: medium
context: inline
version: '1.0'
---
# Asserts · 场景化包装类

## 命名约定

| 规则 | 示例 |
|------|------|
| 类名：`<Domain>Asserts`（Domain = PascalCase 业务名） | `OutlineAsserts` / `TextbookAsserts` / `SessionAsserts` |
| 文件名：`<domain>.py`（小写单数） | `outline.py` / `textbook.py` / `session.py` |
| 方法名：**业务语义**，不用 `assert_` 前缀 | ✅ `title_not_blank(title)` ❌ `assert_title_not_blank(title)` |
| 查找类断言：`found` / `<entity>_found` | `TextbookAsserts.found(textbook, tid)` |
| 状态类断言：业务动词 | `editable(outline)` / `alive(session)` |
| 关系类断言：业务动词 | `chapter_ids_belong_to(...)` |

## 文件位置

```
py/asserts/
├── __init__.py          # 集中 re-export
├── README.md            # 占用错误码总览
├── textbook.py
├── outline.py
├── session.py
├── paper.py
├── referral.py
├── knowledge.py
└── presentation.py
```

平级于 services/ / routers/ / models/，**不放 services/ 内部**——避免 grep 噪音。

## 错误码绑定规则

每个 Asserts 类**绑定一个前缀**（或两个相关前缀，如 SessionAsserts 用 A + S）。
**文件顶部 docstring 必须列出占用的码点**：

```python
"""课本业务断言（G 系列错误码）。

占用：
- G001 (404) 课本不存在
- G002 (404) 章节不存在

完整字典见 .ai/skills/core/error_code_dict.md。
"""
```

## 完整示范：TextbookAsserts

```python
# py/asserts/textbook.py
from typing import Any, Collection, Optional
from core.assertion import Asserts


class TextbookAsserts:
    """课本相关业务断言。"""

    @staticmethod
    def found(textbook: Optional[Any], textbook_id: str) -> None:
        """断言课本存在。失败时抛 G001（404）。"""
        Asserts.not_none(
            textbook,
            code="G001",
            message=f"课本不存在: {textbook_id}",
            http_status=404,
        )

    @staticmethod
    def chapter_found(chapter: Optional[Any], chapter_id: str) -> None:
        """断言章节存在。失败时抛 G002（404）。"""
        Asserts.not_none(
            chapter,
            code="G002",
            message=f"章节不存在: {chapter_id}",
            http_status=404,
        )

    @staticmethod
    def chapters_not_empty(chapters: Optional[Collection[Any]], textbook_id: str) -> None:
        """断言课本下章节非空。失败时抛 G002（404）。"""
        Asserts.not_empty(
            chapters,
            code="G002",
            message=f"课本无章节: {textbook_id}",
            http_status=404,
        )
```

## 设计原则

1. **每个方法签名包含业务语义**：调用方一眼看懂在校验什么
2. **错误消息含动态信息**：`f"课本不存在: {textbook_id}"` 比 "课本不存在" 易排查
3. **方法体只调 `Asserts.<通用方法>` 一行**：复杂校验可叠加多行 Asserts
4. **类只暴露 `@staticmethod`**：状态自由放，不要在 Asserts 类持实例字段

## 反例

```python
# ❌ 在 Asserts 类里写业务逻辑
class TextbookAsserts:
    @staticmethod
    async def found_with_chapters(tid):  # 不该有 async / 查 DB
        tb = await Textbook.get_or_none(id=tid)
        if tb is None: raise ApiException(...)
        return tb

# ✅ 让调用方查，Asserts 只做"是否"
tb = await Textbook.get_or_none(id=tid)
TextbookAsserts.found(tb, tid)

# ❌ 方法名带 assert_ 前缀
class TextbookAsserts:
    @staticmethod
    def assert_textbook_exists(...): ...  # 类名已说明是 asserts，方法名不重复

# ❌ 用 Enum 模拟（Python 没 default method）
class TextbookAssertCode(Enum):
    NOT_FOUND = "G001"
    ...  # 反而冗长
```

## 新加 Asserts 类的清单

1. 在 `.ai/skills/core/error_code_dict.md` 确认或新增前缀 + 码点
2. 新建 `py/asserts/<domain>.py`
3. 在 `py/asserts/__init__.py` re-export
4. 更新 `py/asserts/README.md` 占用表
5. 编写业务侧使用（参照模板示范）

## 自检

- [ ] 类名 `<Domain>Asserts` PascalCase？
- [ ] 文件名 `<domain>.py` 小写单数？
- [ ] 方法名是业务动词，不带 `assert_` 前缀？
- [ ] 文件顶部 docstring 列出占用码点？
- [ ] 方法只有 staticmethod，无实例字段？
- [ ] 错误消息含动态值便于排查？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`principle.md`](./principle.md) · [`validator-vs-assertion.md`](./validator-vs-assertion.md)
- 配套：[`../../lang/python/naming/index.md`](../../lang/python/naming/index.md)
- 实战代码：`py/asserts/textbook.py` / `outline.py` / `session.py` / ...
