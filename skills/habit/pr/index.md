---
name: habit-pr-index
description: PR 流程
parent: ../index.md
children:
  - { name: status-lifecycle, path: status-lifecycle.md, tag: skill, note: 5 态：Backlog→Ready→In Progress→In Review→Done }
  - { name: start-usage, path: start-usage.md, tag: skill, note: scripts/pr-start 用法 }
  - { name: create-and-close, path: create-and-close.md, tag: skill, note: gh pr create --fill + 自动 close }
  - { name: conflict-resolution, path: conflict-resolution.md, tag: skill, note: 兜底命令 pr-set-status / pr-sync-done }
when_to_descend: 开工 / 收工 / PR 状态流转
---

# Pr · 子项索引

| 子项 | 一句话 |
|------|-------|
| status-lifecycle | 5 态：Backlog→Ready→In Progress→In Review→Done |
| start-usage | scripts/pr-start 用法 |
| create-and-close | gh pr create --fill + 自动 close |
| conflict-resolution | 兜底命令 pr-set-status / pr-sync-done |
