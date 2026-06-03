---
name: py-err-raise-from-chaining
description: raise ... from 显式链式异常，保留 __cause__；何时用 from None 切断上下文。Use when 把底层异常转换成领域异常 / traceback 缺少根因 / 抑制无关的 During handling 链。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 链式异常
  - raise from
  - __cause__
  - from None
  - 异常转换
  - 上下文保留
effort: medium
context: inline
version: '1.0'
---
# Python · raise from 链式异常

## 规则

| 写法 | traceback 表现 | 何时用 |
|------|---------------|--------|
| `raise New() from err` | 设 `__cause__`，打印 “The above ... direct cause” | 把底层异常转成领域异常，**保留根因** |
| `raise New()`（在 except 内裸抛） | 自动设 `__context__`，打印 “During handling ...” | 隐式链，信息没 `from` 清晰 |
| `raise New() from None` | 清空链，只显示新异常 | 底层异常是实现细节、对调用方无意义时 |

在 `except` 块里转换异常时**首选 `from err`**：让 traceback 同时显示“你抛的领域异常”和“真正的根因”，排查不用猜。

## 正例

```python
class ConfigError(Exception):
    pass

def load_config(path: str) -> dict:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise ConfigError(f"配置缺失: {path}") from e     # 保留 FileNotFoundError 根因
    except json.JSONDecodeError as e:
        raise ConfigError(f"配置格式错误: {path}") from e
```

底层异常对调用方无意义时，用 `from None` 切断，给出干净的领域错误：

```python
def get_user(uid: int) -> User:
    try:
        return _cache[uid]
    except KeyError:
        raise UserNotFound(uid) from None    # 调用方不关心内部是 dict 还是别的
```

## 反例

```python
# ❌ 裸 raise 新异常 —— 根因被埋进 __context__，且文案像“吞掉了原错误”
try:
    parse(payload)
except ValueError:
    raise ApiException("X009", "解析失败")        # 看不出底层是 ValueError 还是别的

# ✅ 用 from 显式链接
except ValueError as e:
    raise ApiException("X009", "解析失败") from e

# ❌ 误用 from None 把真实根因抹掉，排查时无从下手
except OSError:
    raise ConfigError("读取失败") from None        # OSError 的 errno 丢了
```

理由：转换异常时若不写 `from`，根因虽仍在 `__context__` 但语义模糊；该保留根因却写 `from None`，会永久丢失定位信息。`from None` 仅用于底层异常确实是无关实现细节的场景。

## 自检

- [ ] `except` 内转换异常时用了 `raise New(...) from err`？
- [ ] 只在“底层异常对调用方无意义”时才用 `from None`？
- [ ] 没有在 except 里裸抛新异常导致根因被埋进隐式 `__context__`？
- [ ] 领域异常的 message 不重复 traceback 已有的根因信息？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`exception-group.md`](./exception-group.md) · [`eafp-vs-lbyl.md`](./eafp-vs-lbyl.md) · [`api-exception.md`](./api-exception.md)
- 配套：[`logger-exc-info.md`](./logger-exc-info.md)（记录链式异常的 traceback）
