---
name: lang-python-typing-index
description: Python 类型注解规范
parent: ../index.md
children:
  - { name: strict-annotations, path: strict-annotations.md, tag: skill, note: 100% 函数签名注解 }
  - { name: pydantic-v2-field, path: pydantic-v2-field.md, tag: skill, note: Pydantic Field 必带 description }
  - { name: no-any, path: no-any.md, tag: skill, note: 禁 Any，用 Union / TypeVar }
  - { name: pep695-generics, path: pep695-generics.md, tag: skill, note: "PEP 695 新泛型 def f[T]/class C[T]/type" }
  - { name: protocol-structural, path: protocol-structural.md, tag: skill, note: Protocol 结构化子类型 + runtime_checkable }
  - { name: typeddict-literal, path: typeddict-literal.md, tag: skill, note: TypedDict/Literal/NewType/overload }
  - { name: type-narrowing, path: type-narrowing.md, tag: skill, note: "TypeGuard/TypeIs/Self/assert_never 窄化" }
  - { name: deferred-annotations, path: deferred-annotations.md, tag: skill, note: PEP 649/749 注解延迟求值（3.14） }
when_to_descend: 写新函数 / 泛型与协议 / 类型窄化 / Pydantic schema / 类型检查
---

# Typing · 子项索引

| 你在做什么 | 进哪个 |
|------|-------|
| 给函数加完整签名注解 | strict-annotations |
| 想用 Any 兜底（该避免） | no-any |
| 写泛型函数/类、定义类型别名 | pep695-generics |
| 按行为定义接口、解耦实现 | protocol-structural |
| 给 JSON/kwargs 字典、有限取值、ID 标类型 | typeddict-literal |
| 写类型守卫、链式返回 Self、穷尽检查 | type-narrowing |
| 处理前向引用、运行时读注解、升级 3.14 | deferred-annotations |
| 定义 Pydantic 模型字段 | pydantic-v2-field |
