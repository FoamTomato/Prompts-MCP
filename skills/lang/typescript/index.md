---
name: lang-typescript-index
description: TypeScript 语言级规则索引（命名 / typing / async / module / style / error-handling）
parent: ../index.md
children:
  - { name: naming, path: naming/index.md, tag: folder, note: 文件名 / interface vs type / 命名风格 }
  - { name: typing, path: typing/index.md, tag: folder, note: strict mode / no any }
  - { name: async, path: async/index.md, tag: folder, note: no floating promise / async vs then }
  - { name: module, path: module/index.md, tag: folder, note: ESM only / barrel export }
  - { name: style, path: style/index.md, tag: folder, note: design tokens / 样式约定 }
  - { name: error-handling, path: error-handling/index.md, tag: folder, note: ApiError 子类 / Asserts 工具 / ErrorBoundary / 表单错误处理 }
when_to_descend: |
  写 / 改 .ts / .tsx 文件。
  错误处理任务（fetcher / 表单 / ErrorBoundary）→ error-handling。
---

# TypeScript · 语言级规则

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| naming | 文件夹 | 文件名 / interface / type alias / 命名风格 |
| typing | 文件夹 | strict mode + 禁 any |
| async | 文件夹 | 禁 floating promise / async vs then |
| module | 文件夹 | ESM only / barrel export |
| style | 文件夹 | design tokens / 样式约定 |
| **error-handling** | 文件夹 | **W3.5 新增**：ApiError + Asserts + ErrorBoundary + 表单错误 |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../python/index.md`](../python/index.md) · [`../sql/index.md`](../sql/index.md) · [`../javascript/index.md`](../javascript/index.md)
- 框架配套：[`../../framework/react/`](../../framework/react/index.md) · [`../../framework/antd/`](../../framework/antd/index.md)
