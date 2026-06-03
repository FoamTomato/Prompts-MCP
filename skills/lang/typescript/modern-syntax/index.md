---
name: lang-typescript-modern-syntax-index
description: ES2022+/TS 新语法采用 — 数组对象新方法（at/findLast/groupBy）+ TS 专属运算符（satisfies/using）两个决策点。Use when 想用新数组对象方法替代旧写法 / 用 satisfies 校验配置 / using 释放资源时。
parent: ../index.md
children:
  - { name: array-object-methods, path: array-object-methods.md, tag: skill, note: ES2022+ at/findLast/groupBy/structuredClone }
  - { name: ts-operators, path: ts-operators.md, tag: skill, note: satisfies + using 资源管理 }
when_to_descend: |
  想用新数组 / 对象方法（at / findLast / Object.groupBy / structuredClone）→ array-object-methods。
  想用 TS satisfies 约束字面量、或 using / await using 自动释放资源 → ts-operators。
  ?. / ?? 这类 null-safety 运算符不在这层，去 typing / naming 维度。
---

# TypeScript · Modern Syntax

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| array-object-methods | skill | ES2022+ 标准库新方法：at / findLast / Object.groupBy / structuredClone |
| ts-operators | skill | TS 专属运算符：satisfies 类型约束 + using 资源管理 |

## 何时下钻

- 取末尾元素、倒序查找、按 key 分组、深拷贝对象 → array-object-methods（标准库 runtime 方法）。
- 想让字面量既被类型校验又保留窄类型推断（不用类型注解吞掉推断）→ ts-operators 的 satisfies。
- 资源（文件句柄 / 连接 / 锁）需作用域结束自动释放、避免手写 try/finally → ts-operators 的 using / await using。
- 只是 `?.` 可选链 / `??` 空值合并 → 不在本层，属 null-safety，去上层其他维度。

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../typing/index.md`](../typing/index.md) · [`../async/index.md`](../async/index.md) · [`../naming/index.md`](../naming/index.md)
- 跨引：[`../../javascript/index.md`](../../javascript/index.md)
