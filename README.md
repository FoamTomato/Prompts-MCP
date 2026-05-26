# Prompts-MCP

把一份结构化的 markdown 规约库做成 MCP server，让任意 LLM（Claude Desktop / Cursor / Cline / 自建 agent / 跨电脑跨项目）都能用同一套约定写代码。

> 灵感来自 Matt Pocock 的 [skills repo](https://github.com/mattpocock/skills)，但他用 Claude Code 原生 SKILL.md（always-on description 注入系统提示），我们用 MCP 工具按需检索 —— 因为我们的库是 200 条规约级粒度的，不是 14 条流程脚本。

**公开端点**
- MCP: `https://xiaohang.site/mcp/sse`
- Web 浏览: `https://xiaohang.site/skills/`

---

## 这套东西解决什么问题

### 问题 1：陌生 LLM 不知道我项目的约定

> *"No-one knows exactly what they want."*
> — David Thomas & Andrew Hunt, *The Pragmatic Programmer*

把 Claude 4.6 / Cursor / Cline 接上一个新仓，它会**忠实复现一套通用最佳实践** —— 但那不是我的项目要的最佳实践。我的 antd Table 必须服务端分页、我的 Tortoise Model 有标准 Meta 模板、我的错误码有前缀分配规则。每开一个新会话都解释一遍 = token 浪费 + 失忆。

**解法**：把项目约定写成 `skills/*.md`，agent 自动通过 MCP 查到。每条 skill 描述自己"什么时候要用我"，agent 看到匹配场景就主动加载。

### 问题 2：多人多模型共享一套规约

> *"With a ubiquitous language, conversations among developers and expressions of the code are all derived from the same domain model."*
> — Eric Evans, *Domain-Driven Design*

我用 Claude、他用 Cursor、CI 跑 OpenAI agent —— 大家如果各写各的提示词，规约会漂移。skill 单独维护、靠 git 版本化、靠 MCP 协议分发，所有模型读同一份事实。

**解法**：服务器跑一个公共 MCP server。`mcp.json` 配一行 URL，任何 MCP 客户端都接。

### 问题 3：规约太多，写在 README 里没人看

我的 Quill 项目有 200 条规约。塞进 CLAUDE.md → 系统提示爆 30K token，每个会话首 token 就要刷新缓存。塞进 README → 人读完都难。

**解法**：把 200 条按 (lang / framework / design-pattern / habit) 4 维度切，靠 `search_skills(paths=..., keywords=...)` 反向命中（dev 正在改 `.tsx` + 任务关键字含 `Table`，自动推送 antd table 相关的 3 条 skill）。agent 拿到 ≤5 条精准规则即可。

### 问题 4：写规约的人也需要规约

> *"Always take small, deliberate steps. The rate of feedback is your speed limit."*
> — Thomas & Hunt

新增/修改 skill 时，怎么保证它能被 agent 找到？怎么避免 description 太泛、keywords 漏中文、正文越写越长？

**解法**：[`scripts/lint_skills.py`](scripts/lint_skills.py) 强制 frontmatter 标准；[`habit/skill-authoring/`](skills/habit/skill-authoring/) 这条 meta-skill 把"怎么写 skill" 本身也变成可检索的 skill。lint 不通过的 PR 不让合。

---

## Quick start

### 本地开发

```bash
pip install -e ".[dev]"
cp .env.example .env
uvicorn prompts_mcp.server:app --reload --port 8080
# 浏览器开 http://localhost:8080/web/
```

### Docker

```bash
docker compose up -d
```

### 接入 Claude Desktop / Cursor

```json
{
  "mcpServers": {
    "prompts-mcp": {
      "url": "https://xiaohang.site/mcp/sse"
    }
  }
}
```

---

## 暴露的 7 个工具

**通用原语**（任何 LLM 都能开箱用）：
- `list_skills(dimension?, parent?, depth?, limit?, cursor?)` — 浏览 / 枚举（只回元数据）
- `get_skill(path | name, include?)` — 拿单个 skill 完整内容
- `get_skill_bundle(paths)` — 批量拿
- `search_skills(query?, keywords?, paths?, dimension?, effort?, top_k?, fields?)` — 统一检索（支持中英混合 query）
- `get_index_tree(max_depth?, include_descriptions?)` — 一次拿全局地图，给陌生 agent 用

**流程语法糖**（Quill 两条流程专用，其他场景也能用）：
- `pick_design_skills(topic, kind, limit?)` — 设计阶段抓 framework/design-pattern 规范
- `match_task_skills(artifact_paths, task_keywords, limit?)` — dev 阶段二维反查

**加 MCP Resources**：每条 skill 注册为 `skill://<dim>/<.../leaf>` URI，支持 Resources 的客户端直接浏览。

---

## skill 质量标准

详见 [`CONTRIBUTING.md`](CONTRIBUTING.md) 和 [`skills/habit/skill-authoring/`](skills/habit/skill-authoring/)。要点：

- **description** 两句结构（"是什么 + Use when ..."），30–150 字
- **triggers.keywords** ≥3，中英双语，名词短语
- **body** ≤100 行（warn）/ ≤150 行（error，需拆 `reference.md` / `examples.md`）
- 写完跑 `python scripts/lint_skills.py`，零 error 才能 commit

## License

MIT
