---
name: py-test-fixture-usage
description: pytest fixture 作用域、yield 清理、conftest.py 共享与 autouse。Use when 准备测试数据 / 共享 client / 写 teardown / 放 conftest。
parent: ./index.md
paths:
- '*.py'
- 'py/**/*.py'
- 'tests/**/*.py'
triggers:
  keywords:
  - 夹具
  - 作用域
  - fixture
  - yield 清理
  - conftest
  - autouse
effort: medium
context: inline
version: '1.0'
---
# Python · pytest fixture 用法

## 规则

| 项 | 规则 |
|----|------|
| 声明 | `@pytest.fixture` 装饰函数，测试把名字写进参数即注入 |
| 清理 | 用 `yield` 分隔 setup / teardown，**优先于** `addfinalizer` |
| 作用域 | `function`(默认) / `class` / `module` / `package` / `session`，按复用代价选最窄 |
| 共享 | 跨文件共享的 fixture 放 `conftest.py`，**不要** import |
| autouse | `autouse=True` 仅用于无参副作用（清缓存/设时区），不要滥用 |

## 正例

```python
# tests/conftest.py —— 跨文件自动可见，无需导入
import pytest

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine("sqlite:///:memory:")
    yield engine                    # yield 前是 setup
    engine.dispose()                # yield 后是 teardown，异常也会执行

@pytest.fixture
def db_session(db_engine):          # fixture 可依赖 fixture
    conn = db_engine.connect()
    txn = conn.begin()
    yield Session(bind=conn)
    txn.rollback()                  # 每个用例回滚，互不污染
    conn.close()

@pytest.fixture(autouse=True)
def _reset_cache():
    cache.clear()                   # 每个用例前自动清，无需在参数里写
    yield
```

```python
# tests/test_orders.py
def test_create_order(db_session):  # 参数名 = fixture 名，自动注入
    repo = OrderRepo(db_session)
    assert repo.create(amount=10).id is not None
```

## 反例

```python
# ❌ 1. session 作用域的可变状态被多个用例共享 —— 测试间串味
@pytest.fixture(scope="session")
def user():
    return User(name="a")           # 一个用例改了 name，后续用例受影响

# ✅ 默认 function 作用域，每个用例拿全新对象
@pytest.fixture
def user():
    return User(name="a")

# ❌ 2. 用 return 而非 yield 做清理 —— teardown 根本不会跑
@pytest.fixture
def tmp_file():
    f = open("x", "w")
    return f                        # 文件永不关闭

# ❌ 3. 把 conftest 的 fixture 直接 import —— 破坏发现机制
from conftest import db_session     # 反模式
```

## 自检

- [ ] 有副作用/外部资源的 fixture 用 `yield` 写了 teardown？
- [ ] 作用域选了能满足复用的**最窄**那个，避免状态串味？
- [ ] 跨文件共享放进 `conftest.py` 而非 import？
- [ ] `autouse` 只用于无参副作用，没拿来传数据？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`pytest-structure.md`](./pytest-structure.md) · [`parametrize.md`](./parametrize.md) · [`mock-patch.md`](./mock-patch.md)
