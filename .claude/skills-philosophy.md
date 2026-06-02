# Skills 设计哲学 · Harness 思想纲领

> 这是本仓 `skills/` 的**理论根**。讲的是 **WHY**(为什么这样设计 skill)。
> **HOW**(怎么写 description / 命名 / 拆分 / 长度)在 [`skills/habit/skill-authoring/`](../skills/habit/skill-authoring/index.md) 的 6 个叶子里 —— 本文不重复,只在每条信条末尾指向对应叶子。
>
> 新建或评审任何 skill 之前,先读完本文,再去 skill-authoring 取操作规约。

---

## 一句话

整个 `skills/` 文件夹是一套 **harness**(马具/约束架):它不改模型,而是设计**模型之外的那一层** —— 决定 agent 在什么时机、看到哪些规约。每一条 skill 是这套 harness 上的一个**最小化、语义明确、互不越界**的约束单元;agent 靠**检索**命中它需要的那几条,而不是被全部规约一次性灌满。

---

## 业界锚点(2026 · Harness Engineering)

本仓的做法不是个人偏好,它精确对应 2025 下半年成型、2026 爆火的一套方法论。术语对照,便于和外部资料互译:

| 本仓说法 | 业界术语 | 出处 |
|---------|---------|------|
| 「skills 文件夹是 harness」 | **Harness Engineering** = 优化 agent 系统的**非模型层**(工具/上下文/记忆/编排),是比换模型更高杠杆的事 | LangChain《The Anatomy of an Agent Harness》、OpenAI《Harness Engineering》 |
| 「靠检索判断需要哪个 skill」 | **Progressive Disclosure 三层架构**(发现 / 激活 / 执行) | SwirlAI《Agent Skills: Progressive Disclosure as a System Design Pattern》 |
| 「每个 skill 最小化职责」 | **Single-Responsibility Skill** + "Less (instructions) is more" | HumanLayer《Skill Issue: Harness Engineering for Coding Agents》 |
| 「语义明确不越界」 | 反模式:**单 skill 塞过宽能力 → context bloat → 把模型推进 "dumb zone"** | 同上 |

---

## 四条核心信条

### 信条 1 · skills 是 harness,不是文档库

skill 是写给 **agent** 看的,不是写给人读的手册。判据永远是这一个问题:

> agent 看到这条 skill 时,能否 (1) 立刻判断**要不要**加载它,(2) 加载后**知道做什么**?

推论:任何"读着顺/叙事完整"的考量都让位于"被随机检索命中时是否精准"。作者视角(从头读)与检索者视角(搜一个词跳进来)冲突时,**永远选检索者视角**。

### 信条 2 · 渐进式披露:内容严格分三层,逐层递增

agent 加载 skill 是**分阶段**的,每一阶段加载的内容必须**严格递增**,前一层绝不夹带后一层的东西:

| 层 | 加载什么 | 预算 | 本仓载体 |
|----|---------|------|---------|
| **L1 发现** | 只读 frontmatter 的 `name` + 一句话 `description` | ~80 token/skill | `index.md` 表格 + 各文件 description |
| **L2 激活** | 命中后才载入整篇正文 | ≤100 行 | skill 正文 |
| **L3 执行** | 按需拉详细 API / 示例 / 脚本 | 用到才载 | `*.reference.md` / `*.examples.md` / `scripts/` |

主文件不塞 L3 内容(否则命中即占爆调用方上下文)。
→ HOW:[`progressive-disclosure.md`](../skills/habit/skill-authoring/progressive-disclosure.md) · [`body-length-budget.md`](../skills/habit/skill-authoring/body-length-budget.md)

### 信条 3 · 单一职责:一条 skill 只回答一个决策点

一条 skill 只该回答**一个**开发者会独立提出的问题。判据:

> 把正文每一段贴上"它回答的问题"标签 —— 出现 ≥2 个**互相独立**的问题,就是 ≥2 条 skill,必须拆。

"相关"不等于"同一职责"。`checked vs runtime`(该抛哪类异常)、`catch 块怎么写`、`资源怎么释放`三件事都"和异常相关",但回答的是三个独立问题 → 三条 skill,关联性交给 `index.md` 兜,而不是塞进同一个文件。

拆细带来的副产品恰好是**检索精准**:职责越窄,description 越能一句话说清、零歧义。
→ HOW:[`body-length-budget.md`](../skills/habit/skill-authoring/body-length-budget.md)(拆分判断标准)

### 信条 4 · description 即路由:它是 agent 选 skill 的唯一信号

Claude **纯靠 description 推理**来决定加载哪条 skill —— description 质量**直接决定路由准确率**。因此 description 必须**完整且仅覆盖**正文内容:

- **多一句**(夹带正文没有 / 不属于本职责的东西)→ 误召回
- **少一句**(正文讲了某主题,description 没提)→ 漏召回

一个反向自检:如果一条 skill 的 `triggers.keywords` 覆盖不到它正文里的某块内容(例:正文有 try-with-resources,keywords 却没有),那不是 keywords 漏了 —— 是**那块内容根本不属于这条 skill**,该拆出去。
→ HOW:[`description-format.md`](../skills/habit/skill-authoring/description-format.md) · [`trigger-phrasing.md`](../skills/habit/skill-authoring/trigger-phrasing.md) · [`naming-and-retrieval.md`](../skills/habit/skill-authoring/naming-and-retrieval.md)

---

## 越界自检(新建 / 评审任一 skill 必过)

- [ ] **信条 1**:这条 skill 是给 agent 路由用的,不是给人读的叙事?
- [ ] **信条 2**:正文没夹带 L3(详细 API / 大段示例)?超 100 行已拆 reference/examples?
- [ ] **信条 3**:正文每一段都回答**同一个**决策点?不存在"顺带也讲了"的第二主题?
- [ ] **信条 4**:`description` + `keywords` **完整且仅**覆盖正文?没有覆盖不到的内容块(=该拆),也没有正文里没有的承诺(=误召回)?
- [ ] 关联但独立的知识已拆为兄弟叶子,靠所在 `index.md` 路由,而非塞进同一文件?

---

## 链接

- HOW 操作规约总入口:[`skills/habit/skill-authoring/index.md`](../skills/habit/skill-authoring/index.md)
- skills 根索引:[`skills/index.md`](../skills/index.md)
- 强制规约最终版(lint 按它跑):[`CONTRIBUTING.md`](../CONTRIBUTING.md)
