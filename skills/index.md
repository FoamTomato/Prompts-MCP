---
name: skills-root-index
description: Quill 全部 Agent 技能的根索引 — 4 维度入口
parent: null
children:
  - { name: lang, path: lang/index.md, tag: folder, note: 语言级规则（python / typescript / sql） }
  - { name: framework, path: framework/index.md, tag: folder, note: 框架库规则（react / antd / fastapi / tortoise / gsap） }
  - { name: design-pattern, path: design-pattern/index.md, tag: folder, note: 设计模式（repository / factory / strategy / ddd / pipeline） }
  - { name: habit, path: habit/index.md, tag: folder, note: 流程习惯（commit / pr / prd-sync / error-code） }
when_to_descend: |
  CLAUDE.md Step 5（B/C 档）必读起点。所有 skill 加载都从这里开始下钻，不允许跳过本层直读叶子。
---

# Quill Skills · 顶层路标

> 这是 [`/CLAUDE.md`](../../CLAUDE.md) Step 5 的下钻起点。
> 状态：**W3 内容已落地**——4 维度 × 52 中层索引 × 131 叶子 skill 全部实写完成；frontmatter 均含 `paths` / `triggers`，支持双向检索（顶层下钻 + 路径反查）。

## 规模一览（W3 末）

| 维度 | 中层 index | 叶子 skill | 状态 |
|------|---------|---------|------|
| lang | 24 | 49 | 实写 |
| framework | 17 | 49 | 实写 |
| design-pattern | 6 | 15 | 实写 |
| habit | 5 | 18 | 实写 |
| **合计** | **52** | **131** | **131 / 131 实写** |

所有叶子均有 frontmatter（含 `paths` / `triggers`）通过 YAML 解析校验，可被反向检索。

## 4 大维度

| 维度 | 入口 | 一句话 | 何时进 |
|------|------|--------|--------|
| **lang** | [lang/index.md](lang/index.md) | 语法/语言级风格 | 任务涉及 .py / .ts / .tsx / .sql / .js / .java 文件 |
| **framework** | [framework/index.md](framework/index.md) | 框架/库的使用约定 | 任务涉及 React 组件 / antd / FastAPI / Tortoise / GSAP |
| **design-pattern** | [design-pattern/index.md](design-pattern/index.md) | 抽象设计模式 | 任务涉及分层、Repo、Factory、Strategy、Pipeline 决策 |
| **habit** | [habit/index.md](habit/index.md) | 流程/协作习惯 | commit / PR / PRD-sync / 错误码 / 代码质量 |

## 两种下钻方式

### 方式 A：从顶层向下（场景驱动）

由 CLAUDE.md Step 5 调用：先看任务上下文落到哪个维度 → 进该维度 index → 看决策表选 1-3 个子项继续下钻。

| 任务上下文信号 | 进哪个维度 | 通常下钻深度 |
|--------------|-----------|----------|
| 改某个 .py 文件 | lang/python + framework/fastapi + design-pattern/ddd-layering | 3-4 层 |
| 写新 .tsx 组件 | framework/react/component + lang/typescript + framework/antd（如有） | 3 层 |
| 写 SQL / migration | lang/sql + framework/tortoise | 3 层 |
| 改 PRD / 同步 manifest | habit/prd-sync | 2 层 |
| 设计新 Service | design-pattern/ddd-layering + design-pattern/repository | 3 层 |
| 写 LLM 编排 | framework/fastapi/llm + design-pattern/pipeline | 3 层 |
| 写 antd 表单 | framework/antd/form + framework/antd/mcp-first | 3 层 |
| 收工 PR | habit/pr + habit/commit + habit/prd-sync | 2 层 |

### 方式 B：从文件路径反向命中（自动检索）

每个叶子 skill 在 frontmatter 声明 `paths: ["<glob>"]`。当你正在编辑的文件路径匹配某个 skill 的 paths，**该 skill 强制进入加载清单**（不论顶层下钻路径是否经过它）。

例：你在改 `backend/services/textbook_cache.py` → 自动命中以下叶子（部分）：
- `lang/python/naming/function-naming.md`（paths: `backend/**/*.py`）
- `lang/python/async/no-blocking-call.md`
- `lang/python/style/no-n-plus-one.md`
- `design-pattern/repository/usage-rule.md`（如果文件在 repositories/）
- `framework/fastapi/router/zero-logic-principle.md`（如果文件在 routers/）

PostToolUse hook 在 W3 升级后会自动 echo 命中的 skill 到 stderr，提醒"你写完这段代码应该回头看一眼某 skill"。

## 规则

1. 一个任务**最多同时**激活 3 个维度的叶子（避免上下文炸裂）
2. 每个维度下钻**最多 3 层** index 跳转（叶子层不算下钻）
3. 读完 index.md 后**必须**继续下钻到具体规则文件 — 只读 index 不算「加载了技能」
4. 下钻前若发现某 skill `paths:` 字段匹配当前文件路径 → 强制进入
5. 叶子文件 ≤ 100 行（W3 填充时严格遵守，超就拆）

## 链接

- 上层：（顶层，无）
- 调用方：[`/CLAUDE.md`](../../CLAUDE.md) Step 5
- 流程总图：[`/design/claude-md-flow-sketch.html`](../../design/claude-md-flow-sketch.html)
- 旧版 skills（W3 末删除）：`.ai/skills/`
- 方法论参考：`/Users/foam/个人项目/docs/Creative_Ideation/harness/skills/`
