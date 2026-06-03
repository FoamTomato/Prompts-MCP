---
name: py-uv-workflow
description: uv 统一工作流 — venv/add/run/lock/tool 与 Python 版本管理，取代 pip+venv+pyenv+pipx+poetry。Use when 建环境 / 加删依赖 / 跑脚本 / 装 Python 版本 / 装 CLI 工具。
parent: ./index.md
paths:
- '*.py'
- 'py/**/*.py'
- pyproject.toml
- uv.lock
triggers:
  keywords:
  - 依赖管理
  - uv add
  - uv run
  - uv sync
  - 虚拟环境
  - python version
effort: medium
context: inline
version: '1.0'
---
# Python · uv 统一工作流

## 规则

`uv` 一个工具覆盖整条链路，**不要**再混用 `pip` / `python -m venv` / `pyenv` / `pipx` / `poetry`。

| 你要做的事 | uv 命令 | 取代了 |
|-----------|---------|--------|
| 初始化项目 | `uv init` | 手写 pyproject.toml |
| 加运行时依赖 | `uv add httpx` | `pip install` + 手改 deps |
| 加开发依赖组 | `uv add --dev pytest` | poetry `--group dev` |
| 删依赖 | `uv remove httpx` | `pip uninstall` + 手改 |
| 按 lock 装全部 | `uv sync` | `pip install -r` |
| 在项目环境跑命令 | `uv run pytest` | 手动 activate venv |
| 装/选 Python 版本 | `uv python install 3.13` | pyenv |
| 全局装 CLI 工具 | `uv tool install ruff` | pipx |

## 正例

```bash
# 新机器拉到仓库后，一条命令拿到可运行环境（按 uv.lock 精确复现）
uv sync

# 加依赖：自动写进 pyproject.toml 的 [project].dependencies 并更新 uv.lock
uv add "httpx>=0.27"

# 加只在开发/测试用的依赖到 dev 组
uv add --dev pytest pytest-cov ruff mypy

# 跑命令无需手动 activate；uv 自动用项目 .venv
uv run python -m myapp
uv run pytest

# 钉住项目使用的 Python 版本（写入 .python-version）
uv python pin 3.13
```

`uv add` 会**同步**改三处：`pyproject.toml`、`uv.lock`、`.venv`，三者永远一致。

## 反例

```bash
# ❌ 在 uv 项目里直接 pip install —— 装进了 .venv 但没写进 pyproject/uv.lock，
#    队友 uv sync 后没有这个包，CI 会挂
uv run pip install requests

# ✅ 用 uv add，依赖声明与锁文件同步更新
uv add requests
```

```bash
# ❌ 手动 source .venv/bin/activate 再跑，容易跑到错误环境
source .venv/bin/activate && python app.py

# ✅ uv run 保证用的就是本项目锁定的环境
uv run python app.py
```

```bash
# ❌ 用系统 pip 全局装 CLI，污染系统 Python
pip install --user ruff

# ✅ uv tool 隔离安装，每个工具独立环境
uv tool install ruff
```

## 自检

- [ ] 加/删依赖走 `uv add` / `uv remove`，没有手动 `pip install`？
- [ ] 跑命令用 `uv run`，没有手动 activate venv？
- [ ] 全局 CLI 工具用 `uv tool install`，没污染系统 Python？
- [ ] Python 版本用 `uv python pin` 钉住并提交 `.python-version`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`pyproject-toml.md`](./pyproject-toml.md) · [`lockfile-reproducible.md`](./lockfile-reproducible.md) · [`build-publish.md`](./build-publish.md)
