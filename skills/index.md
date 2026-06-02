---
name: skills-root-index
description: Agent 技能的根索引 — 7 维度入口（lang / framework / design-pattern / habit / tech-selection / ai / fundamentals）
parent: null
children:
  - { name: lang, path: lang/index.md, tag: folder, note: 语言级规则（python / typescript / java / sql / js） }
  - { name: framework, path: framework/index.md, tag: folder, note: 框架库规则（react / antd / fastapi / spring-boot / mybatis / redis...） }
  - { name: design-pattern, path: design-pattern/index.md, tag: folder, note: 设计模式（repository / factory / strategy / ddd / pipeline） }
  - { name: habit, path: habit/index.md, tag: folder, note: 流程习惯（commit / pr / prd-sync / error-code） }
  - { name: tech-selection, path: tech-selection/index.md, tag: folder, note: 技术选型对比（消息队列 / 数据库 / 缓存 / 搜索-OLAP） }
  - { name: ai, path: ai/index.md, tag: folder, note: AI 应用开发（向量库 / RAG / LLM 调用 / Agent-MCP / 框架） }
  - { name: fundamentals, path: fundamentals/index.md, tag: folder, note: 程序员内功（JVM / 并发原理 / 集合源码 / 虚拟线程 / 排查 / 分布式理论） }
when_to_descend: |
  CLAUDE.md Step 5（B/C 档）必读起点。所有 skill 加载都从这里开始下钻，不允许跳过本层直读叶子。
---

# Agent Skills · 顶层路标

> 这是 [`/CLAUDE.md`](../CLAUDE.md) Step 5 的下钻起点。
> 状态：**内容持续扩充中**——7 维度，frontmatter 均含 `paths` / `triggers`，支持双向检索（顶层下钻 + 路径反查）。Java 生态已成体系：lang（JDK 原生 + 流水线风格）、framework（Spring 全家桶/MyBatis(-Plus)/MySQL/Redis/Redisson/MQ/ES/Security/调度/测试/可观测等）、fundamentals（JVM/并发/集合/虚拟线程/排查/分布式理论内功）、tech-selection（选型对比）、ai（AI 应用开发）。

## 规模一览

| 维度 | 中层 index | 叶子 skill | 状态 |
|------|---------|---------|------|
| lang | 36 | 83 | 实写 |
| framework | 45 | 157 | 实写 |
| design-pattern | 6 | 15 | 实写 |
| habit | 6 | 23 | 实写 |
| tech-selection | 4 | 8 | 实写 |
| ai | 5 | 18 | 实写 |
| fundamentals | 6 | 22 | 实写 |
| **合计** | **108** | **326** | **326 实写** |

所有叶子均有 frontmatter（含 `paths` / `triggers`）通过 YAML 解析校验，可被反向检索。

## 7 大维度

| 维度 | 入口 | 一句话 | 何时进 |
|------|------|--------|--------|
| **lang** | [lang/index.md](lang/index.md) | 语法/语言级风格 | 任务涉及 .py / .ts / .tsx / .sql / .js / .java 文件 |
| **framework** | [framework/index.md](framework/index.md) | 框架/库的使用约定 | 任务涉及 React / antd / FastAPI / Spring Boot / MyBatis / Redis 等 |
| **design-pattern** | [design-pattern/index.md](design-pattern/index.md) | 抽象设计模式 | 任务涉及分层、Repo、Factory、Strategy、Pipeline 决策 |
| **habit** | [habit/index.md](habit/index.md) | 流程/协作习惯 | commit / PR / PRD-sync / 错误码 / 代码质量 |
| **tech-selection** | [tech-selection/index.md](tech-selection/index.md) | 技术选型对比 | 选消息队列 / 数据库 / 缓存 / 搜索-OLAP 时 |
| **ai** | [ai/index.md](ai/index.md) | AI 应用开发 | 做 RAG / 调 LLM / 写 Agent / 选向量库或 AI 框架时 |
| **fundamentals** | [fundamentals/index.md](fundamentals/index.md) | 程序员内功（规约+决策） | 调 GC / 排查线上问题 / 选锁 / 分布式方案与一致性决策时 |

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
| 写 antd 表单 | framework/antd/form + framework/antd/antd-mcp-usage.md | 3 层 |
| 收工 PR | habit/pr + habit/commit + habit/prd-sync | 2 层 |
| 改某个 .java 业务方法 | lang/java/pipeline-style + lang/java + framework/spring-boot | 3-4 层 |
| 写 MyBatis Mapper / SQL 映射 | framework/mybatis(-plus) + framework/mysql | 3 层 |
| 集成消息队列 / 缓存 / 搜索 | framework/{kafka,rocketmq,redis,redisson,elasticsearch} | 3 层 |
| 选型：MQ / 数据库 / 缓存 哪个 | tech-selection/{message-queue,database,cache} | 2 层 |
| GC 调优 / 排查 CPU 飙高、OOM、内存泄漏 | fundamentals/{jvm,troubleshooting} | 2-3 层 |
| 选锁 / 该不该用虚拟线程 / 分布式事务方案 | fundamentals/{concurrency-internals,virtual-threads,distributed-theory} | 2-3 层 |
| 实现分布式锁 / 幂等 / 分布式 ID | fundamentals/distributed-theory + framework/{redisson,redis} | 3 层 |
| 做 RAG / 调 LLM / 写 Agent / 选向量库 | ai/{rag,llm-engineering,agent-mcp,vector-db,llm-framework} | 3 层 |

