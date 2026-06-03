---
name: py-test-parametrize
description: pytest 参数化 @pytest.mark.parametrize、可读 ids 与间接参数化。Use when 同一逻辑跑多组输入 / 想要清晰用例名 / 参数喂给 fixture。
parent: ./index.md
paths:
- '*.py'
- 'py/**/*.py'
- 'tests/**/*.py'
triggers:
  keywords:
  - 参数化
  - 数据驱动
  - parametrize
  - ids
  - indirect
  - 用例名
effort: medium
context: inline
version: '1.0'
---
# Python · pytest 参数化

## 规则

| 项 | 规则 |
|----|------|
| 一参一组 | `@pytest.mark.parametrize("x", [a, b])`，每组生成独立用例 |
| 多参 | `@pytest.mark.parametrize("a,b,expected", [...])` 用逗号串名 |
| 可读名 | 传 `ids=[...]` 或对每条用 `pytest.param(..., id=...)`，别让名字变 `x0/x1` |
| 标记单条 | `pytest.param(..., marks=pytest.mark.xfail)` 给某一组打标记 |
| 间接 | `indirect=True` 把参数喂给**同名 fixture** 而非直接传函数 |
| 叠加 | 两个 `parametrize` 叠加 = 笛卡尔积，注意爆炸 |

## 正例

```python
import pytest

@pytest.mark.parametrize(
    "amount,rate,expected",
    [
        pytest.param(100, 0.5, 50, id="half-off"),
        pytest.param(100, 0.0, 100, id="no-discount"),
        pytest.param(100, 1.0, 0, id="free"),
    ],
)
def test_apply_discount(amount, rate, expected):
    assert apply_discount(amount, rate=rate) == expected
```

```python
# 间接参数化：参数先经 fixture 加工，再进测试
@pytest.fixture
def user(request):
    return User(role=request.param)     # request.param = 传入值

@pytest.mark.parametrize("user", ["admin", "guest"], indirect=True)
def test_permission(user):
    assert user.can_edit() is (user.role == "admin")
```

## 反例

```python
# ❌ 1. for 循环里多个 assert —— 第一条挂了后面不跑，报告里看不出哪组失败
def test_discounts():
    for amount, rate, expected in [(100, 0.5, 50), (100, 1.0, 0)]:
        assert apply_discount(amount, rate=rate) == expected

# ❌ 2. 不给 ids，复杂对象生成的用例名是 user0/user1，定位靠数
@pytest.mark.parametrize("user", [User("a"), User("b")])   # 名字不可读

# ✅ 给 id
@pytest.mark.parametrize("user", [User("a"), User("b")], ids=["admin", "guest"])
```

理由：循环里断言把 N 组并成 1 个用例，失败时既不知是哪组、又少跑后面的组；缺 `ids` 让 `-k` 过滤和报告定位全靠序号。

## 自检

- [ ] 多组输入用 `parametrize` 而非 for 循环里堆 assert？
- [ ] 给了 `ids` 或 `pytest.param(id=...)`，用例名可读？
- [ ] 需要预期失败的某组用 `pytest.param(marks=...)` 单独标记？
- [ ] 参数要经 fixture 加工时用了 `indirect=True`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`pytest-structure.md`](./pytest-structure.md) · [`fixture-usage.md`](./fixture-usage.md) · [`mock-patch.md`](./mock-patch.md)
