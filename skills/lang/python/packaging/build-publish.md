---
name: py-build-publish
description: 构建与发布 — uv build 出 wheel+sdist、uv publish 上 PyPI、entry points 暴露 CLI、editable 本地安装。Use when 打包 / 发布到 PyPI / 配命令行入口 / 本地可编辑安装。
parent: ./index.md
paths:
- pyproject.toml
- '*.toml'
- 'py/**/*.py'
triggers:
  keywords:
  - 打包发布
  - uv build
  - uv publish
  - wheel
  - entry points
  - editable
effort: medium
context: inline
version: '1.0'
---
# Python · 构建与发布

## 规则

| 你要做的事 | 命令 / 配置 | 产物 |
|-----------|------------|------|
| 构建分发包 | `uv build` | `dist/*.whl` + `dist/*.tar.gz` |
| 只出 wheel | `uv build --wheel` | wheel（二进制，安装快） |
| 只出 sdist | `uv build --sdist` | 源码 tar.gz（含构建脚本） |
| 发布到 PyPI | `uv publish` | 上传 dist/ 到 PyPI |
| 暴露命令行入口 | `[project.scripts]` | 安装后可直接调命令 |
| 本地可编辑安装 | `uv pip install -e .` | 改源码即生效，免重装 |

wheel 与 sdist 都要发：wheel 给装得快，sdist 给无预编译 wheel 的平台兜底。

## 正例

```toml
# pyproject.toml —— entry points：安装后多出一个 `myapp` 命令
[project.scripts]
myapp = "myapp.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

```python
# myapp/cli.py —— entry point 指向的函数（无参，自己读 argv）
def main() -> None:
    import sys
    print(f"running with {sys.argv[1:]}")
```

```bash
# 1. 构建：默认同时产出 wheel + sdist 到 dist/
uv build

# 2. 发布到 PyPI（token 走环境变量 / 交互；CI 用受信发布 OIDC 免 token）
uv publish

# 3. 本地开发库时可编辑安装：改 .py 立即生效，不必重装
uv pip install -e .
```

## 反例

```bash
# ❌ 把 build / twine 当依赖手动装再调，多一层工具
pip install build twine && python -m build && twine upload dist/*

# ✅ uv 内建，一条链路搞定
uv build && uv publish
```

```toml
# ❌ 用 [project.entry-points.console_scripts] 这种旧写法叠 console_scripts 组名
[project.entry-points.console_scripts]
myapp = "myapp.cli:main"

# ✅ PEP 621 的简写就是 [project.scripts]
[project.scripts]
myapp = "myapp.cli:main"
```

```bash
# ❌ 发布前没清旧产物，dist/ 里混着上个版本的 wheel 一起被传
uv publish

# ✅ 先清 dist/ 再 build，确保只发本次产物
rm -rf dist/ && uv build && uv publish
```

## 自检

- [ ] `uv build` 同时产出了 wheel 和 sdist？
- [ ] 发布前清空了旧的 `dist/`？
- [ ] CLI 入口用 `[project.scripts]`（不是旧 `console_scripts` 写法）？
- [ ] 本地开发库用 `uv pip install -e .` 而非每次重装？
- [ ] CI 发布优先用 OIDC 受信发布，避免明文 token？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`uv-workflow.md`](./uv-workflow.md) · [`pyproject-toml.md`](./pyproject-toml.md) · [`lockfile-reproducible.md`](./lockfile-reproducible.md)
