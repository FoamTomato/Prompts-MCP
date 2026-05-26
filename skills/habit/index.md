---
name: habit-index
description: 流程习惯索引（commit / pr / prd-sync / error-code / code-quality / skill-authoring）
parent: ../index.md
children:
  - { name: commit, path: commit/index.md, tag: folder, note: Conventional Commit / 在消息里 claim Issue }
  - { name: pr, path: pr/index.md, tag: folder, note: PR body 模板 / 一 PR 一子模块 }
  - { name: prd-sync, path: prd-sync/index.md, tag: folder, note: 代码改 → PRD 同步规范 }
  - { name: error-code, path: error-code/index.md, tag: folder, note: 错误码前缀分配 }
  - { name: code-quality, path: code-quality/index.md, tag: folder, note: 命名即文档 / 禁魔法值 等代码风格 }
  - { name: skill-authoring, path: skill-authoring/index.md, tag: folder, note: 写一条好 skill 的规约（Matt 心法本地化） }
when_to_descend: |
  任务涉及协作流：写 commit / 开 PR / 改 PRD / 新增错误码 / 写出可读代码。
  Step 8 PRD 同步 → 必读 prd-sync/。
---

# Habit · 流程习惯

> 状态：**W1 占位** —— 子目录 W2-W3 从 `.ai/skills/core/agent_workflow.md` 拆分而来 + 新写部分。

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| commit | 文件夹 | Conventional Commit / 在消息里 claim Issue |
| pr | 文件夹 | PR body 模板 / 一 PR 一子模块 |
| prd-sync | 文件夹 | 代码改 → PRD 同步规范（Step 8 必读） |
| error-code | 文件夹 | 错误码前缀分配 |

## 何时下钻

- 提交 commit / 写 commit message → `commit/`
- 开 PR / 写 PR body → `pr/`
- 代码改完执行 CLAUDE.md Step 8 → **必入 `prd-sync/`**
- 新增业务错误码 → `error-code/`

## 下钻决策表

| 任务 | 选哪个子项 |
|------|----------|
| CLAUDE.md Step 8 同步 PRD | prd-sync/update-on-code-change + prd-sync/manifest-yaml-sync |
| 收工写 commit | commit/conventional-commit + commit/claim-issue-in-message |
| 开 PR | pr/pr-body-template + pr/one-submodule-per-pr |
| 新增 V/I 系列错误码 | error-code/prefix-allocation |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行维度：[`../lang/index.md`](../lang/index.md) · [`../framework/index.md`](../framework/index.md) · [`../design-pattern/index.md`](../design-pattern/index.md)
- 完整协作流（W3 拆分到 commit/pr 之前的过渡引用）：[`/.ai/skills/core/agent_workflow.md`](../../../.ai/skills/core/agent_workflow.md)
