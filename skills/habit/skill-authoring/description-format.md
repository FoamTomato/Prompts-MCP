---
name: skill-description-format
description: skill 的 description 字段必须是两句结构 — 第一句讲是什么，第二句以"Use when"开头列具体触发场景。Use when 新建 skill / 修改 frontmatter / lint 报 description-length 违规 / 评审 skill PR 时。
parent: ./index.md
paths:
  - "skills/**/*.md"
triggers:
  keywords:
    - description 字段
    - Use when
    - skill 描述
    - skill description
    - frontmatter description
    - 触发场景
effort: low
version: "1.0"
---

# Skill description 字段写法

## 核心规则

**description 字段是 agent 决定要不要加载这条 skill 的唯一信号**（在 MCP 检索里它打 score；在原生 Claude Code 里它进系统提示）。写法不规范 = 永远命不中。

### 两句结构（硬要求）

```
<第一句：这条 skill 是关于什么的，含核心概念>。Use when <具体触发场景，用动词开头，列 2-4 个独立情境>。
```

- **第一句**：是什么、核心概念、限定词。不写"组件命名规则"（太泛），写"React/antd 组件命名：Button vs CTA vs BrandButton 的三类区分与选用"。
- **第二句**：**必须以"Use when"开头**，列出 agent 应该激活本 skill 的具体情境。每个情境是一个动词短语，用 `/` 分隔。

### 长度约束

- 总长 **30–80 字**（lint 强制）
- 超过 80 字优先压缩第一句（去掉冗余形容词）

## 正面示例

```yaml
description: |
  React/antd 组件命名规则 — Button / CTA / BrandButton 三类区分。
  Use when 新建组件文件 / 重构现有按钮组件 / 评审 PR 涉及组件命名。
```

```yaml
description: |
  Tortoise ORM Model 类标准模板：Meta 表名 / auto_now / 关系字段。
  Use when 写新 Model 子类 / 改模型字段 / 评审 Migration 时。
```

## 反面示例

| 反例 | 问题 |
|------|------|
| `组件命名规则` | 1. 太泛 2. 单句 3. 没 Use when |
| `Button / CTA / BrandButton naming` | 没中文，外国人写法照搬不适配 |
| `设计模式 · ddd: Domain 纯净` | 维度面包屑对召回零增益，浪费字数 |
| `写组件的时候要按这个规则来，比较重要，新人尤其注意` | 啰嗦废话，没具体信号 |

## 自检清单

写完后问自己：
- [ ] 第一句包含**具体名词**（类名/字段名/层名）？
- [ ] 第二句以 `Use when` 开头？
- [ ] Use when 后列了 ≥2 个独立触发情境？
- [ ] 触发情境用**用户/agent 实际会说的话**？（"新建 Model 类"而非"使用持久化层时"）
- [ ] 总长 30–80 字？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`trigger-phrasing.md`](./trigger-phrasing.md) （description 触发词 vs keywords 触发词的分工）
- 跨维度：[`../../habit/code-quality/naming-as-doc.md`](../code-quality/naming-as-doc.md) （命名即文档同理）
