---
name: prd-triplet-rule
description: 三件套规范 — PRD + sketch + modules 三者必齐。Use when 改子模块 PRD / 评审涉及 `triplet-rule`
  的 PR。
parent: ./index.md
paths:
- project-index/modules/**
- design/**
triggers:
  keywords:
  - 三件套
  - sketch
  - modules.html
effort: medium
context: inline
version: '1.0'
---
# PRD Sync · 三件套规范

## 核心约束

PRD 模块以**三件套**为最小可交付单位：

- **#1 PRD 文档** — `project-index/modules/<name>.md`（扁平）或 `modules/<name>/README.md`（文件夹）
- **#2 页面草图** — `design/<name>-sketch.html`
- **#3 模块拆解页** — `design/<name>-modules.html`

三者缺一不可（**无 UI 模块可豁免 #2 sketch**，但 #3 拆解页必须有）。

## 状态约束

| 状态 | 三件套要求 | progress 上限 |
|------|----------|------------|
| `scaffold` | 占位 / 三件套不全 | 0% |
| `spec-ready` | 三件套齐全 | 起点 50% |
| `in-progress` / `active` | 三件套齐全 + 代码进展 | 50%~100% |

**三件套未齐全时 `status` 不得设为 `spec-ready`**。

## 新增 PRD 模块的标准 7 步

详见 `project-index/conventions.md` 第 2 节，简版：

```
1. 用 split_prd.md 技能拆解需求
2. 创建 modules/<name>.md（或 modules/<name>/README.md）
3. 创建 design/<name>-sketch.html
4. 创建 design/<name>-modules.html
5. 在 project-index/index.md 追加索引条目
6. 在 mapping/module_path_map.md 追加路径映射
7. 同步 design/prd-dashboard.html
```

## design/prd-dashboard.html 维护

每次以下操作必须同步刷新 prd-dashboard：

- 新增 PRD 模块
- 修改 status 或 progress
- 完成 / 新增一个 artifact（⬜ → ✅）
- 出现新阻塞项

刷新内容：顶部概览数字、模块卡进度条、产物清单勾选、阻塞项列表、最后更新日期。

## Progress 公式

| status | 公式 |
|--------|------|
| scaffold | 0 |
| 其他 | 50 + 50 × closed / total |

由 `scripts/build_snapshot.py` 自动派生，**不可手写**。详见 build_snapshot.py 顶部 docstring 与 `project-index/conventions.md` 第 4 节。

## 反例

```yaml
# ❌ 没草图就标 spec-ready
home_page:
  status: spec-ready
  progress: 60
  artifacts:
    - project-index/modules/home_page.md  ✅
    - design/home-sketch.html             ⬜
    - design/home-modules.html            ⬜
```

## 自检

- [ ] 三件套齐全才设 spec-ready？
- [ ] 手写 progress 数字了吗（不允许）？
- [ ] 新增模块跑了 7 步？
- [ ] prd-dashboard.html 刷新了吗？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`write-7-sections.md`](./write-7-sections.md) · [`split-method.md`](./split-method.md)
- 配套：`project-index/conventions.md` 第 2-4 节

