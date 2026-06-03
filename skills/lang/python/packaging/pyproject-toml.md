---
name: py-pyproject-toml
description: pyproject.toml 写法 — PEP 621 [project] 元数据、dependencies、optional-dependencies、构建后端 [build-system]。Use when 配置项目元数据 / 声明依赖 / 加可选 extra / 选构建后端。
parent: ./index.md
paths:
- pyproject.toml
- '*.toml'
- 'py/**/*.py'
triggers:
  keywords:
  - 项目元数据
  - pyproject
  - PEP 621
  - optional-dependencies
  - build-system
  - 构建后端
effort: medium
context: inline
version: '1.0'
---
# Python · pyproject.toml 元数据

## 规则

`pyproject.toml` 是项目**唯一**配置入口（PEP 621 标准）。不要再用 `setup.py` / `setup.cfg` 声明元数据。

| 段 | 作用 | 必填 |
|----|------|------|
| `[project]` | 名称/版本/依赖（PEP 621 标准字段） | 是 |
| `[project.dependencies]` | 运行时依赖（数组） | 是 |
| `[project.optional-dependencies]` | 用户可选 extra（如 `pip install pkg[redis]`） | 否 |
| `[build-system]` | 构建后端（打包发布时用） | 发包时是 |
| `[tool.*]` | 工具配置（ruff/mypy/pytest） | 否 |

## 正例

```toml
[project]
name = "myapp"
version = "1.2.0"
description = "Demo service"
readme = "README.md"
requires-python = ">=3.11"
authors = [{ name = "Team", email = "team@example.com" }]
license = "MIT"
dependencies = [
    "httpx>=0.27",
    "pydantic>=2.6",
]

# 用户安装时可选启用：pip install myapp[redis]
[project.optional-dependencies]
redis = ["redis>=5.0"]
all = ["myapp[redis]"]

# 构建后端：纯 Python 包推荐 hatchling
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
```

约束写法：用 `>=` 设下界保兼容，**不要**用 `==` 钉死（钉死交给 lockfile，见兄弟叶子）。

## 反例

```toml
# ❌ 在 dependencies 里钉死精确版本 —— 库被依赖时会引发版本冲突
dependencies = ["httpx==0.27.2"]

# ✅ 声明兼容下界，精确版本由 uv.lock 锁定
dependencies = ["httpx>=0.27"]
```

```toml
# ❌ 把开发/测试工具塞进运行时 dependencies —— 用户安装会被迫装 pytest
dependencies = ["pydantic>=2.6", "pytest>=8.0"]

# ✅ 开发依赖用依赖组（见 lockfile-reproducible），不进 [project].dependencies
```

```python
# ❌ 还在用 setup.py 声明元数据（已被 PEP 621 取代）
from setuptools import setup
setup(name="myapp", version="1.2.0", install_requires=["httpx"])
```

## 自检

- [ ] 元数据全在 `[project]`，没有遗留 `setup.py` / `setup.cfg`？
- [ ] `requires-python` 已声明（如 `>=3.11`）？
- [ ] 运行时依赖用 `>=` 下界，没用 `==` 钉死？
- [ ] 开发/测试工具没混进 `[project].dependencies`？
- [ ] 发包项目配了 `[build-system]`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`uv-workflow.md`](./uv-workflow.md) · [`lockfile-reproducible.md`](./lockfile-reproducible.md) · [`build-publish.md`](./build-publish.md)
