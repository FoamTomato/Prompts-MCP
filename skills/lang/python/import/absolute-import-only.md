---
name: python-absolute-import-only
description: 禁相对导入 — 全部用绝对路径。Use when 写 Python 后端代码 / 评审涉及 `absolute-import-only`
  的 PR。
parent: ./index.md
paths:
- backend/**/*.py
- py/**/*.py
triggers:
  keywords:
  - import
  - from .
  - relative import
  - 禁相对导入
  - 全部用绝
  - 部用绝对
effort: medium
context: inline
version: '1.0'
---
# Python · 禁相对导入

## 规则

**所有 import 一律用绝对路径**。Quill 后端 `backend/` 与 `py/` 工作进程的 import 根都是项目根，因此 `from core.config import settings` 是绝对导入。

## 反例 → 正例

```python
# ❌ 相对导入（破坏可移动性）
from .config import settings
from ..models import User
from ...core.db import init_db

# ✅ 绝对导入
from core.config import settings
from models import User
from core.db import init_db
```

## 为什么

1. **重构友好**：移动一个文件不会因为相对 `..` 数量改变而集体崩
2. **IDE 索引清晰**：跳转到定义不依赖当前文件位置
3. **测试一致**：单测和主进程使用同一套路径
4. **避免循环依赖陷阱**：相对导入容易意外构造 A→.B→.A 的循环

## 例外（仅一种）

包内同目录的私有辅助模块可以用单点相对：

```python
# py/services/ppt_generator.py
from .renderers import text_renderer  # 紧密耦合的私有助手，允许
```

但**绝不允许 `..` 或更深**。

## 工具配合

`.ruff.toml` 设置：
```toml
[lint]
select = ["I"]  # isort 风格 + 检查 import 顺序
```

`pyproject.toml` 项目根：
```toml
[tool.ruff.lint.isort]
known-first-party = ["core", "models", "schemas", "adapters", "routers", "services", "agents", "tools", "middleware", "utils", "workers"]
```

## 自检

- [ ] 文件顶部没有 `from .` 或 `from ..` ？
- [ ] 同目录私有助手才用 `from .module` ？
- [ ] ruff 跑过没报 import 错误？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`import-order.md`](./import-order.md) · [`no-circular-import.md`](./no-circular-import.md)

