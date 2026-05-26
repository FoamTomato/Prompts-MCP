---
name: python-import-order
description: import 三段顺序 — stdlib → third-party → local。Use when 写 Python 后端代码 / 评审涉及
  `import-order` 的 PR。
parent: ./index.md
paths:
- backend/**/*.py
- py/**/*.py
triggers:
  keywords:
  - import
  - isort
  - ruff
  - 三段顺序
effort: medium
context: inline
version: '1.0'
---
# Python · import 顺序

## 规则

import 必须分三段，每段内按字母升序，段间空一行：

```python
# 1. 标准库
import asyncio
import json
from pathlib import Path
from typing import AsyncGenerator

# 2. 第三方
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from tortoise import fields

# 3. 项目内（known-first-party）
from core.config import settings
from core.db import init_db
from models.session import Session
from schemas.session import SessionResponse
```

## 通过工具自动维护

`.ruff.toml`：
```toml
[lint.isort]
known-first-party = ["core", "models", "schemas", "adapters", "routers", "services", "agents", "tools", "middleware", "utils", "workers"]
section-order = ["future", "standard-library", "third-party", "first-party", "local-folder"]
combine-as-imports = true
```

CI / pre-commit：
```bash
ruff check --select I --fix
```

## 反例

```python
# ❌ 顺序乱
from fastapi import FastAPI
import json
from core.config import settings
import asyncio
from pydantic import BaseModel

# ❌ 多重导入散开
from typing import Optional
from typing import List   # → 合并为 from typing import List, Optional
```

## 关于 from x import * 

**全局禁用**。namespace 污染、IDE 无法 narrow、IDE/类型检查器追溯困难。

## 自检

- [ ] 三段式（stdlib / third / local）？
- [ ] 段内字母序？
- [ ] 段间空一行？
- [ ] 无 `from x import *`？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`absolute-import-only.md`](./absolute-import-only.md)

