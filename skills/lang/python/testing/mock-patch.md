---
name: py-test-mock-patch
description: unittest.mock 的 patch 打桩位置、MagicMock 断言与 monkeypatch/pytest-mock。Use when 隔离外部依赖 / mock 函数对象 / 改环境变量 / 决定 patch 哪个名字。
parent: ./index.md
paths:
- '*.py'
- 'py/**/*.py'
- 'tests/**/*.py'
triggers:
  keywords:
  - 打桩
  - 替身
  - mock
  - patch
  - monkeypatch
  - MagicMock
effort: medium
context: inline
version: '1.0'
---
# Python · mock 与 patch

## 规则

| 项 | 规则 |
|----|------|
| patch 位置 | **patch 使用处的名字，不是定义处**：`patch("myapp.svc.requests")`，不是 `patch("requests")` |
| 用法 | 优先 `mocker`(pytest-mock) fixture，免去 `with`/装饰器嵌套 |
| 返回值 | `mock.return_value=...`；多次不同值用 `side_effect=[...]` |
| 抛异常 | `side_effect=SomeError(...)` |
| 断言 | `assert_called_once_with(...)` 校验调用，不只校验结果 |
| 环境/属性 | 改 env / 对象属性用 `monkeypatch.setenv` / `monkeypatch.setattr`，自动还原 |

## 正例

```python
# myapp/svc.py
import requests
def fetch_user(uid: int) -> dict:
    return requests.get(f"https://api/users/{uid}").json()
```

```python
# tests/test_svc.py
def test_fetch_user(mocker):
    # patch svc 模块里引用的 requests，而非 requests 包本身
    mock_get = mocker.patch("myapp.svc.requests.get")
    mock_get.return_value.json.return_value = {"id": 1, "name": "a"}

    assert fetch_user(1) == {"id": 1, "name": "a"}
    mock_get.assert_called_once_with("https://api/users/1")

def test_fetch_user_retries_on_timeout(mocker):
    mock_get = mocker.patch("myapp.svc.requests.get")
    mock_get.side_effect = [Timeout(), mocker.Mock(json=lambda: {"id": 1})]
    assert fetch_user(1)["id"] == 1

def test_reads_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")   # 用例结束自动还原
    assert load_config().api_key == "test-key"
```

## 反例

```python
# ❌ 1. patch 到定义处 —— 被测模块早已 import 了名字，桩打不上，真请求发出去
mocker.patch("requests.get")          # 应为 "myapp.svc.requests.get"

# ❌ 2. 只断言返回值，不断言交互 —— 重构掉这次调用测试照样绿
result = fetch_user(1)
assert result["id"] == 1              # 没验证真的请求了正确 URL

# ❌ 3. 手动 setattr 改环境/属性不还原 —— 污染后续用例
os.environ["API_KEY"] = "x"           # 用 monkeypatch.setenv，会自动复原
```

理由：`patch` 替换的是“名字绑定”，必须打在被测代码查找该名字的命名空间；漏断言交互让 mock 失去验证意义；手改全局状态不还原会让测试顺序相关、偶发失败。

## 自检

- [ ] `patch` 的目标是**使用处**完整路径，不是定义处？
- [ ] 既断言了结果，也用 `assert_called_*` 断言了交互？
- [ ] 多次返回用 `side_effect` 列表，抛错用 `side_effect=异常`？
- [ ] 改 env / 属性用 `monkeypatch`，没手动改全局不还原？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`fixture-usage.md`](./fixture-usage.md) · [`async-and-http-test.md`](./async-and-http-test.md) · [`parametrize.md`](./parametrize.md)
