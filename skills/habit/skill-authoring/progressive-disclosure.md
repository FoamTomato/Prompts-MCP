---
name: skill-progressive-disclosure
description: skill 内容分主入口 + 二级引用文件 — 主入口给规则与自检，二级文件给详细 API / 代码示例 / 反模式集。Use when 写超过 80 行的 skill / 主文件外链到 reference / 设计配套脚本 assets / 评审拆分粒度时。
parent: ./index.md
paths:
  - "skills/**/*.md"
triggers:
  keywords:
    - progressive disclosure
    - 渐进披露
    - reference.md
    - examples.md
    - skill 配套文件
    - 二级文件
    - skill 拆分
effort: low
version: "1.0"
---

# Progressive Disclosure · 渐进披露

## 核心思想

agent 加载 skill 是分阶段的：

1. **筛选阶段**：只看 description（决定要不要加载）
2. **理解阶段**：拿主文件正文（落实做法）
3. **深查阶段**：按需拿 reference / examples（处理边界）

每个阶段加载的内容应当**严格递增**，主文件不要塞深查内容。

## 目录形态

```
skills/<dim>/<sub>/
├── my-skill.md              主入口 — frontmatter + 规则 + 自检清单 + 链接
├── my-skill.reference.md    （可选）详细 API / 完整字段表
├── my-skill.examples.md     （可选）完整代码示例集
└── scripts/                 （可选）配套确定性脚本
    └── validate.py
```

## 命名约定

| 文件 | 用途 | frontmatter |
|------|------|-------------|
| `<name>.md` | 主入口 | **完整 frontmatter**，含 paths/triggers/effort |
| `<name>.reference.md` | 详细参考 | **不要 frontmatter**（lint 跳过），只是 markdown 文档 |
| `<name>.examples.md` | 示例集 | 同上 |
| `scripts/*.py` | 配套脚本 | 无 frontmatter |

⚠️ **只有主入口有 frontmatter**，二级文件被 loader 当成普通 markdown — 不会出现在 `search_skills` 结果里，只有主 skill 命中后 agent 顺着链接二次 `get_skill_bundle` 才会拉。

## 链接写法

主入口末尾固定一段：

```markdown
## 详细参考

- API 字段表：[`./my-skill.reference.md`](./my-skill.reference.md)
- 真实示例：[`./my-skill.examples.md`](./my-skill.examples.md)
- 配套验证脚本：[`./scripts/validate.py`](./scripts/validate.py)
```

agent 读到这段就知道 "深内容在这里，按需拉"。

## 反模式

❌ **把 reference 内容直接拼到主文件**

理由：主文件超长 → 命中即占爆调用方上下文 → agent 用不下。

❌ **二级文件也加 frontmatter**

理由：会被 loader 当成独立 skill 索引进去，污染 `list_skills` 返回。

❌ **过度拆分**

主文件 ≤30 行就别拆。"3 句话能讲完的规则"硬拆 reference 是噪音。

## 自检清单

- [ ] 主文件 ≤100 行
- [ ] 二级文件（如有）**没有** frontmatter
- [ ] 主文件末尾有「详细参考」section 列所有二级文件
- [ ] 二级文件命名是 `<主文件名>.reference.md` / `.examples.md`（不是 `详细.md`）

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`body-length-budget.md`](./body-length-budget.md) （什么时候触发拆）
- 跨维度：[`../../design-pattern/pipeline/method-as-flow.md`](../../design-pattern/pipeline/method-as-flow.md) （注释驱动的流水线同样是渐进披露）
