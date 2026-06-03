---
name: py-err-eafp-vs-lbyl
description: EAFP（先做后捕获）vs LBYL（先检查后做）风格选择，及 contextlib.suppress 忽略预期异常。Use when 纠结用 try 还是 if 先检查 / 想消除 TOCTOU 竞态 / 静默忽略某个预期异常。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - EAFP
  - LBYL
  - 先检查后执行
  - suppress
  - contextlib
  - 竞态条件
effort: medium
context: inline
version: '1.0'
---
# Python · EAFP vs LBYL

## 规则

- **EAFP**（Easier to Ask Forgiveness than Permission）：直接做，失败用 `try/except` 兜。Python 的惯用风格。
- **LBYL**（Look Before You Leap）：先 `if` 检查再做。

| 用哪个 | 判据 |
|--------|------|
| **EAFP** 默认 | 正常路径成功率高；操作不可分（文件 / dict / 网络），检查与执行之间可能被改 |
| **LBYL** | 检查无副作用且廉价；失败是高频正常分支，靠异常代价高 |
| `contextlib.suppress(X)` | 只想**忽略**某个预期异常、不做任何处理 |

关键：LBYL 在并发 / 文件 / 外部状态下有 **TOCTOU 竞态**——检查通过到执行之间状态可能已变，EAFP 没有这个窗口。

## 正例

```python
# EAFP：dict 取值，命中率高，一步到位
try:
    name = config["display_name"]
except KeyError:
    name = "匿名"
# 等价惯用写法：config.get("display_name", "匿名")

# EAFP：消除文件存在性的 TOCTOU 竞态
try:
    with open(path) as f:
        data = f.read()
except FileNotFoundError:
    data = default
```

`contextlib.suppress` 取代“空 except”，意图清晰：

```python
import contextlib

with contextlib.suppress(FileNotFoundError):
    os.remove(tmp_path)        # 文件本就可能不存在，删不到无所谓
```

## 反例

```python
# ❌ LBYL 检查文件 —— 检查到打开之间文件可能被删（TOCTOU）
if os.path.exists(path):
    with open(path) as f:    # 仍可能 FileNotFoundError
        ...

# ❌ 用 try/except/pass 静默忽略，意图不明、容易误吞别的异常
try:
    os.remove(tmp_path)
except Exception:            # 范围过宽，且 pass 像漏写
    pass
# ✅ 用 suppress 且只针对预期异常
with contextlib.suppress(FileNotFoundError):
    os.remove(tmp_path)
```

理由：`os.path.exists` 后再 open 存在竞态窗口，直接 open + 捕获更安全；`suppress(具体类型)` 比 `except Exception: pass` 意图明确且不会误吞无关异常。注意 `suppress` 是“无声忽略”，需要日志/降级时仍用显式 `except`（见 no-bare-except）。

## 自检

- [ ] 默认用 EAFP，只在检查廉价无副作用时才退回 LBYL？
- [ ] 涉及文件 / 并发 / 外部状态时避免 LBYL 的 TOCTOU 竞态？
- [ ] 只想忽略预期异常时用 `contextlib.suppress(具体类型)` 而非 `except: pass`？
- [ ] `suppress` 范围收窄到具体异常类型，没用 `Exception` 兜底？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`raise-from-chaining.md`](./raise-from-chaining.md) · [`exception-group.md`](./exception-group.md) · [`no-bare-except.md`](./no-bare-except.md)
