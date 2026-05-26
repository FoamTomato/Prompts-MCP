---
name: prd-write-7-sections
description: PRD 7 章节标准 — Overview / Inputs / Outputs / Assets / Deps / Execution
  / Success。Use when 改子模块 PRD / 评审涉及 `write-prd-7-sections` 的 PR。
parent: ./index.md
paths:
- project-index/modules/**
triggers:
  keywords:
  - PRD
  - Overview
  - 章节
effort: medium
context: inline
version: '1.0'
---
# PRD Sync · PRD 7 章节标准

## 模板结构

每个 PRD 文件必须有以下 7 个标准章节：

```markdown
# 模块名

## Overview
（一句话定位 + 3-5 行说明）

## Inputs
（用户输入 / 上游模块产出）

## Outputs
（本模块向下游交付什么）

## Required Assets
（依赖的 skill / 设计文档 / 第三方库）

## Dependencies
（前置模块清单 + 后置模块清单）

## Execution Steps
（按子模块顺序的实施步骤）

## Success Criteria
（验收清单 / 自检项）
```

## 文件夹格式的 README.md

文件夹格式（dashboard / ppt_generator）的 README.md 同样含 7 章节，**额外加子模块清单表**：

```markdown
## 子模块清单（22 个）

| ID | 子模块 | 路径 | 子分组 |
|----|--------|------|--------|
| D1 | DashboardLayout | [01-page-shell/D1-dashboard-layout.md](...) | Page Shell |
| D2 | SideNav | [02-side-nav/D2-side-nav.md](...) | Navigation |
| ... |
```

## 单子模块 .md（文件夹格式）

包含：

```markdown
---
sub_id: D6
title: PresentationCard
parent_module: dashboard
parent_readme: ../README.md
shared: [../_shared/layout.md, ../_shared/ui-spec.md]
issue: 78
artifacts: [frontend/src/features/dashboard/PresentationCard.tsx]
status: spec-ready
---

# D6 · PresentationCard（课件卡片）

## 功能
（核心功能描述）

## 关联
- 父模块 README
- 设计草图：design/dashboard-modules.html#D6
- manifest 条目：dashboard.submodules.D6（issue #78）
- 实现路径：frontend/src/features/dashboard/PresentationCard.tsx
- 错误码：（如有）

## Change Log
| 日期 | 改动 | commit |
|------|------|--------|
```

## Required Assets 引用新 skills 树

```markdown
## Required Assets
- skills:
  - lang/typescript/typing/strict-mode
  - framework/react/component/structure
  - framework/react/component/button-naming
  - framework/antd/setup/config-provider
- design:
  - design/dashboard-modules.html#D6
- prompts: (无)
```

## 反例

```markdown
# ❌ 缺章节
# DashboardLayout

直接写实现细节...   # 缺 Overview / Inputs / Outputs / ...
```

## 自检

- [ ] 7 章节齐全？
- [ ] Overview 是一句话定位（不超过 3 行）？
- [ ] Required Assets 引用新 .claude/skills/ 路径？
- [ ] Dependencies 列前置 + 后置模块？
- [ ] Success Criteria 是清单（可验收）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`triplet-rule.md`](./triplet-rule.md) · [`split-prd-method.md`](./split-prd-method.md)

