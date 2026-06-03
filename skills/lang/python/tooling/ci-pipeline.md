---
name: py-ci-pipeline
description: GitHub Actions 流水线 lint→typecheck→test→coverage 门禁。Use when 写 CI workflow / 设覆盖率门禁 / 编排 lint typecheck test 顺序。
parent: ./index.md
paths:
- '*.py'
- .github/workflows/*.yml
triggers:
  keywords:
  - 流水线
  - CI
  - GitHub Actions
  - 覆盖率门禁
  - coverage
effort: medium
context: inline
version: '1.0'
---
# Python · CI 流水线门禁

## 规则

| 规则 | 说明 |
|------|------|
| 阶段顺序 | lint → typecheck → test → coverage，快的先跑，早失败早反馈 |
| 用 uv 装环境 | `uv sync` 按 lockfile 复现，比 pip 快且确定 |
| 锁 Python 版本 | 用 `actions/setup-python` 或 uv 指定版本，与 target 一致 |
| 缓存依赖 | 缓存 uv / pip 目录，缩短重复构建 |
| 覆盖率设阈值 | `--cov-fail-under=N`，低于即 fail |
| 失败要真红 | 任一步非零退出码就中断，不用 `continue-on-error` 掩盖 |

## 正例

`.github/workflows/ci.yml`：

```yaml
name: ci
on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
        with:
          enable-cache: true
      - run: uv sync --frozen          # 按 lockfile 复现
      - run: uv run ruff check .        # lint
      - run: uv run ruff format --check .
      - run: uv run mypy .              # typecheck
      - run: uv run pytest --cov=src --cov-branch --cov-fail-under=85
```

`pyproject.toml` 里的覆盖率配置：

```toml
[tool.coverage.report]
show_missing = true
fail_under = 85
```

## 反例

```yaml
# ❌ 把 test 放在 lint 前，慢步骤先跑，反馈晚
- run: uv run pytest        # 应放最后
- run: uv run ruff check .  # lint 该最先

# ❌ 用 continue-on-error 让红变绿
- run: uv run mypy .
  continue-on-error: true   # 门禁失效

# ❌ 不带 --cov-fail-under，覆盖率只展示不卡
- run: uv run pytest --cov=src   # 缺阈值
```

```yaml
# ❌ pip install 不锁版本，构建不可复现
- run: pip install -r requirements.txt   # → uv sync --frozen
```

## 自检

- [ ] 阶段顺序是 lint → typecheck → test → coverage？
- [ ] 用 `uv sync --frozen` 按 lockfile 复现环境？
- [ ] 启用了依赖缓存（`enable-cache` 或 actions/cache）？
- [ ] 覆盖率有 `--cov-fail-under` / `fail_under` 阈值？
- [ ] 没有 `continue-on-error` 或 `|| true` 掩盖失败？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`ruff-lint-format.md`](./ruff-lint-format.md) · [`type-checker-ci.md`](./type-checker-ci.md) · [`pre-commit-hooks.md`](./pre-commit-hooks.md)
