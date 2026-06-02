---
name: framework-mybatis-plus-index
description: MyBatis-Plus 增强用法 6 项 — 条件构造器 / 分页插件 / 逻辑删除 / 乐观锁 / 自动填充 / 与 XML 共存。Use when 用 BaseMapper 写 CRUD / 配分页插件 / 加逻辑删除或乐观锁 / 评审 MP 持久层时。
parent: ../index.md
children:
  - { name: mybatis-plus-lambda-wrapper, path: lambda-wrapper.md, tag: skill, note: "LambdaQueryWrapper 类型安全，方法引用代替字段名硬编码" }
  - { name: mybatis-plus-pagination, path: pagination.md, tag: skill, note: "PaginationInnerInterceptor 必须配置，否则 page 不生效" }
  - { name: mybatis-plus-logic-delete, path: logic-delete.md, tag: skill, note: "@TableLogic 逻辑删除，查询自动加 deleted=0" }
  - { name: mybatis-plus-optimistic-lock, path: optimistic-lock.md, tag: skill, note: "@Version 乐观锁，更新自动加版本号条件" }
  - { name: mybatis-plus-auto-fill, path: auto-fill.md, tag: skill, note: "MetaObjectHandler 自动填充 createTime/updateTime" }
  - { name: mybatis-plus-coexist-with-xml, path: coexist-with-xml.md, tag: skill, note: "简单 CRUD 走 BaseMapper，复杂 SQL 走 XML" }
when_to_descend: 用 MyBatis-Plus 的 BaseMapper / Wrapper / IService，配分页插件，加逻辑删除、乐观锁、自动填充，或纠结 MP 与原生 XML 怎么分工
---

# MyBatis-Plus · 子项索引

MyBatis-Plus 在原生 MyBatis 上增强，拆成 6 个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 拼查询条件（怕字段名写错、想类型安全） | [lambda-wrapper](lambda-wrapper.md) |
| 做分页发现 `page` 不生效 / total 永远 0 | [pagination](pagination.md) |
| 要软删除（删除只改标记不真删行） | [logic-delete](logic-delete.md) |
| 并发更新同一行要防覆盖（防丢失更新） | [optimistic-lock](optimistic-lock.md) |
| 想自动写 createTime/updateTime，不在业务里手填 | [auto-fill](auto-fill.md) |
| 纠结这条 SQL 走 Wrapper 还是写 XML | [coexist-with-xml](coexist-with-xml.md) |

> 原生 MyBatis 的 Mapper 接口 / XML 设计 / 动态 SQL / 防注入见 [`../mybatis/index.md`](../mybatis/index.md)。
