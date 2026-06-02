---
name: prd-review-checklist
description: Review PRD 清单 — 章节完整 / 边界清晰 / artifacts 可追溯。Use when 改子模块 PRD / 评审涉及
  `review-prd-checklist` 的 PR。
parent: ./index.md
paths:
- project-index/modules/**
triggers:
  keywords:
  - Review PRD
  - review
  - checklist
  - 清单
  - 章节完整
  - 边界清晰
effort: medium
context: inline
version: '1.0'
---
# PRD Sync · Review PRD 清单

## 通过条件

PRD 通过 Review 必须满足以下全部：

### 章节完整性

- [ ] 7 章节齐全（Overview / Inputs / Outputs / Required Assets / Dependencies / Execution Steps / Success Criteria）？
- [ ] Overview 一句话定位（≤ 3 行）？
- [ ] Inputs / Outputs 双向都填了？

### 三件套齐全

- [ ] PRD 文档？
- [ ] sketch.html 草图（含状态切换演示）？
- [ ] modules.html 拆解页（卡片网格 + 抽屉详情）？

### 子模块拆解

- [ ] 字母前缀分配 + 未冲突？
- [ ] 每个子模块单一职责？
- [ ] 每个子模块 1-3 人天工作量？
- [ ] 子模块依赖关系清晰？

### artifacts 列表

- [ ] 列出关键文件路径（不漏）？
- [ ] artifacts 与 module_path_map.md 一致？
- [ ] 与 manifest.yaml 的 submodule.artifacts 一致？

### 依赖

- [ ] 前置模块清单清晰（如 "需要 anonymous_session"）？
- [ ] 后置模块清单清晰（如 "被 dashboard D5 消费"）？
- [ ] 无循环依赖？

### 错误处理

- [ ] 错误场景列举（参数错 / 资源不存在 / 配额不足 / 外部失败）？
- [ ] 错误码前缀分配（S/R/AC/B/V/I）？

### 性能 / 可访问性

- [ ] 列表 > 50 行考虑服务端分页？
- [ ] 大文件考虑分块 / 流式？
- [ ] 含动画的模块标 prefers-reduced-motion 兼容？
- [ ] 含可交互元素标 a11y 要求？

### 注册到 index

- [ ] `project-index/index.md` 模块速览表追加条目？
- [ ] `project-index/mapping/module_path_map.md` 追加路径映射？
- [ ] `design/prd-dashboard.html` 追加模块卡？

### 状态与 Progress

- [ ] 三件套齐 → status: spec-ready / progress: 50%（公式自动）？
- [ ] 子模块全部 Issue close → progress 自动 100%？

## Review 流程

```
1. PRD 作者自检（用本清单）
2. 提 PR（关联 PRD 文件）
3. Reviewer 走清单
4. 标 review comment（缺哪项）
5. 作者修正
6. 通过 → merge
```

## 反例

```
❌ 7 章节其中 3 章只写"待补"
❌ 子模块清单缺字母前缀
❌ artifacts 列出不存在的文件
❌ Dependencies 漏写前置
❌ 三件套只有 PRD，sketch / modules.html 没建
```

## 自检（作者侧）

- [ ] PRD 自查清单全部 ✅？
- [ ] 草图 sketch 含状态切换演示？
- [ ] manifest.yaml 同步更新？
- [ ] prd-dashboard.html 刷新？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`write-prd-7-sections.md`](./write-prd-7-sections.md) · [`triplet-rule.md`](./triplet-rule.md)

