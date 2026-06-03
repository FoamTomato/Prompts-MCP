---
name: py-lockfile-reproducible
description: 可复现安装 — uv.lock 是否提交、dev/test 依赖组划分、CI 用 --frozen 精确复现。Use when 决定提交 lockfile / 分依赖组 / 配 CI 复现安装 / 排查环境不一致。
parent: ./index.md
paths:
- uv.lock
- pyproject.toml
- 'py/**/*.py'
triggers:
  keywords:
  - 锁文件
  - lockfile
  - uv.lock
  - 依赖组
  - dependency-groups
  - 可复现
effort: medium
context: inline
version: '1.0'
---
# Python · 锁文件与可复现安装

## 规则

`uv.lock` 钉住**整棵依赖树**的精确版本与哈希，是可复现的唯一来源。

| 场景 | 是否提交 uv.lock | 安装命令 |
|------|----------------|---------|
| 应用 / 服务 | **提交** | `uv sync`（开发）/ `uv sync --frozen`（CI） |
| 库（被别人依赖） | **提交**（用于自身 CI），发布的 wheel 不含它 | 同上 |

- `pyproject.toml` 声明**范围**（`>=`），`uv.lock` 钉死**精确版本**——两者分工，别混。
- 开发/测试工具放**依赖组**（`[dependency-groups]`），不进 `[project].dependencies`，用户安装不会被带上。

## 正例

```toml
# pyproject.toml —— 依赖组（PEP 735），默认只装 dev 之外的运行时依赖
[dependency-groups]
dev = ["ruff>=0.4", "mypy>=1.10"]
test = ["pytest>=8.0", "pytest-cov>=5.0"]
```

```bash
# 本地开发：解析 + 写 uv.lock + 装上（含默认依赖组）
uv sync

# 只装某些组
uv sync --group test

# CI：禁止改 lock，版本与 uv.lock 完全一致；lock 与 pyproject 不符则报错退出
uv sync --frozen
```

```yaml
# GitHub Actions —— 用 --frozen 保证 CI 装的就是提交的 uv.lock
- run: uv sync --frozen --group test
- run: uv run pytest
```

## 反例

```bash
# ❌ CI 里用 uv sync（不带 --frozen）—— 可能悄悄升级依赖、重写 lock，
#    导致「我本地能跑、CI 却用了不同版本」
uv sync

# ✅ CI 必须 --frozen：lock 与 pyproject 一旦不一致就直接失败
uv sync --frozen
```

```gitignore
# ❌ 把 uv.lock 加进 .gitignore —— 等于放弃可复现，每次安装可能不同
uv.lock

# ✅ 应用与库都要提交 uv.lock
```

```bash
# ❌ 手动 pip freeze > requirements.txt 当锁文件 —— 丢哈希、丢平台标记、易漂移
pip freeze > requirements.txt
```

## 自检

- [ ] `uv.lock` 已提交进 git，没被 ignore？
- [ ] 开发/测试工具在 `[dependency-groups]`，不在 `[project].dependencies`？
- [ ] CI 用 `uv sync --frozen`，而非裸 `uv sync`？
- [ ] 精确版本只在 `uv.lock`，`pyproject.toml` 仍是范围声明？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`uv-workflow.md`](./uv-workflow.md) · [`pyproject-toml.md`](./pyproject-toml.md) · [`build-publish.md`](./build-publish.md)
