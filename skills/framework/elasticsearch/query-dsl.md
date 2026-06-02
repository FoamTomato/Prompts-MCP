---
name: elasticsearch-query-dsl
description: Elasticsearch bool 复合查询 DSL — must 算分且必须、should 可选加分、filter 必须但不算分可缓存、must_not 排除，精确条件放 filter 而非 must。Use when 写多条件检索 / 组合过滤与全文检索 / 优化查询性能时。
parent: ./index.md
paths:
- '*.json'
- '*.java'
triggers:
  keywords:
  - 复合查询
  - bool query
  - filter 过滤
  - must should
  - 相关性算分
effort: high
context: inline
version: '1.0'
---
# Elasticsearch · bool 复合查询 DSL

> 本条只管「多条件怎么组合、什么放算分什么放过滤」。聚合统计见 [`aggregation.md`](./aggregation.md)；翻页见 [`deep-paging.md`](./deep-paging.md)。

## 规则

`bool` 把多个子句组合，四个子句各司其职：

| 子句 | 是否必须 | 是否算分(_score) | 用途 |
|------|---------|-----------------|------|
| `must` | 是 | **算分** | 全文相关性检索（`match` 标题/正文） |
| `should` | 可选 | **算分** | 命中加分（择优排序）；无 must 时至少命中 1 个 |
| `filter` | 是 | **不算分、可缓存** | 精确/范围过滤（状态、分类、时间区间） |
| `must_not` | 是 | 不算分 | 排除（已删除、黑名单） |

核心原则：**不需要算分的精确条件一律放 `filter`**——它不参与相关性计算，结果可被 filter cache 缓存，比放 `must` 快得多。只有真正要影响相关性排序的全文检索才放 `must`/`should`。

## 正例

```json
{
  "query": {
    "bool": {
      "must":   [ { "match": { "title": "无线耳机" } } ],
      "filter": [
        { "term":  { "status": "ON_SALE" } },
        { "range": { "price": { "gte": 100, "lte": 500 } } }
      ],
      "must_not": [ { "term": { "deleted": true } } ],
      "should": [ { "term": { "brand": "SONY" } } ]
    }
  }
}
```

## 反例

```json
// ❌ 把精确过滤塞进 must —— 每条都参与算分、无法缓存，慢且 _score 被噪声污染
{ "query": { "bool": { "must": [
    { "match": { "title": "无线耳机" } },
    { "term":  { "status": "ON_SALE" } },   // 应进 filter
    { "range": { "price": { "gte": 100 } } } // 应进 filter
] } } }
```

理由：`status`/`price` 是「是否满足」的布尔判断，不该影响相关性排序；放 `filter` 后 ES 跳过算分并缓存 bitset，重复查询直接命中缓存。放 `must` 既白白算分又每次重算。

## 自检

- [ ] 精确匹配 / 范围 / 排除条件都放在 `filter` / `must_not`，没塞进 `must`？
- [ ] 只有要影响相关性排序的全文检索才用 `must` / `should`？
- [ ] 纯过滤场景（不需要 _score）整体用 `filter`，没用 `must`？
- [ ] `term` 过滤的是 `keyword` 字段而非被分词的 `text`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mapping-design.md`](./mapping-design.md)（filter 用 keyword、match 用 text）
- 兄弟：[`analyzer-ik.md`](./analyzer-ik.md)（match 检索依赖的分词器）
- 兄弟：[`deep-paging.md`](./deep-paging.md)（查询结果翻页）
