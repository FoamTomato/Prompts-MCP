---
name: skill-trigger-phrasing
description: triggers.keywords 写法 — 中英双语 + 同义词 + 名词短语，与 description 的 Use when 职责分离。Use when 写新 skill / lint 报 keywords 类违规 / search_skills 命中率低时。
parent: ./index.md
paths:
  - "skills/**/*.md"
triggers:
  keywords:
    - triggers.keywords
    - 触发词
    - trigger keywords
    - 中英双语
    - bilingual keywords
    - 用户原话
    - 召回率
effort: low
version: "1.0"
---

# 触发词写法

## 两个字段的职责分工

| 字段 | 谁读 | 内容形态 |
|------|------|---------|
| `triggers.keywords` | matcher 倒排索引（精确匹配 + 子串） | 名词短语 / 类名 / API 名 / 中英术语 |
| `description` 第二句 `Use when` | LLM 语义判断 | 完整动词短语 / 用户/agent 实际会说的原话 |

**不要在 keywords 里写句子，不要在 description 里堆名词列表**。

## keywords 规则

### 数量

- ≥ **3** 个（lint 强制）
- 推荐 5–8 个
- 不超过 15 个（超过通常是塞了同义词噪音）

### 双语强制

- 至少 **1 个中文** + 至少 **1 个英文**（lint 强制）
- 中文为主的项目，建议 60% 中文 40% 英文

### 形态

✅ 好的 keywords：

```yaml
keywords:
  - Form 校验            # 项目术语
  - validator            # API/库名
  - 表单校验             # 中文同义
  - field validation     # 英文同义
  - Pydantic Field       # 跨技术栈关联词
```

❌ 反例：

```yaml
keywords:
  - 写表单的时候          # 句子（应进 description）
  - 自定义校              # sliding-window 截断片段
  - rules                # 单词太泛，会跟 antd / yup / zod 等全部撞
  - 表单                  # 单词太泛
  - validator            # 重复
  - validator            # 重复
```

### 同义词覆盖

写完后做一个**思想实验**：

> 一个陌生 LLM 不知道我项目的术语，它最可能用什么词描述这个场景？

把那 2-3 个候选词加进 keywords。例：

- 主词 `JWT` → 加 `鉴权` / `auth` / `token 验证`
- 主词 `匿名会话` → 加 `anonymous session` / `游客模式` / `未登录用户`
- 主词 `Tortoise Model` → 加 `ORM` / `数据模型` / `database model`

## description 的 Use when 补什么

`Use when` 后写**agent 实际行为情境**（动词开头），不写关键字：

```
Use when 新建 entity / 重构 aggregate root / Migration 报字段冲突 / 评审 ORM 类。
```

不写：

```
Use when entity, aggregate, ORM, migration, fields.   ❌ 关键字堆砌
```

## 自检清单

- [ ] keywords ≥3 且含至少 1 中 1 英
- [ ] keywords 全是名词短语 / 专有名词，**没有句子**
- [ ] 至少 1 个 keyword 是"陌生 LLM 会用但本项目术语没用的词"
- [ ] description 第二句 Use when 后是**动词短语**，不是关键字列表
- [ ] keywords 和 Use when 的内容**不重复**（重复说明职责没分清）

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`description-format.md`](./description-format.md) （Use when 的写法标准）
- 工具：[`../../../scripts/fix_keywords_zh.py`](../../../scripts/fix_keywords_zh.py) 批量补中文 keywords 的工具
