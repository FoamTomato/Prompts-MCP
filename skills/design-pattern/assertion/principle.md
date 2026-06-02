---
name: assertion-principle
description: 断言式异常处理三条精髓 + Asserts 引擎 12 个通用方法。Use when 写 Python 后端代码 / 评审 PR 时。
parent: ./index.md
paths:
- backend/**/*.py
- py/**/*.py
- py/asserts/**/*.py
- py/core/assertion.py
- frontend/app/lib/assertion.ts
triggers:
  keywords:
  - 断言
  - assertion
  - Asserts
  - ApiException
  - ApiError
  - ImportAsserts
effort: medium
context: inline
version: '1.0'
---
# 断言式异常处理 · 精髓

## 三条精髓

1. **断言失败 → 立即抛 ApiException**（不返回 boolean，不做 None 透传）
2. **错误码与业务场景绑定**（`OutlineAsserts.title_not_blank(title)` 抛 D003 是规约）
3. **异常向上冒泡**，只在边界（FastAPI exception_handler / 前端 ErrorBoundary）统一捕获

业务主流程读起来像直叙：4 行参数校验 + 2 行存在性校验 + 1 行业务规则 + 1 行执行。

## 通用引擎：`py/core/assertion.py`

12 个静态方法，所有 `code/message/http_status` 都是 keyword-only：

| 类别 | 方法 |
|------|------|
| 空 / 非空 | `not_none` / `not_blank` / `not_empty` |
| 数值 / 长度 | `in_range` / `max_length` / `min_length` |
| 等值 / 包含 | `equals` / `count_match` / `contains` |
| 格式 | `matches` |
| 布尔 / 状态 | `is_true` / `is_false` |

```python
from core.assertion import Asserts

Asserts.not_blank(title, code="D003", message="大纲标题不能为空", http_status=422)
Asserts.in_range(slide_count, 3, 20, code="D002", message="幻灯片数必须 3-20")
```

## 业务侧不直接调 Asserts

业务层**永远**调场景化包装 `<Domain>Asserts.<语义方法>(...)`，不直接调通用 `Asserts.<方法>`：

```python
# ❌ 业务里直接调通用引擎
Asserts.not_none(textbook, code="G001", message=f"课本不存在: {tid}", http_status=404)

# ✅ 通过场景化包装
TextbookAsserts.found(textbook, tid)
```

通用方法是"实现细节"，场景化包装是"业务接口"。这让错误码集中在 Asserts 类里，业务方不需要记忆码点。

## 改造前后对照

```python
# 改前：散落 8 处 if + raise
if not req.title.strip():
    raise HTTPException(400, "标题不能为空")
if len(req.title) > 200:
    raise HTTPException(422, "标题超长")
textbook = await Textbook.get_or_none(id=req.textbook_id)
if textbook is None:
    raise HTTPException(404, "课本不存在")
chapters = await Chapter.filter(textbook_id=req.textbook_id).all()
if not chapters:
    raise HTTPException(404, "课本没有章节")

# 改后：5 行线性直叙
OutlineAsserts.title_not_blank(req.title)
OutlineAsserts.title_within_limit(req.title)
textbook = await Textbook.get_or_none(id=req.textbook_id)
TextbookAsserts.found(textbook, req.textbook_id)
chapters = await Chapter.filter(textbook_id=req.textbook_id).all()
TextbookAsserts.chapters_not_empty(chapters, req.textbook_id)
```

## 前端等价

```typescript
import { ApiError, Asserts } from "@/app/lib/assertion";

Asserts.notBlank(form.title, { code: "D003", message: "大纲标题不能为空" });
Asserts.inRange(form.slideCount, 3, 20, { code: "D002", message: "幻灯片数 3-20" });
```

利用 TS `asserts value is T` 谓词：断言后类型自动收窄，调用方不需要再 `!` 强断言。

## 自检

- [ ] 断言失败抛 ApiException（不是 bool / None）？
- [ ] 业务层调 `<Domain>Asserts.<方法>` 而非通用 `Asserts.<方法>`？
- [ ] 边界（exception_handler）统一捕获，而非到处 try/except？
- [ ] code 是字符串（A001 / G002）不是 int？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`asserts-class.md`](./asserts-class.md) · [`validator-vs-assertion.md`](./validator-vs-assertion.md) · [`side-effect-cleanup.md`](./side-effect-cleanup.md)
- 配套：[`../../lang/python/error-handling/api-exception.md`](../../lang/python/error-handling/api-exception.md)
