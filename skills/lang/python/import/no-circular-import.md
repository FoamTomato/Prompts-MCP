---
name: python-no-circular-import
description: Python Service 层禁循环依赖 — 不互相 import，必要时下移共享逻辑到 helper。Use when 写 Python
  后端代码 / 评审涉及 `no-circular-import` 的 PR。
parent: ./index.md
paths:
- backend/services/**/*.py
- py/services/**/*.py
triggers:
  keywords:
  - 循环依赖
  - circular import
  - import order
  - 模块依赖
effort: medium
context: inline
version: '1.0'
---
# Python · 禁循环依赖

## 规则

任何两个 Service / Adapter / Agent 之间**不能互相 import**。Repository / Model 也不允许向上调 Service。

合法依赖方向（仅向下）：

```
Router → Service → Adapter → Schema/Model
            ↓
           Agent → Tools
            ↓
           Core (config / db / redis / logger / exceptions)
```

## 反例

```python
# services/session_manager.py
from services.credits_service import deduct_credits

# services/credits_service.py
from services.session_manager import get_current_session   # ← 循环！
```

报错形式：`ImportError: cannot import name 'X' from partially initialized module 'Y'`

## 拆解模式

### 模式 1：抽出共享下层

把两个 Service 都需要的逻辑下沉到 `core/` 或新增 `services/_shared/`：

```python
# services/_shared/auth_session.py
async def get_active_session(session_id: str) -> Session: ...

# services/session_manager.py
from services._shared.auth_session import get_active_session

# services/credits_service.py
from services._shared.auth_session import get_active_session
```

### 模式 2：依赖注入

被调用的 Service 作为参数传入，而不是 import：

```python
# services/credits_service.py
async def deduct(uid: int, amount: int, session_loader):
    sess = await session_loader(uid)
    ...

# services/session_manager.py
from services.credits_service import deduct
await deduct(uid, 1, session_loader=load_session_internal)
```

### 模式 3：事件 / 信号

完全解耦：发事件，让另一边订阅。Quill 内当前没实现事件总线，规模未到。

## 工具

```bash
# 用 pydeps 找循环
uv run pydeps backend --max-bacon 0 --reverse > /tmp/deps.svg
```

或用 ruff 的 `flake8-import-cycle` 规则（如启用）。

## 自检

- [ ] 两个 Service 不互相 import？
- [ ] Repo / Model 不 import Service？
- [ ] 共享下层放 `core/` 或 `services/_shared/`？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`../../../design-pattern/ddd-layering/service-orchestration.md`](../../../design-pattern/ddd-layering/service-orchestration.md)

