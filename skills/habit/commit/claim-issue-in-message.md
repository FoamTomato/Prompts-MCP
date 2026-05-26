---
name: commit-claim-issue
description: '习惯 · commit: commit 消息里 claim Issue'
parent: ./index.md
paths:
- .git/**
- '**'
triggers:
  keywords:
  - Issue
  - '#N'
  - claim
  - feat
  - 消息里
effort: medium
context: inline
version: '1.0'
---
# Commit · 在消息里 claim Issue

## 规则

实施任务的 commit 在 message body 或 footer **关联 Issue 编号**：

```
feat(D6):实现 PresentationCard 卡片

- 三类按钮命名遵循 react/component/button-naming
- antd Table 配合卡片缩略图

Closes #78
```

## 关键词

| 关键词 | 行为 |
|--------|------|
| `Closes #N` | merge 后自动 close Issue（推荐用 close） |
| `Fixes #N` | 同上（bug 修复语境） |
| `Refs #N` | 仅关联不关闭（中间提交） |
| `See #N` | 弱关联（讨论里提到） |

## 一 PR 一 Issue 原则

详见 [`../pr/one-submodule-per-pr.md`](../pr/one-submodule-per-pr.md)（如不存在则参考 agent_workflow.md）。

一个 PR 关闭一个子模块的 Issue。中间多个 commit 用 `Refs #N`，最后合并时 PR description 用 `Closes #N`。

## Quill 子模块编号映射

详见 `project-index/manifest.yaml`：

```yaml
home_page:
  submodules:
    H1: {issue: 54, ...}
    H2: {issue: 55, ...}
```

commit 时 commit message body 写 `Refs #54`，scope 用 `H1`。

## 反例

```
# ❌ 无关联
feat:实现登录

# ❌ 仅 Issue 号无关键词
feat:实现登录
#54

# ❌ 错的关键词（github 不认）
feat:实现登录
Linked to #54

# ✅
feat(H1):实现登录页

Closes #54
```

## 自检

- [ ] commit / PR 关联了 Issue #N？
- [ ] 用 GitHub 识别的关键词（Closes / Fixes / Refs）？
- [ ] 一 PR 一子模块？
- [ ] scope 用子模块编号？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`conventional-commit.md`](./conventional-commit.md)
- 配套：[`../pr/quill-start-usage.md`](../pr/quill-start-usage.md)

