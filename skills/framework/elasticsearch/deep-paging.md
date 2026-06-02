---
name: elasticsearch-deep-paging
description: Elasticsearch 深分页 — from+size 受 1 万限制且越深越慢，连续翻页用 search_after 游标，全量导出用 scroll/PIT。Use when 翻页深处报 result window 错误 / 分页越翻越慢 / 做大批量导出时。
parent: ./index.md
paths:
- '*.json'
- '*.java'
triggers:
  keywords:
  - 深分页
  - search_after
  - from size
  - 游标分页
  - max_result_window
effort: high
context: inline
version: '1.0'
---
# Elasticsearch · 深分页

> 本条只管「翻很深的页怎么办」。前几页正常分页随查询一起用 `from+size` 即可，见 [`query-dsl.md`](./query-dsl.md)。

## 问题

`from + size` 翻第 N 页时，每个分片要取回 `from+size` 条再汇总丢弃前面的，**越深越慢**且耗内存。ES 默认 `index.max_result_window = 10000`，**`from+size` 超过 1 万直接报 `Result window is too large`**。

## 规则

| 场景 | 方案 | 说明 |
|------|------|------|
| 浅分页（前几页，总深度 < 1 万） | `from + size` | 支持跳页，简单够用 |
| 连续往后翻（无限下拉、深翻页） | **`search_after`** | 带上次最后一条的 `sort` 值续翻，无深度上限、无大 offset 开销；**不能跳页** |
| 全量导出 / 跑批 | `scroll`（旧）或 **PIT + search_after**（推荐） | 一次性遍历全部数据，不适合实时分页 |
| 仅放大窗口 | 调大 `max_result_window` | ❌ 治标不治本，深 offset 仍慢且吃内存，不推荐 |

`search_after` 要求排序**唯一**（末尾加 `_id`/主键兜底），否则翻页会漏或重。

## 正例

```json
// ✅ search_after：排序须唯一（业务字段 + _id 兜底）
// 第一页
{ "size": 20, "sort": [ { "createdAt": "desc" }, { "_id": "asc" } ],
  "query": { "match_all": {} } }

// 下一页：把上一页最后一条的 sort 值原样填进 search_after
{ "size": 20, "sort": [ { "createdAt": "desc" }, { "_id": "asc" } ],
  "search_after": [ 1717200000000, "doc_8842" ],
  "query": { "match_all": {} } }
```

## 反例

```json
// ❌ 深 offset：第 1001 页报 Result window is too large（10000 上限），即便没报错也极慢
{ "from": 20000, "size": 20, "query": { "match_all": {} } }

// ❌ search_after 排序不唯一 —— 多条 createdAt 相同的文档在翻页边界会漏读或重复
{ "size": 20, "sort": [ { "createdAt": "desc" } ], "search_after": [ 1717200000000 ] }
```

理由：`from` 越大每分片要扫并丢弃的文档越多，10000 是安全阀；`search_after` 用「上次游标」定位，开销与页深无关。排序不唯一时相同值的文档边界不确定，必然漏/重。

## 自检

- [ ] 深翻页 / 无限下拉用 `search_after`，没用大 `from`？
- [ ] `search_after` 的排序带了唯一字段（如 `_id`）兜底？
- [ ] 没靠盲目调大 `max_result_window` 绕过问题？
- [ ] 全量导出用 PIT + search_after（或 scroll），没当实时分页用？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`query-dsl.md`](./query-dsl.md)（分页所基于的查询本身）
- 兄弟：[`aggregation.md`](./aggregation.md)（统计场景常可替代深翻页取数）
