---
name: python-no-bare-except
description: "禁 except: pass 和 except Exception 不记日志"
parent: ./index.md
paths:
  - "backend/**/*.py"
  - "py/**/*.py"
triggers:
  keywords: [bare except, except, 异常吞掉]
effort: medium
context: inline
version: "1.0"
---

# Python · 禁裸 except

## 规则

不允许：

```python
# ❌ 1. 裸 except — 连 KeyboardInterrupt 都吞
try: ...
except: pass

# ❌ 2. except Exception 不记日志
try: ...
except Exception:
    pass

# ❌ 3. except Exception 不重抛
try: ...
except Exception as e:
    logger.error(f"failed: {e}")   # 静默掉了，调用方以为成功
    return None
```

## 正确做法

### 必须捕获并恢复

```python
try:
    return await primary_provider.call(req)
except (TimeoutError, ConnectionError) as e:
    logger.warning(f"主 provider 失败，切换备用: {e}")
    return await backup_provider.call(req)
```

捕获**具体异常类型**，不要 `except Exception`。

### 必须抛出但要清理

```python
deducted = False
try:
    deducted = await deduct_credits(uid, 1)
    return await call_llm(req)
except ApiException:
    raise
except Exception as e:
    logger.exception(f"LLM 调用失败 - uid={uid}: {e}")
    raise ApiException(msg="生成失败，请重试")
finally:
    if deducted and not success:
        await restore_credits(uid, 1)
```

## except 选择决策表

| 你想 | 用什么 |
|------|-------|
| 失败降级 | `except (TimeoutError, ConnectionError) as e:` |
| 业务异常透传 | `except ApiException: raise` |
| 未知异常友好提示 | `except Exception as e: logger.exception(...); raise ApiException(...)` |
| 资源清理 | `finally:`（不是 except） |

## 反例

```python
# ❌ 把所有错都当成 None
try:
    user = await User.filter(id=uid).first()
except:
    user = None

# ✅ 仅 Tortoise 的 DoesNotExist 才返回 None
user = await User.filter(id=uid).first()  # 已经返回 None，无需 try
```

## 自检

- [ ] 没有 `except:` 裸接？
- [ ] 没有 `except Exception: pass`？
- [ ] `except Exception` 都带 `exc_info=True` 并 raise？
- [ ] 业务异常用 `except ApiException: raise` 透传？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`api-exception.md`](./api-exception.md) · [`logger-exc-info.md`](./logger-exc-info.md)

