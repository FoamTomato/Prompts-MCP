---
name: pr-start-usage
description: scripts/pr-start <MODULE_ID/Issue#> — 反查 manifest + 建分支 + assign。Use
  when 评审涉及 `pr-start-usage` 的 PR。
parent: ./index.md
paths:
- scripts/pr-start
- scripts/**
triggers:
  keywords:
  - pr-start
  - MODULE_ID
  - 反查
  - 建分支
effort: medium
context: inline
version: '1.0'
---
# PR · scripts/pr-start 用法

> 这是一份**项目无关**的 PR-start 脚本约定。脚本名 `scripts/pr-start` 仅作占位，团队可改名为 `scripts/<your-pr-start>` 适配自有工具链。

## 命令

```bash
scripts/pr-start <input>
```

`<input>` 可以是：

- **模块编号**：如 `<MODULE_ID>`（例 `feature-x` / `billing` / `auth`）
- **Issue 号**：`54` 或 `#54`
- **Issue URL**：`https://github.com/your-org/your-repo/issues/54`

## 自动做的事

```
1. 反查 manifest.yaml → 找到 MODULE_ID 对应 Issue 号
2. gh issue develop <N> -b feature -n <branch-name>
3. git checkout <branch-name>
4. gh issue edit <N> --add-assignee @me
5. 推 Project Status: Backlog/Ready → In Progress
```

## 分支命名

```
<N>-<module-id-lower>-<short-name>
```

例：
- `54-feature-x-content-type-selector`
- `78-billing-invoice-card`

## 使用示例

```bash
# 接任务（用 MODULE_ID）
$ scripts/pr-start feature-x
反查 manifest: feature-x → Issue #78
建分支: 78-feature-x-invoice-card
推 Status: Ready → In Progress
切到分支并开始

# 接任务（用 Issue 号）
$ scripts/pr-start 78
（同上）

# 接任务（用 URL）
$ scripts/pr-start https://github.com/your-org/your-repo/issues/78
（同上）
```

## 与 CLAUDE.md Step 2 协同

CLAUDE.md Step 2 在用户消息中识别到 MODULE_ID / Issue 号 / URL → 直接调 `scripts/pr-start`，不需要手工。

## 失败处理

| 失败 | 原因 | 解法 |
|------|------|------|
| manifest 查不到 MODULE_ID | manifest.yaml 未更新 | 手工补充 manifest |
| gh 无权限 | `gh auth login --scopes project,...` | 重 auth |
| Status 推不上去 | Project workflow rule 失败 | best-effort，跳过 |
| 已有同名分支 | 之前没清理 | 删旧分支或换名 |

## 自检

- [ ] 任务前用 pr-start，不手工建分支？
- [ ] gh CLI 已认证 + 有 project scope？
- [ ] manifest.yaml 与 Issue 同步？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`status-lifecycle.md`](./status-lifecycle.md) · [`pr-create-and-close.md`](./pr-create-and-close.md)
