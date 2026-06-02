---
name: mybatis-n-plus-one
description: MyBatis N+1 查询问题 — association/collection 嵌套查询的 fetchType、嵌套 resultMap 一次 join vs 多次查、批量查替代循环单查。Use when 列表带关联数据变慢 / 循环里反复调 Mapper / 评审 N+1 隐患时。
parent: ./index.md
paths:
- '*.java'
- '*.xml'
triggers:
  keywords:
  - N+1 查询
  - fetchType
  - 嵌套 resultMap
  - association collection
  - 批量查询
  - 关联查询
effort: high
context: inline
version: '1.0'
---
# MyBatis · N+1 查询问题

> 本条只管「关联数据别一条条查」。结果映射本身怎么写见 [`xml-design.md`](./xml-design.md)；分页见 [`pagination.md`](./pagination.md)。

## 问题

查 1 个列表（1 次）后，为每行的关联数据各发 1 次查询（N 次）= **N+1 次往返**，行数一多即慢。常见于 `association`（一对一）/ `collection`（一对多）用了**嵌套 select** + `fetchType="eager"`。

## 规则

| 方案 | 用途 |
|------|------|
| 嵌套 `resultMap`（一条 join） | 列表稳定要带关联，**首选**：一次 join 全取回 |
| 嵌套 select + `fetchType="lazy"` | 关联数据**不一定用到**时延迟加载，避免无谓查询 |
| 批量查 + Java 内存组装 | 先查主表拿 id 集合，再 `IN` 一次查全部子表，按 key 分组挂载 |
| 禁止 | Java 循环里逐行调 Mapper（手写版 N+1） |

## 正例

```xml
<!-- ✅ 嵌套 resultMap：一条 join 取主+从，无 N+1 -->
<resultMap id="OrderWithItems" type="Order">
  <id column="o_id" property="id"/>
  <collection property="items" ofType="OrderItem">
    <id column="i_id" property="id"/>
    <result column="i_name" property="name"/>
  </collection>
</resultMap>
<select id="listWithItems" resultMap="OrderWithItems">
  select o.id o_id, i.id i_id, i.name i_name
  from orders o left join order_item i on i.order_id = o.id
</select>
```

```java
// ✅ 批量查替代循环单查：1 次 IN 查全部，再内存分组
List<Long> orderIds = orders.stream().map(Order::getId).toList();
Map<Long, List<OrderItem>> byOrder = itemMapper.listByOrderIds(orderIds)
        .stream().collect(groupingBy(OrderItem::getOrderId));
orders.forEach(o -> o.setItems(byOrder.getOrDefault(o.getId(), List.of())));
```

## 反例

```java
// ❌ 循环里逐行查 —— orders.size() 次额外查询，典型 N+1
for (Order o : orders) {
    o.setItems(itemMapper.listByOrderId(o.getId()));
}
```

理由：每行一次往返，网络与解析开销随行数线性放大；改成一次 join 或一次 `IN` 批量查，把 N+1 压到 1~2 次。

## 自检

- [ ] 列表稳定要带关联：用嵌套 `resultMap` 一条 join，没用 eager 嵌套 select？
- [ ] 关联可选：嵌套 select 设了 `fetchType="lazy"`？
- [ ] 没有在 Java 循环里逐行调 Mapper？
- [ ] 必须分步查时，用 `IN` 批量 + 内存分组，而非逐行查？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`xml-design.md`](./xml-design.md)（association/collection 的 resultMap 写法）
- 兄弟：[`dynamic-sql.md`](./dynamic-sql.md)（foreach 拼 IN 批量查）
- 兄弟：[`pagination.md`](./pagination.md)（分页列表带关联的组合场景）
