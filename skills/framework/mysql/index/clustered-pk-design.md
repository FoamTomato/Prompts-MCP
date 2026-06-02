---
name: mysql-clustered-pk-design
description: InnoDB 聚簇索引与主键选型 — 主键即数据物理顺序，宜用自增 BIGINT，忌用 UUID/随机串/业务字段做 PK（页分裂 + 二级索引膨胀）。Use when 建表定主键 / 评审用 UUID 当主键 / 排查写入页分裂时。
parent: ./index.md
paths:
- '*.sql'
- '*.java'
- '*.xml'
triggers:
  keywords:
  - 聚簇索引
  - 主键选型
  - clustered index
  - primary key
  - 自增主键
  - UUID 主键
  - 页分裂
  - page split
effort: high
context: inline
version: '1.0'
---
# MySQL · 聚簇索引与主键选型

> 本条只管「主键该用什么类型、为什么」。分布式场景主键生成算法见 [`../ops/distributed-id.md`](../ops/distributed-id.md)；二级索引最左前缀见 [`leftmost-prefix.md`](./leftmost-prefix.md)。

## 核心机制

InnoDB 表数据**按主键物理有序存放**（主键即聚簇索引，叶子节点就是整行数据）。推论：

- **二级索引的叶子存的是主键值**，不是行指针 → 主键越长，每个二级索引越占空间。
- 插入时若主键无序，会插到已满数据页中间 → **页分裂**、碎片、写放大。

## 规则

| 项 | 约定 | 原因 |
|----|------|------|
| 默认主键 | `BIGINT AUTO_INCREMENT` | 单调递增，永远追加到末页，无页分裂 |
| 禁做主键 | UUID / 随机字符串 / MD5 | 随机分布 → 频繁页分裂 + 二级索引膨胀 |
| 禁做主键 | 可变的业务字段（手机号、订单号） | 业务变更即改主键，牵动全部二级索引 |
| 必须有主键 | 每张 InnoDB 表显式建 PK | 无 PK 时 InnoDB 用隐藏 6 字节 rowid，不可控 |
| 主键宽度 | 尽量窄 | 二级索引都携带主键值，窄主键省全表空间 |

## 正例

```sql
-- ✅ 自增 BIGINT 主键，业务唯一键单独建唯一索引
CREATE TABLE orders (
  id          BIGINT      NOT NULL AUTO_INCREMENT,
  order_no    VARCHAR(32) NOT NULL,
  user_id     BIGINT      NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uk_order_no (order_no)   -- 业务唯一性靠唯一键，不靠主键
) ENGINE=InnoDB;
```

## 反例

```sql
-- ❌ UUID 当主键：写入随机页分裂，二级索引每条都背 36 字节
CREATE TABLE events (
  id   CHAR(36) NOT NULL,   -- 随机 → 页分裂 + 膨胀
  PRIMARY KEY (id)
);

-- ❌ 用业务订单号当主键：订单号规则一变就得迁全表
PRIMARY KEY (order_no)
```

## 例外

- **真需要分布式有序 ID**：用「号段模式」或「雪花算法」生成的 `BIGINT`（仍单调递增），见 [`../ops/distributed-id.md`](../ops/distributed-id.md)，**不要**退回 UUID。
- 必须存 UUID 时，作普通列 + 唯一索引，主键仍用自增。

## 自检

- [ ] 主键是 `BIGINT AUTO_INCREMENT`（或单调递增的分布式 ID）？
- [ ] 没有用 UUID / 随机串 / 可变业务字段做主键？
- [ ] 业务唯一性用 `UNIQUE KEY` 而非主键承载？
- [ ] 主键尽量窄，避免拖累所有二级索引？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`leftmost-prefix.md`](./leftmost-prefix.md)（二级索引）
- 运维：[`../ops/distributed-id.md`](../ops/distributed-id.md)（分布式有序 ID 生成）
