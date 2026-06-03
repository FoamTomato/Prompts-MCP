---
name: py-pre-commit-hooks
description: 用 pre-commit 编排 ruff/mypy 钩子，让本地提交与 CI 跑同一套检查。Use when 装提交前钩子 / 编排 ruff mypy / 统一本地与 CI 检查。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 提交钩子
  - pre-commit
  - hooks
  - ruff
  - 钩子编排
effort: medium
context: inline
version: '1.0'
---
# Python · pre-commit 钩子编排

## 规则

| 规则 | 说明 |
|------|------|
| 用 pre-commit 框架 | 不手写 `.git/hooks` 脚本，用 `.pre-commit-config.yaml` 声明 |
| pin 版本 `rev` | 每个 hook 锁定 tag，靠 `pre-commit autoupdate` 升级 |
| 钩子复用 CI 配置 | ruff/mypy 读同一份 `pyproject.toml`，本地与 CI 一致 |
| ruff 先 fix 再 format | `ruff` + `ruff-format` 两个 hook，顺序固定 |
| 安装到 git | `pre-commit install` 写入 `.git/hooks/pre-commit` |
| CI 也跑一遍 | `pre-commit run --all-files` 防止有人没装钩子 |

## 正例

`.pre-commit-config.yaml`：

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff           # lint，自动修
        args: [--fix]
      - id: ruff-format    # 排版
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.2
    hooks:
      - id: mypy
        additional_dependencies: [pydantic, types-requests]
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-yaml
```

启用与运行：

```bash
pre-commit install               # 装进 git 钩子
pre-commit run --all-files       # 首次/CI 全量跑
pre-commit autoupdate            # 升级各 hook 的 rev
```

## 反例

```yaml
# ❌ 不 pin rev，用 main，行为随上游漂移
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: main
  hooks: [{ id: ruff }]

# ❌ mypy 不声明 additional_dependencies，
#    钩子环境缺第三方类型，报一堆 import-untyped
- id: mypy   # 缺 pydantic/types-* → 误报
```

```bash
# ❌ 只在本地装钩子，CI 不跑 → 没装钩子的人能绕过
git commit --no-verify        # 还能直接跳过

# ✅ CI 兜底：pre-commit run --all-files
```

## 自检

- [ ] 用 `.pre-commit-config.yaml`，没有手写 `.git/hooks` 脚本？
- [ ] 每个 hook 都 pin 了 `rev`，不是 `main`？
- [ ] ruff 与 mypy 读同一份 `pyproject.toml`，与 CI 配置一致？
- [ ] mypy hook 的 `additional_dependencies` 列了运行期类型依赖？
- [ ] CI 里有 `pre-commit run --all-files` 兜底？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`ruff-lint-format.md`](./ruff-lint-format.md) · [`type-checker-ci.md`](./type-checker-ci.md) · [`ci-pipeline.md`](./ci-pipeline.md)
