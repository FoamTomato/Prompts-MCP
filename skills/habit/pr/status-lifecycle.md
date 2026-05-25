---
name: pr-status-lifecycle
description: PR 5 态：Backlog → Ready → In Progress → In Review → Done
parent: ./index.md
paths:
  - ".github/**"
  - "scripts/**"
  - "**"
triggers:
  keywords: [Status, Backlog, Ready, Done]
effort: medium
context: inline
version: "1.0"
---

# PR · Status 5 态流转

## 状态生命周期

| Status | 何时 | 谁推 | 命令 |
|--------|------|------|------|
| **Backlog** | bootstrap 默认值 | bootstrap 脚本 | `bootstrap-github-issues.py` 自动 |
| **Ready** | Issue 已就绪、准备认领 | Planner / 人工 | `scripts/quill-set-status <N> Ready` |
| **In Progress** | Agent 接到任务、开始改代码 | `quill-start` 自动 | `scripts/quill-start <SUB_ID>` |
| **In Review** | PR 已创建、等审 | session-end hook | 自动；或 `scripts/quill-set-status <N> "In Review"` |
| **Done** | PR 已合并、Issue 关闭 | Project workflow rule | "Item closed → Set Status: Done"（部署时启用） |

## 流转方向

```
Backlog → Ready → In Progress → In Review → Done
```

单向。回退（如评审打回）由人工操作。

## Status 切换失败不阻塞

hook / 脚本均 best-effort；Status 切换失败不阻塞主流程。Issue 状态本身 + branch + PR 关联即可。

## 兜底命令

```bash
# 批量推 Backlog → Ready（Planner 准备一批任务给 Agent）
scripts/quill-set-status 54 Ready

# 修正漏标 Done（Project workflow rule 没开 / 失败时）
scripts/quill-sync-done                # 把所有已关闭 issue 推 Done
scripts/quill-sync-done --dry-run      # 先看会动哪些
```

`dashboard.yml` 已把 `quill-sync-done` 接入 hourly schedule，所以 Done 兜底自动。

## 前置：token scope

`gh auth login --scopes project,read:project,repo` 必须含 `project` scope，否则 Project v2 GraphQL 调用 403。

## 自检

- [ ] 流转方向是单向 forward？
- [ ] 用脚本 / hook 自动推，不要手工改？
- [ ] 失败不阻塞主流程？
- [ ] Status 推不上去不要循环重试（best-effort）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`quill-start-usage.md`](./quill-start-usage.md) · [`pr-create-and-close.md`](./pr-create-and-close.md) · [`conflict-resolution.md`](./conflict-resolution.md)

