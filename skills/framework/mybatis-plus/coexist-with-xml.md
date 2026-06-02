---
name: mybatis-plus-coexist-with-xml
description: MyBatis-Plus 与原生 MyBatis 分工 — 简单 CRUD 走 BaseMapper/Wrapper，多表关联与复杂业务 SQL 走 XML，反对 Wrapper 拼复杂 SQL。Use when 纠结 SQL 走 Wrapper 还是 XML / 评审 MP 与 XML 混用时。
parent: ./index.md
paths:
- '*.java'
- '*.xml'
triggers:
  keywords:
  - 共存
  - 复杂查询
  - BaseMapper
  - Wrapper 拼 SQL
  - 多表关联
  - 走 XML 还是 Wrapper
effort: medium
context: inline
version: '1.0'
---
# MyBatis-Plus · 与原生 MyBatis XML 共存

> 本条只管「哪条 SQL 走 Wrapper、哪条走 XML」。Wrapper 本身怎么写见 [`lambda-wrapper.md`](./lambda-wrapper.md)；XML 怎么设计见 [`../mybatis/xml-design.md`](../mybatis/xml-design.md)。

## 规则

| 场景 | 走哪条路 |
|------|---------|
| 单表增删改查、简单等值/范围条件 | `BaseMapper` + `LambdaQueryWrapper`，零 SQL |
| 多表 join、子查询、聚合、复杂业务规则 | **手写 XML**（Mapper 继承 `BaseMapper` 同时挂 XML） |
| 动态拼接很重的查询 | XML 的 `<if>/<where>/<foreach>`，比 Wrapper 链式可读 |
| 性能敏感 / 要看懂执行计划的 SQL | XML，SQL 显式可控、可 EXPLAIN |
| 共存方式 | 同一 Mapper 既继承 `BaseMapper<T>` 又写 XML 自定义方法，互不冲突 |

## 正例

```java
// ✅ Mapper 同时拥有 MP 增强 + 自定义 XML 方法
@Mapper
public interface OrderMapper extends BaseMapper<Order> {
    // 复杂多表统计：走 XML，SQL 显式可读可优化
    List<OrderStatVO> statByDept(@Param("deptId") Long deptId);
}
// 简单 CRUD 直接用继承来的 selectById / selectList(wrapper)，不写一行 SQL
```

## 反例

```java
// ❌ 用 Wrapper 拼复杂业务 SQL —— 链式越堆越长，读不懂、改不动、没法 EXPLAIN
List<Order> list = orderMapper.selectList(Wrappers.<Order>lambdaQuery()
        .eq(Order::getStatus, 1)
        .ge(Order::getAmount, min)
        .le(Order::getAmount, max)
        .in(Order::getDeptId, deptIds)
        .and(w -> w.like(Order::getRemark, kw).or().eq(Order::getVip, 1))
        .last("HAVING COUNT(*) > 1 ORDER BY amount DESC LIMIT 10"));   // 已失控
```

理由：Wrapper 擅长单表简单条件；一旦涉及 join/聚合/`.last()` 拼裸 SQL，可读性和可维护性都崩，这类逻辑天生属于 XML。

## 自检

- [ ] 单表简单 CRUD 用了 BaseMapper + Wrapper，没多余 XML？
- [ ] 多表/聚合/复杂业务 SQL 走了 XML，没硬塞进 Wrapper？
- [ ] 没有靠 `.last()` 往 Wrapper 里塞裸 SQL 片段？
- [ ] 同一 Mapper 共存时，继承 `BaseMapper` 与 XML 自定义方法各司其职？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`lambda-wrapper.md`](./lambda-wrapper.md)（简单条件用 Wrapper 怎么写对）
- XML 设计：[`../mybatis/xml-design.md`](../mybatis/xml-design.md)（复杂 SQL 的 XML 怎么写）
- 动态 SQL：[`../mybatis/dynamic-sql.md`](../mybatis/dynamic-sql.md)（XML 里 if/where/foreach）
