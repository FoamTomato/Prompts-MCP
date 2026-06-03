---
name: python-api-exception
description: ApiException 三件套 — 业务异常专用类 + 业务错误码 + 配合断言模式。Use when 写 Python 后端代码 /
  评审涉及 `api-exception` 的 PR。
parent: ./index.md
paths:
- backend/**/*.py
- py/**/*.py
triggers:
  keywords:
  - ApiException
  - 异常
  - raise
  - BusinessError
effort: medium
context: inline
version: '2.0'
---
# Python · ApiException 三件套

## 规则

业务异常**只**抛 `ApiException(code, message)`，不要用裸 `Exception` 或继承的其他类。
更进一步：业务校验**首选断言**（`<Domain>Asserts.<语义方法>(...)`），让 raise 隐藏在断言里。

## ApiException 标准签名

```python
# py/core/exceptions.py
class ApiException(HTTPException):
    def __init__(
        self,
        code: str,            # 业务错误码字符串（A001 / D001 / X009 …）
        message: str,         # 面向用户的描述
        http_status: int = 400,
        data: Any = None,
    ):
        self.error_code = code
        self.error_message = message
        self.error_data = data
        super().__init__(
            status_code=http_status,
            detail={"code": code, "message": message, "data": data},
        )
```

## 三件套（边界处理模式）

```python
async def process_document(req: ProcessReq) -> Result:
    try:
        result = await perform_operation(req)
        logger.info(f"操作成功 - user_id={req.user_id}, result_id={result.id}")
        return result

    except ApiException:
        raise  # 业务异常直接传播，不二次包装

    except Exception as e:
        logger.error(f"操作失败 - user_id={req.user_id}: {e}", exc_info=True)
        raise ApiException("X009", "服务器内部错误")
```

三段含义：
1. **正常路径**：成功的入口日志（`info` 级，含关键参数）
2. **业务异常**：原样传播给中间件统一处理（不二次包装）
3. **未知异常**：记录 `exc_info=True` 后兜底为 X009

## 配合断言模式（优先）

业务层**首选断言**而非手写 if + raise：

```python
# ❌ 散落 if + raise
async def list_chapters(textbook_id: str):
    textbook = await Textbook.get_or_none(id=textbook_id)
    if textbook is None:
        raise ApiException("G001", f"课本不存在: {textbook_id}", http_status=404)
    ...

# ✅ 用 TextbookAsserts（语义化业务接口）
from asserts.textbook import TextbookAsserts

async def list_chapters(textbook_id: str):
    textbook = await Textbook.get_or_none(id=textbook_id)
    TextbookAsserts.found(textbook, textbook_id)
    ...
```

完整断言体系见 [`/.claude/skills/design-pattern/assertion/`](../../../design-pattern/assertion/index.md)。

## 业务错误码

详见 [`/.ai/skills/core/error_code_dict.md`](../../../../../.ai/skills/core/error_code_dict.md)。

| 前缀 | 模块 |
|------|------|
| A | anonymous_session（身份） |
| B | presentations（课件） |
| C | assets（媒体资产） |
| D | outlines |
| E | tasks / AI |
| F | templates / themes |
| G | textbooks / chapters |
| H | settings |
| I | papers |
| J | knowledge |
| R | referral |
| S | session / 积分 |
| X | 通用 / 内部 |

直接抛 ApiException 时：

```python
raise ApiException("S005", f"积分余额不足（需要 {cost}）", http_status=402)
```

## 反例

```python
# ❌ 抛裸 Exception
raise Exception("error")

# ❌ 空 except: pass — 异常吞掉
try:
    await foo()
except:
    pass

# ❌ logger.error 不带 exc_info
except Exception as e:
    logger.error(f"failed: {e}")  # 没有 traceback，无法排查
    raise

# ❌ 二次包装 ApiException（丢失原始 code）
except ApiException as e:
    raise ApiException("X009", e.error_message)

# ❌ 手写 if + raise（应改用 Asserts）
if textbook is None:
    raise ApiException("G001", f"课本不存在: {tid}", http_status=404)
```

## 自检

- [ ] 业务异常用 `ApiException("<code>", "<message>", http_status=...)`？
- [ ] 业务校验首选 `<Domain>Asserts.<语义方法>(...)` 而非手写 if + raise？
- [ ] `except Exception` 必带 `exc_info=True`？
- [ ] `except ApiException: raise` 直接传播，不二次包装？
- [ ] 没有空 `except: pass`？
- [ ] code 是字符串（A001 / G002）不是 int？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`logger-exc-info.md`](./logger-exc-info.md) · [`no-bare-except.md`](./no-bare-except.md)
- 配套：[`../../../framework/fastapi/middleware/error-handler.md`](../../../framework/fastapi/middleware/error-handler.md)
- **断言模式**：[`../../../design-pattern/assertion/index.md`](../../../design-pattern/assertion/index.md)
