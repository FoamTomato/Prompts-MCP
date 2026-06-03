---
name: py-test-coverage-gate
description: 用 pytest-cov 量覆盖率、开分支覆盖并在 CI 卡阈值。Use when 测量覆盖率 / 开启 branch coverage / 配置 fail_under / 在 CI 加覆盖门禁。
parent: ./index.md
paths:
- '*.py'
- 'py/**/*.py'
- 'tests/**/*.py'
triggers:
  keywords:
  - 覆盖率
  - 分支覆盖
  - 覆盖门禁
  - pytest-cov
  - branch coverage
  - fail_under
effort: medium
context: inline
version: '1.0'
---
# Python · 覆盖率门禁

## 规则

| 项 | 规则 |
|----|------|
| 工具 | `pytest-cov`（底层 coverage.py），`pytest --cov=<包>` |
| 分支覆盖 | 必开 `branch = true`：行覆盖不能发现没走的分支 |
| 门禁 | `fail_under` 设阈值，未达**退出非 0**，CI 据此卡 |
| 范围 | `source` 指向被测包，**别**统计测试目录本身 |
| 排除 | 用 `# pragma: no cover` 标真不可达分支，不要为凑数滥用 |
| 报告 | CI 出 `xml`(给平台) 或 `term-missing`(看缺哪些行) |

## 正例

```toml
# pyproject.toml
[tool.coverage.run]
source = ["myapp"]               # 只统计源码包
branch = true                    # 分支覆盖，不只行覆盖

[tool.coverage.report]
fail_under = 85                  # 低于 85% 退出码非 0
show_missing = true
exclude_also = ["if TYPE_CHECKING:", "raise NotImplementedError"]
```

```yaml
# .github/workflows/ci.yml
- name: Test with coverage gate
  run: pytest --cov=myapp --cov-branch --cov-report=term-missing
  # fail_under 已在 pyproject，未达阈值此步骤失败，PR 被挡
```

```python
def parse(mode: str) -> int:
    if mode == "fast":
        return 1
    elif mode == "slow":         # branch=true 才能发现这条分支没被测到
        return 2
    raise ValueError(mode)       # pragma: no cover —— 防御性，真不可达
```

## 反例

```python
# ❌ 1. 只看行覆盖率，没开 branch —— if 只测了 True 分支也能报 100%
# [tool.coverage.run] 漏了 branch = true

# ❌ 2. 把 tests 算进 source —— 测试代码自己覆盖自己，数字虚高
[tool.coverage.run]
source = ["myapp", "tests"]      # 删掉 tests

# ❌ 3. 设了 fail_under 但 CI 用 `|| true` 吞掉退出码 —— 门禁形同虚设
run: pytest --cov=myapp || true  # 永远绿，覆盖率跌了也不报
```

理由：行覆盖会把“分支只走了一半”误报成满分；统计测试目录拉高虚假数字；用 `|| true` 吞退出码让阈值无法真正阻断合并。

## 自检

- [ ] 开了 `branch = true`（分支覆盖）？
- [ ] `source` 只含源码包，没把 `tests` 算进去？
- [ ] 设了 `fail_under`，且 CI 没用 `|| true` 吞退出码？
- [ ] `pragma: no cover` 只标真不可达，没拿来凑数？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`pytest-structure.md`](./pytest-structure.md) · [`async-and-http-test.md`](./async-and-http-test.md) · [`parametrize.md`](./parametrize.md)
