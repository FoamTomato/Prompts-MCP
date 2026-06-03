# CLAUDE.md

本仓是一套 **skills harness**:把项目规约写成 `skills/**/*.md`,通过 MCP 按需检索分发给任意 LLM。详见 [`README.md`](README.md)。

---

## 设计 / 评审 skill 前 —— 强制入口

只要任务涉及**新建、修改、拆分或评审任何 `skills/**/*.md`**,**第一步必读**:

1. [`.claude/skills-philosophy.md`](.claude/skills-philosophy.md) —— **WHY**:harness 思想纲领(4 条核心信条 + 业界锚点 + 越界自检)。先理解为什么这样设计。
2. [`skills/habit/skill-authoring/index.md`](skills/habit/skill-authoring/index.md) —— **HOW**:description 写法 / 命名与检索 / 渐进披露 / 触发词 / 正文长度的具体操作规约。

> 一句话准则:**每条 skill 最小化职责、语义明确、互不越界;agent 靠检索命中,而非被全部规约灌满。** 任何"读着顺/叙事完整"的考量,都让位于"被随机检索命中时是否精准"。

强制规约的最终版(lint 按它跑)在 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

---

## skills 结构速览

八个正交维度(详见 [`skills/index.md`](skills/index.md)):

| 维度 | 管什么 |
|------|--------|
| [`lang/`](skills/lang/index.md) | 语言级规则(python / typescript / java / sql / js) |
| [`framework/`](skills/framework/index.md) | 框架库用法(react / antd / fastapi / spring-boot / mybatis / mapstruct / redis / dubbo / spring-cloud / kafka / rocketmq...) |
| [`design-pattern/`](skills/design-pattern/index.md) | 设计模式(repository / factory / strategy / ddd / pipeline / assertion) |
| [`habit/`](skills/habit/index.md) | 流程习惯(commit / pr / prd-sync / error-code / code-quality / skill-authoring) |
| [`tech-selection/`](skills/tech-selection/index.md) | 技术选型对比(消息队列 / 数据库 / 缓存 / 搜索-OLAP) |
| [`ai/`](skills/ai/index.md) | AI 应用开发(向量库 / RAG / LLM 调用 / Agent-MCP / 框架) |
| [`fundamentals/`](skills/fundamentals/index.md) | 程序员内功·规约+决策(JVM / 并发原理 / 集合源码 / 虚拟线程 / 线上排查 / 分布式理论) |
| [`design/`](skills/design/index.md) | UI 设计(通用规范 a11y/间距/字体/配色 + 主题风格 bento/flat/wes-anderson + 设计语言 token + 组件模式) |

一个任务通常横跨多个维度下钻;关联但独立的规约拆成兄弟叶子,靠各层 `index.md` 路由。

> Java 业务方法（Service 层）的代码示例统一遵循[注释驱动流水线编排风格](skills/lang/java/pipeline-style/index.md)：方法即编排器、每步一注释一调用、中间变量 `final`、逻辑下沉 Converter/Validator/Utils。
