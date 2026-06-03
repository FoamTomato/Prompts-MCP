---
name: framework-react-index
description: React 组件 / Hook / 状态 / 错误处理 / 主题 / 布局 / 反馈 / 可靠性 / 性能 / 安全 / 新特性 / 无障碍 / 国际化 / 文件 使用约定索引
parent: ../index.md
children:
  - { name: component, path: component/index.md, tag: folder, note: 组件结构 / 命名 / 分层 / 渲染坑 / 受控 }
  - { name: hook, path: hook/index.md, tag: folder, note: 自定义 Hook 规范 / useEffect 边界 }
  - { name: state, path: state/index.md, tag: folder, note: 状态分层（local / context / zustand） }
  - { name: error-handling, path: error-handling/index.md, tag: folder, note: 路由级 + 区域级 ErrorBoundary }
  - { name: theming, path: theming/index.md, tag: folder, note: 主题色板 / dark mode / token }
  - { name: layout, path: layout/index.md, tag: folder, note: 栅格 Row/Col + 布局容器（房规） }
  - { name: feedback, path: feedback/index.md, tag: folder, note: Skeleton 骨架屏 + Empty 空态（房规） }
  - { name: reliability, path: reliability/index.md, tag: folder, note: 竞态取消 / 清理泄漏 / 防重 / chunk 恢复 }
  - { name: performance, path: performance/index.md, tag: folder, note: 虚拟列表 / 代码分割 / Core Web Vitals }
  - { name: security, path: security/index.md, tag: folder, note: XSS 消毒 / token 存储 / open redirect }
  - { name: react19, path: react19/index.md, tag: folder, note: use/Actions/并发/Compiler 新特性 }
  - { name: a11y, path: a11y/index.md, tag: folder, note: 语义 ARIA + 键盘焦点 }
  - { name: i18n, path: i18n/index.md, tag: folder, note: 占位符模板 / 复数 / locale 格式化 / RTL }
  - { name: file, path: file/index.md, tag: folder, note: 分片上传 / createObjectURL 泄漏 / 流式下载 }
when_to_descend: |
  写 / 改 `frontend/src/**/*.tsx`、`frontend/src/**/*.ts` 中 React 组件、Hook、状态、主题、布局、反馈、可靠性、性能、安全、新特性、无障碍、国际化、文件相关代码。
---

# React · 使用约定

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| component | 文件夹 | 组件结构 / 命名 / 分层 / 渲染坑 / 受控 |
| hook | 文件夹 | 自定义 Hook + useEffect 边界 |
| state | 文件夹 | 状态分层选型 |
| error-handling | 文件夹 | 路由级 + 区域级 ErrorBoundary |
| theming | 文件夹 | 主题色板与 token |
| layout | 文件夹 | 栅格 + 布局容器（房规） |
| feedback | 文件夹 | 骨架屏 + 空态（房规） |
| reliability | 文件夹 | 竞态取消 / 清理泄漏 / 防重 / chunk 恢复 |
| performance | 文件夹 | 虚拟列表 / 代码分割 / Core Web Vitals |
| security | 文件夹 | XSS 消毒 / token 存储 / 跳转安全 |
| react19 | 文件夹 | use / Actions / 并发 / Compiler 新特性 |
| a11y | 文件夹 | 语义 ARIA + 键盘焦点 |
| i18n | 文件夹 | 占位符模板 / 复数 / 格式化 / RTL |
| file | 文件夹 | 分片上传 / 预览泄漏 / 流式下载 |

## 何时下钻

- 写新组件 / 渲染坑 / 受控输入 → `component/index.md` 起步
- 抽取共享逻辑成 Hook → `hook/index.md`
- 数据流跨多层 → `state/index.md` 选型
- 路由级或区域级异常处理 → `error-handling/index.md`
- 配色 / 暗色模式 → `theming/index.md`
- 搭页面布局 / 分列 / 选容器（房规）→ `layout/index.md`
- 加载态或空数据展示（房规）→ `feedback/index.md`
- 数据乱序 / 卸载报错 / 重复提交 / 部署后白屏 → `reliability/index.md`
- 列表卡顿 / 首屏慢 / 布局抖动 → `performance/index.md`
- 渲染用户内容 / 存登录态 / 做跳转 → `security/index.md`
- 用 use / Actions / 并发 / Compiler 新写法 → `react19/index.md`
- 无障碍语义 / 键盘焦点 → `a11y/index.md`
- 多语言文案 / 本地化格式化 → `i18n/index.md`
- 文件上传 / 图片预览 / 大文件下载 → `file/index.md`

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../antd/index.md`](../antd/index.md) · [`../gsap/index.md`](../gsap/index.md)
