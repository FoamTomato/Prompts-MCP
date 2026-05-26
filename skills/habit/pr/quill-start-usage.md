---
name: pr-quill-start-usage
description: scripts/quill-start <SUB_ID/Issue#> — 反查 manifest + 建分支 + assign。Use
  when 评审涉及 `quill-start-usage` 的 PR。
parent: ./index.md
paths:
- scripts/quill-start
- scripts/**
triggers:
  keywords:
  - quill-start
  - SUB_ID
  - 反查
  - 建分支
effort: medium
context: inline
version: '1.0'
---
# PR · scripts/quill-start 用法

## 命令

```bash
scripts/quill-start <input>
```

`<input>` 可以是：

- **子模块编号**：`H1` / `D21.6` / `C5`
- **Issue 号**：`54` 或 `#54`
- **Issue URL**：`https://github.com/FoamTomato/Quill/issues/54`

## 自动做的事

```
1. 反查 manifest.yaml → 找到 SUB_ID 对应 Issue 号
2. gh issue develop <N> -b feature -n <branch-name>
3. git checkout <branch-name>
4. gh issue edit <N> --add-assignee @me
5. 推 Project Status: Backlog/Ready → In Progress
```

## 分支命名

```
<N>-<sub-id-lower>-<short-name>
```

例：
- `54-h1-content-type-selector`
- `78-d6-presentation-card`

## 使用示例

```bash
# 接任务（用 SUB_ID）
$ scripts/quill-start D6
反查 manifest: D6 → Issue #78
建分支: 78-d6-presentation-card
推 Status: Ready → In Progress
切到分支并开始

# 接任务（用 Issue 号）
$ scripts/quill-start 78
（同上）

# 接任务（用 URL）
$ scripts/quill-start https://github.com/FoamTomato/Quill/issues/78
（同上）
```

## 与 CLAUDE.md Step 2 协同

CLAUDE.md Step 2 在用户消息中识别到 SUB_ID / Issue 号 / URL → 直接调 `scripts/quill-start`，不需要手工。

## 失败处理

| 失败 | 原因 | 解法 |
|------|------|------|
| manifest 查不到 SUB_ID | manifest.yaml 未更新 | 手工补充 manifest |
| gh 无权限 | `gh auth login --scopes project,...` | 重 auth |
| Status 推不上去 | Project workflow rule 失败 | best-effort，跳过 |
| 已有同名分支 | 之前没清理 | 删旧分支或换名 |

## 自检

- [ ] 任务前用 quill-start，不手工建分支？
- [ ] gh CLI 已认证 + 有 project scope？
- [ ] manifest.yaml 与 Issue 同步？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`status-lifecycle.md`](./status-lifecycle.md) · [`pr-create-and-close.md`](./pr-create-and-close.md)

