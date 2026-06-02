---
name: elasticsearch-aggregation
description: Elasticsearch 聚合分析 — 桶聚合 terms 分组、date_histogram 时间分桶、metrics 指标，聚合字段须 keyword/数值/date。Use when 做分组统计 / 时间趋势分析 / 计算指标或去重计数时。
parent: ./index.md
paths:
- '*.json'
- '*.java'
triggers:
  keywords:
  - 聚合分析
  - terms 聚合
  - date_histogram
  - metrics 指标
  - 分组统计
effort: high
context: inline
version: '1.0'
---
# Elasticsearch · 聚合分析

> 本条只管「怎么做统计聚合」。聚合字段为什么要 keyword 见 [`mapping-design.md`](./mapping-design.md)；先过滤再聚合的查询部分见 [`query-dsl.md`](./query-dsl.md)。

## 规则

聚合分两类：**桶（bucket）** 把文档分组、**指标（metric）** 在桶内算数。

| 聚合 | 类型 | 用途 |
|------|------|------|
| `terms` | 桶 | 按字段值分组计数（如各状态的订单数）；字段须 `keyword`/数值 |
| `date_histogram` | 桶 | 按时间间隔（`calendar_interval: day/month`）分桶，做趋势 |
| `range` | 桶 | 按数值/日期区间分桶（价格段） |
| `sum`/`avg`/`min`/`max` | 指标 | 数值字段求和、均值、极值 |
| `cardinality` | 指标 | 去重计数（近似，省内存，海量场景代替 distinct） |
| `value_count` | 指标 | 有值文档计数 |

要点：桶里可**嵌套子聚合**（先 terms 分组、组内再 avg）；`terms` 默认只返回 top 10，要全量调 `size`；纯统计设 `"size": 0` 不返回命中文档，省传输。

## 正例

```json
{
  "size": 0,
  "query": { "bool": { "filter": [ { "range": { "createdAt": { "gte": "now-30d/d" } } } ] } },
  "aggs": {
    "by_status": {
      "terms": { "field": "status", "size": 20 },
      "aggs": { "avg_amount": { "avg": { "field": "amount" } } }
    },
    "daily": {
      "date_histogram": { "field": "createdAt", "calendar_interval": "day" },
      "aggs": { "uv": { "cardinality": { "field": "userId" } } }
    }
  }
}
```

## 反例

```json
// ❌ 对 text 字段做 terms 聚合 —— 分词后按词条分组，结果是碎词不是原值，且需 fielddata 吃内存
{ "aggs": { "by_title": { "terms": { "field": "title" } } } }

// ❌ 只为统计却不设 size:0 —— 默认带回 10 条命中文档，浪费传输
{ "aggs": { "by_status": { "terms": { "field": "status" } } } }
```

理由：聚合作用在 doc_values 上，`text` 没有 doc_values（要 fielddata，极耗堆内存），且分词后分组无意义；应聚合 `keyword` 子字段。纯报表查询设 `size: 0` 跳过命中文档。

## 自检

- [ ] 聚合的字段是 `keyword` / 数值 / `date`，不是分词的 `text`？
- [ ] 纯统计场景设了 `"size": 0`，不返回命中文档？
- [ ] 去重计数用 `cardinality`（近似省内存）而非把数据全拉回来 distinct？
- [ ] `terms` 需要全量时显式调大 `size`，没被默认 top 10 截断？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mapping-design.md`](./mapping-design.md)（聚合字段须 keyword/数值/date）
- 兄弟：[`query-dsl.md`](./query-dsl.md)（聚合前用 filter 缩小范围）
