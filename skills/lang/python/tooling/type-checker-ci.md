---
name: py-type-checker-ci
description: 把类型检查器 mypy strict / pyright / Astral ty 接入 CI 并设门禁。Use when 选型类型检查器 / 配 strict 模式 / 让 typecheck 卡住流水线。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 类型检查
  - mypy
  - pyright
  - strict
  - typecheck
effort: medium
context: inline
version: '1.0'
---
# Python · 类型检查器接入 CI

## 规则

| 规则 | 说明 |
|------|------|
| 选一个为主 | mypy（生态最广）/ pyright（IDE 一致、快）/ ty（Astral，Rust 实现，最快但较新） |
| 开 strict | 新项目从 `strict = true` 起步，比逐条开更省心 |
| 配置进 `pyproject.toml` | mypy 用 `[tool.mypy]`，pyright 用 `[tool.pyright]` |
| CI 必须能 fail | typecheck 非零退出码要卡住流水线，不能仅警告 |
| 第三方缺类型用 stub | 装 `types-*` 包或在 overrides 里 `ignore_missing_imports` |
| 局部豁免要带码 | `# type: ignore[code]` 写明具体错误码，不裸 ignore |

## 正例

`pyproject.toml`（mypy strict）：

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_unused_ignores = true
warn_redundant_casts = true
files = ["src", "tests"]

[[tool.mypy.overrides]]
module = ["some_untyped_lib.*"]
ignore_missing_imports = true
```

pyright 等价：

```toml
[tool.pyright]
include = ["src", "tests"]
typeCheckingMode = "strict"
pythonVersion = "3.12"
```

CI 步骤（任选其一）：

```bash
mypy .                  # 非零退出码即 fail
pyright                 # 同理
uvx ty check            # Astral ty，最快
```

## 反例

```toml
# ❌ strict 未开，漏检大量隐式 Any
[tool.mypy]
# 没有 strict = true，untyped def 不报

# ❌ 同时跑 mypy + pyright 当门禁，规则差异制造噪音
# → 选一个当门禁，另一个最多作 IDE 提示
```

```python
# ❌ 裸 ignore 掩盖一切错误
result = legacy()  # type: ignore

# ✅ 标明错误码，将来修了会被 warn_unused_ignores 提醒
result = legacy()  # type: ignore[no-any-return]
```

```yaml
# ❌ CI 用 || true 吞掉失败，门禁形同虚设
- run: mypy . || true
```

## 自检

- [ ] 选定单一检查器作为 CI 门禁（mypy / pyright / ty 三选一）？
- [ ] 开了 `strict`（或 pyright 的 strict 模式）？
- [ ] CI 里 typecheck 失败会让流水线红，没有 `|| true`？
- [ ] 所有 `# type: ignore` 都带了具体错误码？
- [ ] 第三方缺类型用 `types-*` stub 或 overrides，而非全局关检查？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`ci-pipeline.md`](./ci-pipeline.md) · [`pre-commit-hooks.md`](./pre-commit-hooks.md) · [`ruff-lint-format.md`](./ruff-lint-format.md)
