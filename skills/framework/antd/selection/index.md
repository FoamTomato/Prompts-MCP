---
name: framework-antd-selection-index
description: antd 组件选型索引，按 UX 任务给「用哪个 antd 组件」的决策入口，涵盖浮层 / 输入 / 数据展示 / 反馈 / 导航五类。Use when 已定用 antd 但不确定用哪个具体组件承载某个 UX 任务 / 在 Modal-Drawer-Popover 等近义组件间纠结 / 选错组件想纠偏。
parent: ../index.md
children:
  - { name: overlay-selection, path: overlay-selection.md, tag: skill, note: 浮层选型 Modal / Drawer / Popconfirm / Popover / Tooltip }
  - { name: input-selection, path: input-selection.md, tag: skill, note: 输入选型 Select / Cascader / TreeSelect / AutoComplete / Radio / Checkbox / Switch / Segmented }
  - { name: data-display-selection, path: data-display-selection.md, tag: skill, note: 数据展示选型 Table / List / Descriptions / Card / Tree }
  - { name: feedback-selection, path: feedback-selection.md, tag: skill, note: 反馈选型 message / notification / Alert / Result }
  - { name: navigation-selection, path: navigation-selection.md, tag: skill, note: 导航选型 Tabs / Steps / Menu / Breadcrumb }
when_to_descend: |
  已确定用 antd（见 ../when-antd-vs-custom.md）但不确定用哪个具体组件承载某个 UX 任务。
  按 UX 任务归类下钻：要弹出层选浮层、要采集值选输入、要呈现选数据展示、要给状态反馈选反馈、要切换位置选导航。
---

# antd · 组件选型索引

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| overlay-selection | skill | 浮层：Modal / Drawer / Popconfirm / Popover / Tooltip 怎么选 |
| input-selection | skill | 输入采集：Select / Cascader / TreeSelect / AutoComplete / Radio / Checkbox / Switch / Segmented 怎么选 |
| data-display-selection | skill | 数据展示:Table / List / Descriptions / Card / Tree 怎么选 |
| feedback-selection | skill | 状态反馈:message / notification / Alert / Result 怎么选 |
| navigation-selection | skill | 导航切换:Tabs / Steps / Menu / Breadcrumb 怎么选 |

## 何时下钻

- 要在当前页面之上弹出内容（确认 / 表单 / 提示 / 菜单）→ `overlay-selection.md`
- 要让用户从候选集里选值或开关状态 → `input-selection.md`
- 要把一份数据只读地呈现给用户看 → `data-display-selection.md`
- 要告诉用户操作的结果 / 加载 / 进度状态 → `feedback-selection.md`
- 要在多个视图 / 步骤 / 页面间切换位置 → `navigation-selection.md`

## 链接

- 上层：[`../index.md`](../index.md)
- 前置：[`../when-antd-vs-custom.md`](../when-antd-vs-custom.md)（先定用 antd 再来选组件）
- 不确定 API：[`../antd-mcp-usage.md`](../antd-mcp-usage.md)
