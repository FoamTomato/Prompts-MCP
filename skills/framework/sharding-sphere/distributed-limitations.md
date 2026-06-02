---
name: sharding-sphere-distributed-limitations
description: ShardingSphere 分布式限制 — 跨库 JOIN 不支持、跨片分页深翻页内存放大、聚合需中间件归并、跨片事务退化为分布式事务，各有规避手段。Use when 跨片查询报错或结果不对 / 深分页 OOM / 评审分片下 JOIN 聚合事务时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
triggers:
  keywords:
  - 分布式限制
  - 跨库 JOIN
  - 跨片分页
  - 跨片聚合
  - 分布式事务
  - 深分页
effort: high
context: inline
version: '1.0'
---
# ShardingSphere · 分布式限制

> 本条只管「分片后哪些操作受限及怎么绕」。绑定/广播表避 join 见 [`broadcast-binding-table.md`](./broadcast-binding-table.md)；读写一致见 [`read-write-split.md`](./read-write-split.md)。

## 四类限制与规避

| 操作 | 限制 | 规避 |
|------|------|------|
| **跨库 JOIN** | 不同分片键的表无法跨库 join | 广播表/绑定表落同片；冗余宽表；应用层分别查再内存组装 |
| **跨片分页** | `LIMIT m, n` 要从每片各取前 `m+n` 行再归并，深翻页内存暴涨 | 改键集分页（上次最大 id / 游标），避免大 offset |
| **跨片聚合** | `SUM/COUNT/AVG/GROUP BY/ORDER BY` 要查所有片再归并 | 中间件能归并但慢；高频聚合走预聚合表或 ES/数仓 |
| **跨片事务** | 一笔事务跨多片即退化为分布式事务，性能与一致性代价大 | 让一笔业务落单片；必须跨片用 XA 或 Seata（见 seata 模块） |

## 深分页为何爆内存

跨片 `LIMIT 100000, 10`：中间件无法只取某片第 10w 行，必须让**每个分片**都返回前 `100010` 行再全局排序取第 10w~10w+10 行。分片越多、offset 越大，拉回内存的行数成倍放大 → 慢且 OOM。

## 正例

```sql
-- ✅ 键集分页替代深 offset：带分片键 + 上次最大 id，命中单片不归并
SELECT * FROM t_order
WHERE user_id = 1001 AND id > #{lastMaxId}
ORDER BY id LIMIT 10;
```

```java
// ✅ 不同分片键的两表跨库：分别查再内存组装，不写跨库 JOIN
final List<OrderDO> orders = orderMapper.listByUser(userId);
final List<Long> pids = orders.stream().map(OrderDO::getProductId).toList();
final Map<Long, ProductDO> products = productMapper.listByIds(pids)   // 走商品分片
        .stream().collect(toMap(ProductDO::getId, p -> p));
orders.forEach(o -> o.setProduct(products.get(o.getProductId())));
```

## 反例

```sql
-- ❌ 跨片深分页：每个分片各回 1,000,010 行到内存归并 → 慢 + OOM
SELECT * FROM t_order ORDER BY create_time LIMIT 1000000, 10;

-- ❌ 不同分片键的两表直接跨库 JOIN —— 中间件无法路由
SELECT * FROM t_order o JOIN t_product p ON o.product_id = p.id;
```

理由：分片后单库视角的 JOIN/分页/聚合都变成「全片查 + 归并」，深 offset 把每片的扫描量按 offset 放大；跨片事务退化成分布式事务。能落单片就别跨片，必须跨片的聚合/事务交预聚合表与 Seata。

## 自检

- [ ] 跨片深分页改成了键集分页，没用大 offset 的 `LIMIT m,n`？
- [ ] 不同分片键的表没写跨库 JOIN，改广播/绑定表或应用层组装？
- [ ] 高频聚合走预聚合表 / ES，没靠中间件实时归并全片？
- [ ] 业务尽量落单片；确需跨片事务才上 Seata / XA？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`broadcast-binding-table.md`](./broadcast-binding-table.md)（用广播/绑定表消除跨库 JOIN）
- 兄弟：[`read-write-split.md`](./read-write-split.md)（读一致性）
- 分布式事务：[`../seata/index.md`](../seata/index.md)
