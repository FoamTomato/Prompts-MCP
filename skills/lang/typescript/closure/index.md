---
name: lang-typescript-closure-index
description: TypeScript 原生闭包坑索引 — 循环变量捕获 / 异步回调延迟读值 / 闭包内存泄漏。Use when 写循环内回调 / 写定时器或事件监听 / 设计缓存闭包时下钻。
parent: ../index.md
children:
  - { name: pitfalls, path: pitfalls.md, tag: skill, note: 循环 var 共享绑定 / setTimeout 闭包延迟读值 / 闭包内存泄漏 }
when_to_descend: |
  写循环内回调 / 定时器 / 事件监听 / 缓存闭包时。
---

# TypeScript · Closure 子项索引

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| pitfalls | skill | 循环 var 共享绑定 / setTimeout 闭包延迟读值 / 闭包内存泄漏 |

## 何时下钻

- 在循环体内创建回调 / 闭包(map、定时器、监听器)，担心捕获到同一变量
- 写 setTimeout / setInterval 异步回调,回调执行时读到的是延迟后的值
- 注册事件监听 / 长生命周期闭包,持有大对象或 DOM 引用导致内存泄漏

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../async/`](../async/index.md) · [`../typing/`](../typing/index.md) · [`../style/`](../style/index.md)
- 框架配套：[`../../../framework/react/`](../../../framework/react/index.md)
