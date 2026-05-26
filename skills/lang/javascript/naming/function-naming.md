---
name: javascript-function-naming
description: JS 函数 camelCase 动词开头。Use when 写 JavaScript 代码 / 评审涉及 `function-naming`
  的 PR。
parent: ./index.md
paths:
- '*.js'
- '*.ts'
triggers:
  keywords:
  - function
  - camelCase
  - 函数
  - 动词开头
effort: medium
context: inline
version: '1.0'
---
# JS · 函数命名

> Quill 主栈不用 Node/Express。本文件为未来引入 Node 服务的扩展点。

## 规则

| 规则 | 示例 |
|------|------|
| camelCase 动词开头 | `fetchUser` / `buildPayload` / `validateInput` |
| 异步函数同步命名 | `async function fetchUser()`（不加 async_ 前缀） |
| 私有用 `_` 前缀 | `_normalizeUrl` |
| 高阶函数返回再返回 | `createValidator` / `makeHandler` |
| 工厂函数 `create*` / `make*` | `createLogger(config)` |

## 反例

```js
// ❌ 名词开头
function user() {}

// ❌ 中文/拼音
function 获取用户() {}

// ❌ 缩写
function proc(x) {}

// ❌ PascalCase（那是类）
function GetUser() {}
```

## 自检

- [ ] camelCase 动词开头？
- [ ] 不是缩写 / 拼音？
- [ ] 类用 PascalCase，函数用 camelCase 区分？

## 相关

- 父：[`./index.md`](./index.md)