### 方式 B：从文件路径反向命中（自动检索）

每个叶子 skill 在 frontmatter 声明 `paths: ["<glob>"]`。当你正在编辑的文件路径匹配某个 skill 的 paths，**该 skill 强制进入加载清单**（不论顶层下钻路径是否经过它）。

例：你在改 `backend/services/textbook_cache.py` → 自动命中以下叶子（部分）：
- `lang/python/naming/function-naming.md`（paths: `backend/**/*.py`）
- `lang/python/async/no-blocking-call.md`
- `lang/python/style/no-n-plus-one.md`
- `design-pattern/repository/crud-contract.md`（如果文件在 repositories/）
- `framework/fastapi/router/zero-logic-principle.md`（如果文件在 routers/）

PostToolUse hook 在 W3 升级后会自动 echo 命中的 skill 到 stderr，提醒"你写完这段代码应该回头看一眼某 skill"。

## 跨切面主题速查（一个主题散在多维度时，从这里找入口）

有些主题天然横跨多维度，单靠维度下钻容易漏。下表给「主题 → 权威入口 + 相关落点」，避免各处建议不一致：

| 跨切面主题 | 权威入口（先看） | 相关落点 |
|-----------|----------------|---------|
| 幂等设计 | [fundamentals/distributed-theory/idempotent-design](fundamentals/distributed-theory/idempotent-design.md) | framework/kafka·rocketmq 的 idempotent（MQ 落地）/ mysql 唯一键 |
| 分布式锁 | [framework/redisson/distributed-lock](framework/redisson/distributed-lock.md) | framework/redis/distributed-lock（SETNX 视角）/ fundamentals/distributed-theory |
| 分布式 ID | [fundamentals/distributed-theory/distributed-id](fundamentals/distributed-theory/distributed-id.md) | framework/mysql/ops/distributed-id（DB 发号器落地） |
| 分布式事务 | [fundamentals/distributed-theory/transaction-solutions](fundamentals/distributed-theory/transaction-solutions.md) | framework/seata（AT/TCC/Saga 落地） |
| 配置管理 | [framework/spring-boot/config-properties](framework/spring-boot/config-properties.md) | fundamentals/jvm/heap-params（JVM 启动参数） |
| 日志规约 | [framework/observability/structured-logging](framework/observability/structured-logging.md) | framework/observability/skywalking-tracing（traceId 贯穿） |
| 错误码体系 | [habit/error-code](habit/error-code/index.md) | lang/java/error-handling（异常分类）/ design-pattern/assertion |
| 缓存一致性 | [framework/redis/cache-patterns](framework/redis/cache-patterns.md) | tech-selection/cache（选型）/ framework/observability |
| 线上问题排查 | [fundamentals/troubleshooting](fundamentals/troubleshooting/index.md) | fundamentals/jvm/oom-troubleshooting / framework/mysql/diagnosis |

> 原则：跨切面主题以「权威入口」为准，各维度的落点只讲自己那部分的落地，**不重复给方案**。新写这类 skill 时务必回链权威入口（见 [`/.claude/skills-philosophy.md`](../.claude/skills-philosophy.md) 信条 3）。

## 规则

1. 一个任务**最多同时**激活 3 个维度的叶子（避免上下文炸裂）
2. 每个维度下钻**最多 3 层** index 跳转（叶子层不算下钻）
3. 读完 index.md 后**必须**继续下钻到具体规则文件 — 只读 index 不算「加载了技能」
4. 下钻前若发现某 skill `paths:` 字段匹配当前文件路径 → 强制进入
5. 叶子文件 ≤ 100 行（W3 填充时严格遵守，超就拆）

## 链接

- 上层：（顶层，无）
- 调用方：[`/CLAUDE.md`](../CLAUDE.md) Step 5
- 流程总图：[`/design/claude-md-flow-sketch.html`](../../design/claude-md-flow-sketch.html)
- 旧版 skills（W3 末删除）：`.ai/skills/`
- 方法论参考：`/Users/foam/个人项目/docs/Creative_Ideation/harness/skills/`
