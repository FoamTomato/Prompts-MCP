---
name: framework-mapstruct-index
description: MapStruct 对象映射四件事 — Mapper 接口定义 / 字段映射 / 映射策略 / 反模式。Use when 写 MapStruct Mapper / 做 DO-DTO-VO 转换 / 评审对象映射的 PR 时。
parent: ../index.md
children:
  - { name: mapstruct-mapper-definition, path: mapper-definition.md, tag: skill, note: "@Mapper(componentModel=spring) 接口定义与注入" }
  - { name: mapstruct-field-mapping, path: field-mapping.md, tag: skill, note: "@Mapping 字段映射：source/target、嵌套、表达式、日期格式" }
  - { name: mapstruct-mapping-strategy, path: mapping-strategy.md, tag: skill, note: "unmappedTargetPolicy/空值策略/@Named 自定义转换" }
  - { name: mapstruct-anti-patterns, path: anti-patterns.md, tag: skill, note: 别用 BeanUtils 反射拷贝、别手写 getter/setter、枚举映射 }
when_to_descend: 用 MapStruct 写 / 评审对象映射 Mapper 时
---

# MapStruct · 子项索引

MapStruct 对象映射拆成四个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 新建一个 Mapper 接口、让它能被 Spring 注入 | [mapper-definition](mapper-definition.md) |
| 字段名对不上 / 要映射嵌套属性 / 多源参数 / 表达式 / 日期格式 | [field-mapping](field-mapping.md) |
| 想强制显式映射防漏字段、处理 null、写自定义类型转换 | [mapping-strategy](mapping-strategy.md) |
| 在纠结要不要用 BeanUtils / 手写搬运 / 枚举怎么映射 | [anti-patterns](anti-patterns.md) |

> 「为什么用 MapStruct 而不是 BeanUtils」的拷贝选型见 [`../../lang/java/utils/bean-copy.md`](../../lang/java/utils/bean-copy.md)。
