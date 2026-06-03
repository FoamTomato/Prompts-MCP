---
name: framework-react-layout-index
description: 页面结构约定索引——栅格 Row/Col 排版 + 布局容器 Layout/Space/Flex/Divider 选型。房规：每页必须由栅格 + 布局容器组成，禁裸 div 堆砌。
parent: ../index.md
children:
  - { name: grid-system, path: grid-system.md, tag: skill, note: Row/Col 24 栅格 + 响应式 gutter + 断点 }
  - { name: layout-containers, path: layout-containers.md, tag: skill, note: Layout/Space/Flex/Divider 容器选型 }
when_to_descend: |
  搭 / 改任意页面骨架时下钻。房规:页面必须由栅格(Row/Col)+ 布局容器(Layout/Space/Flex)组成,严禁用裸 div + 手写 style 堆砌排版。
  - 列/行排布、响应式分栏 → grid-system.md
  - 选哪种容器(整页框架 / 等距堆叠 / 弹性对齐 / 分隔) → layout-containers.md
---

# React · Layout 页面结构

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| grid-system | skill | Row/Col 24 栅格 + 响应式 gutter + 断点 |
| layout-containers | skill | Layout/Space/Flex/Divider 容器选型 |

## 何时下钻

- 要按列/行分栏、做响应式布局 → [`grid-system.md`](grid-system.md)
- 不确定用哪种容器(整页 Layout / 等距 Space / 弹性 Flex / 分隔 Divider)→ [`layout-containers.md`](layout-containers.md)
- 房规:每个页面骨架都由栅格 + 布局容器拼成,禁裸 div + 手写 style 堆砌

## 链接

- 上层:[`../index.md`](../index.md)
- 平行:[`../component/index.md`](../component/index.md) · [`../theming/index.md`](../theming/index.md)
- 跨引:[`../../antd/index.md`](../../antd/index.md)
