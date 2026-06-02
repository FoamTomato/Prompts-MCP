---
name: pr-conflict-resolution
description: 兜底命令 — pr-set-status / pr-sync-done。Use when 评审涉及 `conflict-resolution`
  的 PR。
parent: ./index.md
paths:
- scripts/**
triggers:
  keywords:
  - pr-set-status
  - pr-sync-done
  - 冲突
effort: medium
context: inline
version: '1.0'
---
# PR · 冲突与兜底命令

## 多 Agent 协作冲突

可借助团队的协作 dashboard 实现模块化协作：

- 每个 Agent claim 不同 Issue → 不同分支
- PreToolUse hook 在 Edit/Write 前检测："其他 Agent 是否动了同一 module 的文件"
- 检测到冲突 → stderr 警告（不阻断），建议先 `git pull --rebase`

## 兜底命令

> 下面的脚本名为占位，团队可改名适配自有工具链。

### Status 推不上

```bash
# 单个推
scripts/pr-set-status <N> Ready
scripts/pr-set-status <N> "In Progress"
scripts/pr-set-status <N> "In Review"
scripts/pr-set-status <N> Done

# 把已关闭 Issue 全部推 Done
scripts/pr-sync-done

# 先看会动哪些（不实际执行）
scripts/pr-sync-done --dry-run
```

### Manifest ↔ Issue 不同步

manifest.yaml 加了新 MODULE_ID 但 GitHub Issues 还没建：

```bash
# 触发团队的 bootstrap 脚本
scripts/bootstrap-github-issues.py
```

或：

```bash
# 手动触发对应 workflow
gh workflow run bootstrap.yml
```

### Snapshot 漂移

dashboard 看板数据来自 `snapshot.json`，hourly 自动更新。手动触发：

```bash
# 跑团队的 dashboard CI
gh workflow run dashboard.yml
```

或本地跑项目自有的同步脚本：

```bash
python3 scripts/build_snapshot.py > /tmp/snapshot.json
```

## 分支冲突

```bash
# 主线有更新，先 rebase
git fetch origin
git rebase origin/feature

# 解决冲突后
git rebase --continue
git push --force-with-lease
```

不要用 `--force`（覆盖别人提交风险）。

## 与 PRD 同步冲突

详见 CLAUDE.md Step 8 + `prd-sync-check.yml`。
若 PR 阻塞在 `prd-sync-check` CI，回到 Step 8 同步 PRD 文档再 push。

## 自检

- [ ] 用 hook 警告而非阻断？
- [ ] Status 失败用 pr-sync-done 兜底？
- [ ] 分支冲突用 rebase 不 force？
- [ ] PRD-sync CI 阻塞时回到 CLAUDE.md Step 8？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`status-lifecycle.md`](./status-lifecycle.md) · [`start-usage.md`](./start-usage.md) · [`create-and-close.md`](./create-and-close.md)

