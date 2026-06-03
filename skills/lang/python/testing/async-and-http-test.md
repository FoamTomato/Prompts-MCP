---
name: py-test-async-and-http-test
description: 用 pytest-asyncio 测协程、respx/responses mock 出站 HTTP、freezegun 冻结时间。Use when 测 async 函数 / mock httpx 或 requests 请求 / 固定 now()。
parent: ./index.md
paths:
- '*.py'
- 'py/**/*.py'
- 'tests/**/*.py'
triggers:
  keywords:
  - 异步测试
  - 时间冻结
  - pytest-asyncio
  - respx
  - responses
  - freezegun
effort: medium
context: inline
version: '1.0'
---
# Python · 异步与 HTTP 测试

## 规则

| 场景 | 工具 | 要点 |
|------|------|------|
| 测 `async def` | pytest-asyncio | 用例标 `@pytest.mark.asyncio`；配 `asyncio_mode = "auto"` 可免标记 |
| mock httpx 出站 | respx | 拦截 URL，断言被调用，不发真请求 |
| mock requests 出站 | responses | 注册 URL → 假响应 |
| 冻结时间 | freezegun | `@freeze_time("...")` 固定 `now()`，让时间相关断言确定 |
| 异步 fixture | pytest-asyncio | fixture 也可 `async def` + `yield` |

## 正例

```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"            # async 用例无需逐个标 @pytest.mark.asyncio
```

```python
import pytest, respx, httpx
from freezegun import freeze_time

async def get_profile(uid: int) -> dict:
    async with httpx.AsyncClient() as c:
        r = await c.get(f"https://api/users/{uid}")
        return r.json()

@respx.mock
async def test_get_profile():
    route = respx.get("https://api/users/1").mock(
        return_value=httpx.Response(200, json={"id": 1})
    )
    assert (await get_profile(1)) == {"id": 1}
    assert route.called                       # 断言确实发出了请求

@freeze_time("2026-01-01 00:00:00")
def test_token_expiry():
    token = issue_token(ttl_seconds=60)
    assert token.expires_at.isoformat() == "2026-01-01T00:01:00"
```

## 反例

```python
# ❌ 1. 没装/没标 asyncio，直接定义 async 测试 —— pytest 收集成协程没 await，静默不跑（绿但没测）
async def test_get_profile():        # 无 @pytest.mark.asyncio 且非 auto 模式
    assert await get_profile(1)

# ❌ 2. 自己 asyncio.run 包一层 —— 拿不到 async fixture，事件循环也可能冲突
def test_get_profile():
    assert asyncio.run(get_profile(1))  # 用 pytest-asyncio 而非手动跑

# ❌ 3. 断言依赖真实时间 —— 跨午夜/慢机偶发失败
assert token.expires_at.date() == date.today()  # 用 freeze_time 固定
```

理由：未启用 asyncio 插件时协程用例不被 await，是最隐蔽的“假绿”；手动 `asyncio.run` 与插件管理的事件循环打架；真实时钟让断言变成不确定测试。

## 自检

- [ ] async 用例配了 `asyncio_mode="auto"` 或逐个标 `@pytest.mark.asyncio`？
- [ ] 出站 HTTP 用 respx/responses 拦截，且断言了 `route.called`？
- [ ] 时间相关断言用 `freeze_time` 固定，不依赖 `now()`？
- [ ] 没有手写 `asyncio.run` 包测试体？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mock-patch.md`](./mock-patch.md) · [`fixture-usage.md`](./fixture-usage.md) · [`coverage-gate.md`](./coverage-gate.md)
