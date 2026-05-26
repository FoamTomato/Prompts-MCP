---
name: prd-map-requirements
description: 需求映射方法 — 用户需求 → 模块 + 子模块 + artifacts。Use when 改子模块 PRD / 评审涉及 `map-requirements-method`
  的 PR。
parent: ./index.md
paths:
- project-index/modules/**
triggers:
  keywords:
  - 需求映射
  - map
  - requirements
effort: medium
context: inline
version: '1.0'
---
# PRD Sync · 需求映射方法

## 用途

把用户的"业务需求 / 用户故事"翻译成 Quill 的 PRD 结构（模块 + 子模块 + artifacts）。

## 流程

```
用户原话："我想让老师能批量下载本月所有班级的课件作为压缩包"
        ↓
[需求理解] 关键词提取：
  - 角色：老师
  - 动作：批量下载
  - 范围：本月、所有班级
  - 输出：压缩包
        ↓
[模块定位] 这是 dashboard 模块的扩展（涉及 D5 MyPresentations）
        ↓
[子模块拆解]
  - D5.batch_download: 选择 + 批量下载按钮
  - 新增 D23 BatchExportModal: 选择范围对话框（月 / 班级 / 格式）
  - 复用 backend/services/exporters/: 压缩 + 上传 OSS
        ↓
[artifacts 落点]
  - frontend/src/features/dashboard/BatchExportModal.tsx
  - backend/routers/exports.py + backend/services/batch_exporter.py
  - py/services/oss.py 复用
        ↓
[依赖梳理]
  - 前置：anonymous_session（鉴权）+ ppt_generator（PPT 已生成）
  - 后置：无
        ↓
[PRD 7 章节填充]
```

## 关键技术

### 1. 找定位模块

读 `project-index/index.md` 模块速览表，按用户消息匹配 name / tags / description。

### 2. 找定位子模块

读 `project-index/modules/<module>/README.md` 子模块清单，找最接近的子模块。

### 3. 评估是新增还是扩展

| 情况 | 操作 |
|------|------|
| 完全新功能，与现有模块无交集 | 新建模块（命名 + 字母前缀） |
| 现有模块的延伸 | 在原模块加子模块（按字母序） |
| 多模块组合 | 在最相关的模块加，引用其他模块 |

### 4. 确认与用户

将拆解结果汇报给用户，确认无误后才动 PRD 文档：

> 我理解的需求是这样：
> - 落点：dashboard 模块（D 系列）
> - 新增子模块：D23 BatchExportModal
> - 修改子模块：D5（加批量选择能力）
> - 依赖：ppt_generator 必须已生成
> - 错误处理：单个失败不影响其他
>
> 是否准确？

## 工具协同

| 工具 | 用途 |
|------|------|
| `index.md` 速览 | 找定位模块 |
| `modules/<X>/README.md` | 找定位子模块 |
| `mapping/module_path_map.md` | 找已有实现路径 |
| `manifest.yaml` | 看 Issue 编号 |
| antd MCP | 查 UI 组件实现可能性 |

## 反例

```
用户："加个导出"
       ↓
❌ 直接开始写 ExportButton 组件
   （没确认：哪个模块的导出？什么格式？哪些数据？）

✅
- 询问：你说的导出是 ppt_generator 的单个 PPT 导出，还是 dashboard 的批量？
- 询问：要 docx / pdf / pptx 哪种？
- 询问：是否需要历史导出记录？
- 确认后才开 PRD
```

## 自检

- [ ] 用户原话已提炼成"角色 / 动作 / 范围 / 输出"？
- [ ] 定位到最相关的模块和子模块？
- [ ] 与用户确认拆解结果？
- [ ] 依赖前置 / 后置模块清晰？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`split-prd-method.md`](./split-prd-method.md) · [`user-story-template.md`](./user-story-template.md)

