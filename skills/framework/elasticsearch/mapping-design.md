---
name: elasticsearch-mapping-design
description: Elasticsearch Mapping 字段类型设计 — text 用于分词全文检索、keyword 用于精确匹配/聚合/排序，避免全 text，长文用 text+keyword 子字段。Use when 建 ES 索引 / 定字段类型 / 排查字段不能聚合或排序时。
parent: ./index.md
paths:
- '*.json'
- '*.java'
triggers:
  keywords:
  - 字段类型
  - Mapping 设计
  - text vs keyword
  - keyword
  - 聚合排序字段
effort: medium
context: inline
version: '1.0'
---
# Elasticsearch · Mapping 字段类型设计

> 本条只管「字段定成什么类型」。中文分词器选哪个见 [`analyzer-ik.md`](./analyzer-ik.md)；定好类型后怎么聚合见 [`aggregation.md`](./aggregation.md)。

## 规则

| 字段用途 | 选什么类型 | 原因 |
|---------|-----------|------|
| 要全文检索（标题、正文、商品名） | `text` | 建索引时分词，支持 `match` 模糊/相关性检索 |
| 要精确匹配 / 聚合 / 排序（状态、标签、枚举、ID） | `keyword` | 不分词，整体作为 term，可做 `term`/聚合/`sort` |
| 既要检索又要聚合的字段（如标题） | `text` + `fields.keyword` 子字段 | `field` 用于检索，`field.keyword` 用于聚合排序 |
| 数值范围 / 日期范围 | `integer`/`long`/`double`/`date` | 支持 `range` 查询与 `date_histogram` |
| 不检索只存储返回 | `text` 配 `"index": false` | 省索引空间 |
| 关闭动态映射 | 索引设 `"dynamic": "strict"` | 防止脏字段自动建错类型 |

`text` 字段**默认不能直接聚合/排序**（需开 `fielddata`，极耗内存，禁用）。要聚合排序就上 `keyword` 或子字段。

## 正例

```json
{
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "title":  { "type": "text", "analyzer": "ik_max_word",
                  "fields": { "keyword": { "type": "keyword", "ignore_above": 256 } } },
      "status": { "type": "keyword" },
      "price":  { "type": "double" },
      "createdAt": { "type": "date", "format": "yyyy-MM-dd HH:mm:ss" }
    }
  }
}
```

## 反例

```json
// ❌ 把状态、ID 也定成 text —— 既被分词破坏精确匹配，又无法聚合/排序
{ "properties": {
    "status": { "type": "text" },   // term 查不准、聚合直接报错
    "userId": { "type": "text" }    // 想按 userId 聚合时被迫开 fielddata，吃爆内存
} }
```

理由：`text` 会分词，`status` 被拆后精确过滤失效，且聚合/排序需 `fielddata` 占大量堆内存；这类字段本质是「值」不是「文档」，应当 `keyword`。

## 自检

- [ ] 要分词检索的才用 `text`，状态/ID/枚举/标签一律 `keyword`？
- [ ] 既检索又聚合的字段配了 `text` + `keyword` 子字段？
- [ ] 没有为了聚合 `text` 字段去开 `fielddata`？
- [ ] 生产索引设了 `dynamic: strict`，避免脏字段自动建错类型？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`analyzer-ik.md`](./analyzer-ik.md)（text 字段的中文分词器选择）
- 兄弟：[`aggregation.md`](./aggregation.md)（keyword/date 字段怎么聚合）
- 兄弟：[`query-dsl.md`](./query-dsl.md)（keyword 走 filter、text 走 must 的检索）
