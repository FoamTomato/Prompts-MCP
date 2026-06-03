---
name: design-pattern-react-patterns-index
description: "React 组件设计模式(前端视角) — 复合组件 / 自定义 hook 抽逻辑 / render props headless / Provider context / 容器展示分离。Use when 设计复杂组件 API / 复用跨组件逻辑 / 共享跨层级状态 / 解耦数据与展示时。"
parent: ../index.md
children:
  - { name: design-pattern-react-compound-components, path: compound-components.md, tag: skill, note: "复合组件: 父子隐式协作共享上下文, 灵活组合式 API" }
  - { name: design-pattern-react-custom-hook-extraction, path: custom-hook-extraction.md, tag: skill, note: "自定义 hook 抽离副作用/状态逻辑, useXxx 复用" }
  - { name: design-pattern-react-render-props-headless, path: render-props-headless.md, tag: skill, note: "render props / headless: 逻辑与 UI 解耦, 调用方控制渲染" }
  - { name: design-pattern-react-provider-context, path: provider-context.md, tag: skill, note: "Provider + Context 共享跨层级状态, 避免 prop drilling" }
  - { name: design-pattern-react-container-presentational, path: container-presentational.md, tag: skill, note: "容器/展示分离: 数据获取与纯渲染各司其职" }
when_to_descend: 设计复杂组件 API、复用跨组件逻辑、共享跨层级状态、解耦数据与展示时
---

# Design Pattern · React 组件设计模式

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| compound-components | skill | 父子隐式协作共享上下文，组合式灵活 API（Tabs/Select 风格） |
| custom-hook-extraction | skill | 把副作用与状态逻辑抽成 `useXxx`，跨组件复用 |
| render-props-headless | skill | 逻辑与 UI 解耦，逻辑层只给数据、渲染交调用方 |
| provider-context | skill | Provider + Context 共享跨层级状态，消除 prop drilling |
| container-presentational | skill | 数据获取（容器）与纯渲染（展示）职责分离 |

## 何时下钻

| 你在做什么 | 进哪个 |
|-----------|-------|
| 设计一组父子配合、对外暴露组合式 API 的组件（如自定义 Tabs/Menu/Form） | [compound-components](compound-components.md) |
| 多个组件重复同一段 `useState`/`useEffect`/订阅逻辑，想抽出复用 | [custom-hook-extraction](custom-hook-extraction.md) |
| 一段交互逻辑要配多种不同 UI，想把渲染权交给调用方 | [render-props-headless](render-props-headless.md) |
| 主题/登录态/i18n 等跨多层级共享，prop 一路透传太痛苦 | [provider-context](provider-context.md) |
| 组件里数据请求与展示揉在一起，想拆成"取数 + 纯展示" | [container-presentational](container-presentational.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行模式：[`../solid/index.md`](../solid/index.md) · [`../behavioral/index.md`](../behavioral/index.md)
- 用法侧：[`../../framework/react/component/index.md`](../../framework/react/component/index.md)
