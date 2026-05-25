---
name: ddd-repository-thin
description: Repository 薄 — 持久化转译，禁业务
parent: ./index.md
paths:
  - "backend/repositories/**/*.py"
  - "py/repositories/**/*.py"
triggers:
  keywords: [Repository, Repo, 持久化]
effort: medium
context: inline
version: "1.0"
---

# DDD · Repository 薄

## 规则

Repository 是**持久化转译层**。只做 ORM ↔ 领域对象的转换，不做业务判断。

## 方法签名

```python
class PresentationRepo:
    async def find_by_id(self, pid: UUID) -> Presentation | None: ...
    async def find_by_owner(
        self,
        owner_id: UUID,
        *,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Presentation]: ...
    async def save(self, p: Presentation) -> Presentation: ...
    async def delete(self, pid: UUID) -> None: ...
    async def count_by_owner(self, owner_id: UUID) -> int: ...
```

## 必须满足

| 规则 | 说明 |
|------|------|
| 方法名是 `find_* / save / delete / count_*` | 无业务动词（如 `submit` / `approve`） |
| 参数是值类型或领域实体 | 不接受 dict 或 ORM Model |
| 返回领域实体或值 | 不返回 ORM Model 暴露给 Service |
| 不调其他 Repo | 除非父子聚合根 |
| 不抛业务异常 | 找不到返回 None |

## ORM ↔ Domain 转换

```python
class PresentationRepo:
    async def find_by_id(self, pid: UUID) -> Presentation | None:
        row = await PresentationModel.filter(id=str(pid)).first()
        if not row:
            return None
        return self._to_domain(row)

    async def save(self, p: Presentation) -> Presentation:
        # 创建 or 更新
        if p.id is None:
            row = await PresentationModel.create(
                title=p.title,
                owner_id=str(p.owner_id),
                theme_id=str(p.theme_id) if p.theme_id else None,
            )
            return self._to_domain(row)
        else:
            await PresentationModel.filter(id=str(p.id)).update(
                title=p.title,
                theme_id=str(p.theme_id) if p.theme_id else None,
                updated_at=datetime.now(),
            )
            row = await PresentationModel.filter(id=str(p.id)).first()
            return self._to_domain(row)

    def _to_domain(self, row: PresentationModel) -> Presentation:
        return Presentation(
            id=UUID(row.id),
            title=row.title,
            owner_id=UUID(row.owner_id),
            theme_id=UUID(row.theme_id) if row.theme_id else None,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
```

## Quill 当前简化

Quill 后端规模小，**不强制 Domain ↔ ORM 转换**，可以让 Repo 直接返回 ORM Model（用 `Adapter` 在 Service 出口转 Pydantic）。

实际形态：

```python
# py/services/textbook.py — 直接用 Tortoise Model 当"领域对象"
async def list_textbooks_by_subject(subject: str) -> list[Textbook]:
    return await Textbook.filter(subject=subject).all()
```

当领域规则复杂时再升级为真正的 Domain 层。

## 反例（无论简化版还是完整版）

```python
# ❌ Repo 内业务判断
async def find_publishable_presentations(self, owner_id):
    rows = await Presentation.filter(owner_id=owner_id)
    return [r for r in rows if r.slide_count >= 5]   # 业务规则在 Repo

# ❌ Repo 返回 dict
async def find_by_id(self, pid):
    row = await Presentation.filter(id=pid).first()
    return row.__dict__   # 丢类型信息

# ❌ Repo 调其他 Repo
async def find_with_owner(self, pid):
    p = await Presentation.filter(id=pid).first()
    owner = await self.user_repo.find_by_id(p.owner_id)   # 跨 Repo 调用
    return p, owner
```

## 自检

- [ ] 方法名只有 `find_* / save / delete / count_*`？
- [ ] 不写业务判断？
- [ ] 返回领域实体（或 ORM Model 简化版）而非 dict？
- [ ] 不调其他 Repo？
- [ ] 找不到返回 None 而非抛异常？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`controller-thin.md`](./controller-thin.md) · [`service-orchestration.md`](./service-orchestration.md) · [`domain-pure.md`](./domain-pure.md)
- 配套：[`../repository/usage-rule.md`](../repository/usage-rule.md) · [`../repository/no-business-in-repo.md`](../repository/no-business-in-repo.md)

