---
name: elasticsearch-analyzer-ik
description: Elasticsearch 中文分词器 IK — 索引用 ik_max_word 细粒度多切词提召回，查询用 ik_smart 粗粒度保精度，避免默认 standard 单字切分。Use when 中文字段配分词 / 检索召回不准 / 索引与查询分词器选择时。
parent: ./index.md
paths:
- '*.json'
- '*.java'
triggers:
  keywords:
  - 中文分词
  - IK 分词器
  - ik_max_word
  - ik_smart
  - analyzer
effort: medium
context: inline
version: '1.0'
---
# Elasticsearch · 中文分词器 IK

> 本条只管「中文字段用哪个分词器、索引/查询分别配什么」。字段该不该用 text 见 [`mapping-design.md`](./mapping-design.md)。

## 规则

| 场景 | 用什么 | 原因 |
|------|--------|------|
| 中文 `text` 字段建索引（`analyzer`） | `ik_max_word` | 细粒度，尽可能多切词，**提高召回**（一段话切出更多词条入倒排） |
| 中文 `text` 字段查询（`search_analyzer`） | `ik_smart` | 粗粒度，切分更合理，**提高精度**（避免查询词被过度拆分误匹配） |
| 默认不配 | `standard`（中文按**单字**切） | ❌ 中文场景几乎不可用，召回精度都差 |
| 词典 | IK 自定义词典 / 远程词典 | 业务专有名词（品牌、术语）加入，避免被切碎 |

口诀：**索引 max_word（多切多召回），查询 ik_smart（少切准命中）**。IK 是插件，需在每个节点安装对应 ES 版本的 `analysis-ik`。

## 正例

```json
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "ik_max_word",
        "search_analyzer": "ik_smart"
      }
    }
  }
}
```

```bash
# 验证分词效果（建索引视角）
POST /my_index/_analyze
{ "field": "title", "text": "中华人民共和国国歌" }
# ik_max_word 切出：中华人民共和国 / 中华人民 / 中华 / 华人 / 人民共和国 / 人民 / 共和国 / 国歌 ...
```

## 反例

```json
// ❌ 不配分词器，中文走默认 standard —— 按单字切，"手机壳" 拆成 手/机/壳，搜"手机"也命中"洗手机液"
{ "properties": { "title": { "type": "text" } } }

// ❌ 索引和查询都用 ik_max_word —— 查询词也被多切，召回过多噪声、精度下降
{ "title": { "type": "text", "analyzer": "ik_max_word", "search_analyzer": "ik_max_word" } }
```

理由：中文无空格分隔，`standard` 单字切既丢语义又乱命中；查询端若也用 `ik_max_word`，查询词被拆成过多碎词，匹配面过宽，相关性变差。

## 自检

- [ ] 中文 `text` 字段显式配了 IK，没用默认 `standard`？
- [ ] 索引 `analyzer = ik_max_word`、查询 `search_analyzer = ik_smart`？
- [ ] 所有数据节点都装了与 ES 版本匹配的 IK 插件？
- [ ] 业务专有名词通过自定义词典维护，没被切碎？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mapping-design.md`](./mapping-design.md)（哪些字段该是 text 才需要分词器）
- 兄弟：[`query-dsl.md`](./query-dsl.md)（分词字段用 match 走相关性检索）
