---
name: py-test-pytest-structure
description: pytest 测试发现规则、目录布局与 assert 自省。Use when 新建测试文件 / 决定测试放哪 / 命名 test 函数 / 配置 testpaths。
parent: ./index.md
paths:
- '*.py'
- 'py/**/*.py'
- 'tests/**/*.py'
triggers:
  keywords:
  - 测试发现
  - 测试目录结构
  - pytest
  - test discovery
  - conftest
  - assert
effort: medium
context: inline
version: '1.0'
---
# Python · pytest 测试结构与发现

## 规则

| 项 | 规则 |
|----|------|
| 测试文件名 | `test_*.py` 或 `*_test.py`（默认发现规则） |
| 测试函数名 | 以 `test_` 开头；测试类以 `Test` 开头且**无** `__init__` |
| 断言 | 直接用 `assert`，靠 pytest 自省看到两边值；**不要** `unittest` 的 `self.assertEqual` |
| 目录布局 | 推荐 `tests/` 与源码同级；`src/` 布局下源码包放 `src/` |
| 发现根 | 在 `pyproject.toml` 显式声明 `testpaths`，避免误扫 |

## 正例

```python
# tests/test_pricing.py
from myapp.pricing import apply_discount

def test_apply_discount_halves_price():
    assert apply_discount(100, rate=0.5) == 50

def test_apply_discount_rejects_negative_rate():
    import pytest
    with pytest.raises(ValueError):
        apply_discount(100, rate=-0.1)

class TestCart:                       # 仅分组，无 __init__
    def test_empty_cart_total_is_zero(self):
        assert Cart().total() == 0
```

```toml
# pyproject.toml —— 显式声明发现范围
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra --strict-markers --strict-config"
```

`assert a == b` 失败时 pytest 会展开两边实际值；无需手写消息。

## 反例

```python
# ❌ 1. 用 unittest 风格断言 —— 丢失 pytest 自省输出
import unittest
class TestPricing(unittest.TestCase):
    def test_x(self):
        self.assertEqual(apply_discount(100, 0.5), 50)  # 失败时只说 "not equal"

# ❌ 2. 测试类带 __init__ —— pytest 跳过整个类且不报错
class TestCart:
    def __init__(self):              # 会被静默忽略，用例不执行
        self.cart = Cart()

# ❌ 3. 文件名 pricing_tests.py —— 不匹配默认 glob，永不被发现
```

理由：自定义断言方法掩盖了失败现场；`__init__` 让 pytest 无法实例化收集类；非 `test_*` 命名直接漏跑，最危险的是“绿色但其实没测”。

## 自检

- [ ] 文件名是 `test_*.py`，函数名以 `test_` 开头？
- [ ] 测试类无 `__init__`，用 fixture 替代构造？
- [ ] 用裸 `assert`，没引入 `self.assertXxx`？
- [ ] `pyproject.toml` 里声明了 `testpaths`、`--strict-markers`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`fixture-usage.md`](./fixture-usage.md) · [`parametrize.md`](./parametrize.md) · [`coverage-gate.md`](./coverage-gate.md)
