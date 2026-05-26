---
name: tortoise-model-pattern
description: Tortoise Model 类标准模板 — Meta.table + auto_now/auto_now_add。Use when 写
  Python 后端代码 / 评审涉及 `model-class-pattern` 的 PR。
parent: ./index.md
paths:
- backend/models/**/*.py
- py/models/**/*.py
triggers:
  keywords:
  - Tortoise
  - Model
  - fields.
  - Meta
  - 类标准模板
effort: medium
context: inline
version: '1.0'
---
# Tortoise · Model 类模板

## 标准结构

```python
# py/models/referral.py
from tortoise import fields
from tortoise.models import Model
from models.base import TimestampMixin

class Referral(TimestampMixin, Model):
    """邀请关系（一对一：邀请人 → 被邀请人）"""

    id = fields.UUIDField(pk=True)
    inviter_session_id = fields.UUIDField(index=True)
    invitee_session_id = fields.UUIDField(unique=True)
    invite_code = fields.CharField(max_length=16, index=True)

    class Meta:
        table = "referrals"
        unique_together = (("inviter_session_id", "invitee_session_id"),)

    def __str__(self) -> str:
        return f"<Referral {self.invite_code}>"
```

## TimestampMixin

```python
# py/models/base.py
from tortoise import fields

class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
```

## 字段类型对照

| Tortoise | SQL（MySQL 8） |
|----------|--------------|
| `IntField(pk=True, generated=True)` | INT AUTO_INCREMENT PRIMARY KEY |
| `UUIDField(pk=True)` | CHAR(36) PRIMARY KEY |
| `CharField(max_length=N)` | VARCHAR(N) |
| `TextField()` | TEXT |
| `JSONField()` | JSON |
| `DatetimeField(auto_now_add=True)` | DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6) |
| `BooleanField(default=False)` | TINYINT(1) DEFAULT 0 |
| `DecimalField(max_digits=10, decimal_places=2)` | DECIMAL(10,2) |
| `ForeignKeyField("models.User", related_name="orders")` | INT/UUID + FK |
| `ManyToManyField("models.Tag", related_name="textbooks")` | 自动建中间表 |

## Meta 选项

```python
class Meta:
    table = "snake_case_name"            # 显式表名
    unique_together = (("a", "b"),)      # 多字段唯一
    indexes = (("a", "b"),)              # 联合索引
    ordering = ["-created_at"]            # 默认排序
```

## 关系

```python
# 1:N
class Slide(Model):
    presentation = fields.ForeignKeyField(
        "models.Presentation",
        related_name="slides",
        on_delete=fields.CASCADE,
    )

# 反向访问
p = await Presentation.get(id=pid).prefetch_related("slides")
for s in p.slides: ...

# N:M
class Tag(Model):
    textbooks = fields.ManyToManyField("models.Textbook", related_name="tags")
```

## 注册到 TORTOISE_ORM

```python
TORTOISE_ORM = {
    "connections": {"default": settings.database_url},
    "apps": {
        "models": {
            "models": [
                "models.session", "models.textbook", "models.referral",
                # ...
                "aerich.models",    # 必须 — Aerich 自己用
            ],
            "default_connection": "default",
        },
    },
}
```

## 查询模板

```python
# 单条
brand = await Textbook.filter(id=tid).first()

# 批量（防 N+1）
items = await Textbook.filter(id__in=id_list).all()
item_map = {i.id: i for i in items}

# 条件 + 排序 + 分页
results = await Textbook.filter(subject="math").order_by("-created_at").offset(0).limit(20)

# 存在性检查
exists = await Textbook.filter(id=tid).exists()

# 创建
record = await Textbook.create(name="...", subject="math")

# 批量创建
records = [Textbook(name=n) for n in names]
await Textbook.bulk_create(records)

# 更新
await Textbook.filter(id=tid).update(name="new")

# 仅取部分字段（节省内存）
names = await Textbook.filter(...).values_list("name", flat=True)
```

## 自检

- [ ] 继承 `TimestampMixin` + `Model`？
- [ ] `Meta.table` 显式 snake_case？
- [ ] 索引字段加 `index=True`？
- [ ] 外键明确 `on_delete`？
- [ ] 新增 Model 后追加到 `TORTOISE_ORM.models`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`transaction-context.md`](./transaction-context.md)
- 配套：[`../../lang/sql/ddl/tortoise-model-template.md`](../../lang/sql/ddl/tortoise-model-template.md)

