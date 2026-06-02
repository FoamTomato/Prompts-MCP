---
name: elasticsearch-sync-from-mysql
description: MySQL 数据同步到 Elasticsearch — Canal 订阅 binlog 准实时(推荐)、应用双写(强耦合易不一致)、Logstash JDBC 批量定时拉(有延迟)，按实时性与侵入性选型。Use when 把 MySQL 数据导入 ES / 维护索引与库一致 / 选同步方案时。
parent: ./index.md
paths:
- '*.java'
- '*.json'
triggers:
  keywords:
  - 数据同步
  - Canal binlog
  - 双写
  - Logstash
  - MySQL 同步 ES
effort: high
context: inline
version: '1.0'
---
# Elasticsearch · 与 MySQL 同步

> 本条只管「MySQL 的数据怎么进 ES、选哪种同步方式」。进 ES 后字段怎么定见 [`mapping-design.md`](./mapping-design.md)。

## 方案对比

| 方案 | 实时性 | 侵入性 | 适用 / 取舍 |
|------|--------|--------|------------|
| **Canal 订阅 binlog** | 准实时（秒级） | 低（不改业务代码） | **推荐**：伪装成 MySQL 从库读 binlog，解析变更投递 ES（常配 MQ 削峰） |
| **应用双写** | 实时 | 高（每处写库都要补写 ES） | 简单场景；DB 与 ES 非原子，需重试/补偿兜底一致性 |
| **Logstash JDBC** | 批量（分钟级延迟） | 低（无代码） | 定时增量拉取（按 `update_time`/自增 id 游标）；只能近实时，删除难捕获 |

通用要点：ES 同步本质是**最终一致**，不要当强一致用；**全量初始化用 `_bulk` 批量写**（别逐条），增量用上述方案；同步失败要有重试与对账（定时比对 MySQL 与 ES 计数/抽样）。

## 正例

```text
// ✅ Canal 准实时链路（低侵入、可削峰）
MySQL binlog → Canal Server → MQ(Kafka/RocketMQ) → 消费者解析 → ES _bulk 写入
              （消费幂等：按主键 _id 覆盖写，重复消费结果一致）
```

```json
// ✅ 全量/批量初始化走 _bulk，一次多条，别逐条 index
POST /_bulk
{ "index": { "_index": "product", "_id": "1001" } }
{ "name": "无线耳机", "status": "ON_SALE" }
{ "index": { "_index": "product", "_id": "1002" } }
{ "name": "蓝牙音箱", "status": "OFF" }
```

## 反例

```text
// ❌ 业务代码里写完 MySQL 紧接着同步调用写 ES，且无失败兜底
save(po);                 // 写库成功
esClient.index(doc);      // 这步抛异常 → DB 有、ES 没有，永久不一致且无人发现
// 双写至少要：异步重试 + 失败入死信 + 定时对账；强一致诉求别用 ES 兜
```

理由：DB 与 ES 是两套存储，无法在一个事务里原子提交；裸双写一旦后半步失败就静默不一致。Canal 走 binlog 天然在 DB 提交后才有事件，配 MQ 重试更稳，且不侵入业务。

## 自检

- [ ] 同步方案与实时性诉求匹配（准实时→Canal / 可延迟→Logstash）？
- [ ] 没把 ES 当强一致存储，承认最终一致并有对账兜底？
- [ ] 全量/批量同步走 `_bulk`，没逐条 index？
- [ ] 双写/消费按主键 `_id` 幂等覆盖，重复同步结果一致？
- [ ] 同步失败有重试 + 死信，不静默吞掉？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mapping-design.md`](./mapping-design.md)（同步进来的字段类型怎么定）
