---
name: repository-usage-rule
description: Repository 只做 CRUD — find_by / save / delete，禁业务判断
parent: ./index.md
paths:
  - "backend/repositories/**/*.py"
  - "py/repositories/**/*.py"
  - "backend/services/**/*.py"
  - "py/services/**/*.py"
triggers:
  keywords: [Repository, Repo, DAO, find_by]
effort: medium
context: inline
version: "1.0"
---

# Repository · 使用规则

## 一句话定义

Repository = **持久化层的薄壳**。只翻译"业务对象 ↔ 数据库行"，不做任何业务决策。

## 必须满足的形态

```python
# py/repositories/presentation_repo.py
class PresentationRepo:
    async def find_by_id(self, pid: UUID) -> Presentation | None: ...
    async def find_by_owner(self, owner_id: UUID, *, limit: int = 20) -> list[Presentation]: ...
    async def save(self, p: Presentation) -> Presentation: ...
    async def delete(self, pid: UUID) -> None: ...
```

特征：方法名都是 `find_* / save / delete / count_*`，参数都是值类型或领域实体，返回也是领域实体或值。

## 禁止行为（命中 = 重构）

1. **禁在 Repo 写业务判断**
   ```python
   # ❌
   async def find_active_presentations(self, owner_id):
       items = await Presentation.filter(owner_id=owner_id)
       return [p for p in items if p.slide_count >= 5 and p.theme_id]  # 业务规则
   ```

2. **禁 Repo 调用 Repo**（除非父子聚合根）— 事务边界会模糊
3. **禁返回 dict / tuple** — 一律返回领域实体或值对象
4. **禁抛业务异常** — 找不到记录返回 `None`，由 Service 决定抛 `NotFoundError`

## Quill 落点

按 `module_path_map.md`：

- `backend/repositories/` — FastAPI 主后端（dashboard / outline_review / ppt_generator）
- `py/repositories/` — py 工作进程（textbook_data / database_setup 的种子脚本和 RQ worker）

## Service 与 Repo 的协作

```python
class PresentationService:
    def __init__(self, repo: PresentationRepo, theme_repo: ThemeRepo):
        self._repo = repo
        self._theme_repo = theme_repo

    async def create_for_outline(self, outline: Outline, theme_id: UUID) -> Presentation:
        # 1. 业务校验在 Service
        theme = await self._theme_repo.find_by_id(theme_id)
        if theme is None:
            raise ThemeNotFoundError(theme_id)   # 业务异常

        # 2. 领域对象创建
        p = Presentation.from_outline(outline, theme)

        # 3. 持久化交给 Repo
        return await self._repo.save(p)
```

## 自检

- [ ] Repo 方法名是 `find_* / save / delete / count_*`？
- [ ] Repo 不写 if 业务判断？
- [ ] Repo 不调用其他 Repo（除非聚合根）？
- [ ] Repo 不抛业务异常？
- [ ] Repo 返回领域实体而非 dict？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`no-business-in-repo.md`](./no-business-in-repo.md)
- 配套：[`../ddd-layering/repository-thin.md`](../ddd-layering/repository-thin.md) · [`../ddd-layering/service-orchestration.md`](../ddd-layering/service-orchestration.md)

