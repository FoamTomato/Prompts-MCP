---
name: skill-body-length-budget
description: skill 正文（H1 之后到文末）必须 ≤100 行，超出部分拆到同目录 reference.md / examples.md。Use when 写新 skill / 重构超长 skill / lint 报 body-too-long 警告 / agent 抱怨某条 skill 拖慢响应时。
parent: ./index.md
paths:
  - "skills/**/*.md"
triggers:
  keywords:
    - 100 行限制
    - skill 长度
    - body length
    - skill body
    - reference.md
    - progressive disclosure
    - 拆 skill
effort: low
version: "1.0"
---

# Skill 正文长度预算

## 硬边界

**正文 ≤ 100 行**（不含 frontmatter）。lint 工具 warn ≥100 行，error ≥150 行。

## 为什么 100 行

| 长度 | 后果 |
|------|------|
| ≤50 行 | 理想区间，agent 一次性消化无负担 |
| 50–100 行 | 可接受，但每次 search_skills 返回会占调用方上下文 |
| 100–150 行 | 一定能拆 — 通常前 50 行是 "principle"，后面是 "examples" |
| >150 行 | 几乎一定是把多个相关但独立的规则塞一起了，得分文件 |

## 超长怎么办

不是"压缩文字"，而是**结构性拆分**：

```
my-skill.md           （前 50 行：核心规则 + 自检清单）
my-skill.reference.md （详细 API / 完整字段列表 / 长表格）
my-skill.examples.md  （5+ 个完整代码示例）
```

在主 SKILL 末尾用相对链接引：

```markdown
## 详细参考

- 完整 API 字段表：[`./my-skill.reference.md`](./my-skill.reference.md)
- 真实项目示例：[`./my-skill.examples.md`](./my-skill.examples.md)
```

调用方 LLM 先 `get_skill` 拿主文件，需要细节才 `get_skill_bundle([reference.md])` 二次拉。

## 拆分判断标准

写完一条 skill，回看正文，问：

1. **能不能一眼看完？** 不能 → 拆
2. **里面有没有 ≥3 个独立规则？** 有 → 拆成多个 skill 而不是拆成 reference
3. **API/字段表占了一半篇幅？** 是 → reference.md
4. **大段代码示例 >30 行？** 是 → examples.md

## 反例：什么算拖太长

- 在一条 skill 里同时讲"什么是 X" + "为什么用 X" + "X 的完整 API" + "X 的 5 个使用场景" + "X 的反模式" —— 这是 5 条独立 skill
- 把整个第三方库文档复述一遍 —— 应该外链官方文档，skill 只写本仓约定

## 自检清单

- [ ] `wc -l skill.md` 主文件 ≤100 行（含空行 / 含 frontmatter）
- [ ] 没有"附录"或"补充资料"类章节夹在主文件里
- [ ] 代码示例 ≤2 个，每个 ≤15 行
- [ ] 表格 ≤2 个，每个 ≤10 行

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`progressive-disclosure.md`](./progressive-disclosure.md) （拆完之后怎么组织外链）
- 跨维度：[`../code-quality/no-magic-values.md`](../code-quality/no-magic-values.md) （硬边界数值要可量化）
