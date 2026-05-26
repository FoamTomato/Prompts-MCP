---
name: pr-create-and-close
description: gh pr create --fill — SessionEnd hook 自动翻 In Review
parent: ./index.md
paths:
- .github/**
- '**'
triggers:
  keywords:
  - gh pr create
  - PR
  - close
  - 自动翻
effort: medium
context: inline
version: '1.0'
---
# PR · 创建与关闭

## 创建 PR

```bash
gh pr create --fill
```

`--fill` 用第一个 commit 作为 PR title + 后续 commits 作为 body。

## SessionEnd hook 自动行为

会话结束时（`session_end.sh`）：

1. 检查当前分支是否对应一个 Issue（manifest 反查）
2. 检查是否有未推送的 commit
3. 如有且 PR 不存在 → 自动 `gh pr create --fill`
4. PR 创建后推 Status: In Progress → In Review

## PR Body 标准格式

```markdown
## What

简述本 PR 改动（≤ 3 行）

## Why

为什么改 / 解决什么问题（≤ 5 行）

## How

关键技术决策（如有特殊取舍）

## Related

Closes #54
- PRD: [project-index/modules/home_page/H1-page-shell.md](...)
- 设计：[design/home-sketch.html#H1](...)
```

## 关闭 Issue

PR merge 后：

1. GitHub 自动识别 `Closes #N` → 关闭 Issue
2. Project workflow rule "Item closed → Set Status: Done" 触发
3. `dashboard.yml` hourly schedule 兜底（若上面没触发，跑 `quill-sync-done`）

## Merge 策略

| 策略 | 何时 |
|------|------|
| **Squash merge** | 默认（保持 main 分支线性） |
| Merge commit | 大改动需保留中间历史 |
| Rebase merge | 不用（容易丢 commit 信息） |

## 反例

```bash
# ❌ 手工 git push 不开 PR
git push origin feature

# ❌ PR description 留空 / 无 issue 关联
gh pr create --title "feat" --body ""

# ❌ 多模块塞一个 PR
# 一个 PR 改了 H1 + D6 + M3
```

## 自检

- [ ] 用 gh pr create --fill 不手动？
- [ ] PR body 有 What / Why / Closes #N？
- [ ] 一 PR 一子模块？
- [ ] Squash merge？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`status-lifecycle.md`](./status-lifecycle.md) · [`quill-start-usage.md`](./quill-start-usage.md) · [`conflict-resolution.md`](./conflict-resolution.md)

