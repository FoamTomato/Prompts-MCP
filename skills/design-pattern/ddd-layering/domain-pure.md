---
name: ddd-domain-pure
description: Domain 纯净 — 不依赖框架，封装业务规则。Use when 写 Python 后端代码 / 评审涉及 `domain-pure`
  的 PR。
parent: ./index.md
paths:
- backend/domain/**/*.py
- py/domain/**/*.py
triggers:
  keywords:
  - Domain
  - 值对象
  - 业务规则
effort: medium
context: inline
version: '1.0'
---
# DDD · Domain 纯净

## 规则

Domain 层封装核心业务规则，**不依赖任何基础设施**（DB / Redis / HTTP / LLM）。

## 必须满足

| 形态 | 例 |
|------|------|
| 仅 Python 内置 + Pydantic + 业务子类 | `class User(BaseModel): ...` |
| 不 import Tortoise / requests / redis | — |
| 不 import FastAPI / Flask | — |
| 不读环境变量 | — |
| 可在 pytest 内无外部依赖跑通 | — |

## 示例

```python
# py/domain/credits.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Credits:
    base: int           # 基础积分
    bonus: int          # 邀请奖励积分

    @property
    def total(self) -> int:
        return self.base + self.bonus

    def can_afford(self, cost: int) -> bool:
        return self.total >= cost

    def deduct(self, cost: int) -> "Credits":
        """扣减：优先扣 bonus，再扣 base"""
        if not self.can_afford(cost):
            raise InsufficientCredits(need=cost, have=self.total)

        remain = cost
        bonus_deduct = min(self.bonus, remain)
        remain -= bonus_deduct

        base_deduct = remain
        return Credits(base=self.base - base_deduct, bonus=self.bonus - bonus_deduct)


class InsufficientCredits(Exception):
    def __init__(self, need: int, have: int):
        self.need = need
        self.have = have
```

`Credits` 是纯领域对象。可以单测：

```python
def test_credits_deduct_bonus_first():
    c = Credits(base=5, bonus=3)
    result = c.deduct(2)
    assert result.bonus == 1   # 先扣 bonus
    assert result.base == 5

def test_credits_deduct_overflow():
    c = Credits(base=5, bonus=3)
    result = c.deduct(7)
    assert result.bonus == 0
    assert result.base == 1
```

无需 mock 任何东西。

## Service 使用

```python
class CreditsService:
    def __init__(self, repo: SessionRepo):
        self.repo = repo

    async def deduct_for_generation(self, session_id: str, cost: int) -> None:
        # 1. 加载领域对象
        session = await self.repo.find_or_raise(session_id)
        credits = Credits(base=session.base_credits, bonus=session.bonus_credits)

        # 2. 领域操作
        new_credits = credits.deduct(cost)   # 抛 InsufficientCredits 由 Service 翻译为 ApiException

        # 3. 持久化
        await self.repo.update_credits(session_id, base=new_credits.base, bonus=new_credits.bonus)
```

## 反例

```python
# ❌ Domain 里直接查 DB
@dataclass
class User:
    id: int

    async def get_orders(self):
        return await Order.filter(user_id=self.id).all()   # 依赖 Tortoise

# ✅ Domain 只描述数据 + 行为；持久化在 Repo
@dataclass
class User:
    id: int
    name: str

    def is_premium(self) -> bool: ...   # 业务规则

class UserService:
    async def get_orders(self, user: User) -> list[Order]:
        return await self.order_repo.find_by_user(user.id)
```

## Quill 现状

Quill 当前后端规模较小，**没有显式 `domain/` 目录**——业务规则散落在 Service 内。当业务复杂度上升（Credits / Referral 等含核心规则的领域）时再抽 `domain/`。

## 自检

- [ ] Domain 类不 import 任何 I/O 库？
- [ ] Domain 类可单测无需 mock？
- [ ] 领域异常用业务专有 Exception 子类？
- [ ] Service 通过 Repo 加载 → 调用 Domain 方法 → Repo 保存？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`controller-thin.md`](./controller-thin.md) · [`service-orchestration.md`](./service-orchestration.md) · [`repository-thin.md`](./repository-thin.md)

