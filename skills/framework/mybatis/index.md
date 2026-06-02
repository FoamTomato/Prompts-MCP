---
name: framework-mybatis-index
description: MyBatis + Mapper XML 设计规范 6 项 — 接口约定 / XML 设计 / 动态 SQL / 注入安全 / 分页 / N+1。Use when 写 Mapper 接口或 XML / 排查 SQL 注入与慢查询 / 评审 MyBatis 持久层 PR 时。
parent: ../index.md
children:
  - { name: mybatis-mapper-interface, path: mapper-interface.md, tag: skill, note: "Mapper 接口：@Mapper、方法名、@Param、返回类型" }
  - { name: mybatis-xml-design, path: xml-design.md, tag: skill, note: "XML 设计：namespace、resultMap 显式映射、sql 片段复用" }
  - { name: mybatis-dynamic-sql, path: dynamic-sql.md, tag: skill, note: "动态 SQL：if / where / foreach / choose" }
  - { name: mybatis-sql-injection-safety, path: sql-injection-safety.md, tag: skill, note: "安全红线：#{} 预编译 vs ${} 白名单" }
  - { name: mybatis-pagination, path: pagination.md, tag: skill, note: PageHelper / IPage 物理分页，禁内存分页 }
  - { name: mybatis-n-plus-one, path: n-plus-one.md, tag: skill, note: N+1 查询：fetchType、嵌套 resultMap、批量查 }
when_to_descend: 写 / 评审 MyBatis Mapper 接口、Mapper XML、动态 SQL、分页或关联查询
---

# MyBatis · 子项索引

MyBatis 持久层拆成 6 个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 写 Mapper 接口（注解扫描、方法名、多参数、返回类型） | [mapper-interface](mapper-interface.md) |
| 写 Mapper XML（namespace、resultMap、sql 片段复用） | [xml-design](xml-design.md) |
| 写动态 SQL（条件拼接 / 批量 / 多分支） | [dynamic-sql](dynamic-sql.md) |
| 拼 SQL 时纠结用 `#{}` 还是 `${}`（防注入） | [sql-injection-safety](sql-injection-safety.md) |
| 做分页查询（物理分页 / count 优化） | [pagination](pagination.md) |
| 列表带关联数据、循环里反复查库（慢） | [n-plus-one](n-plus-one.md) |
