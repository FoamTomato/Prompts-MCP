---
name: java-package-naming
description: Java 包命名 — 全小写、反域名前缀、按业务分包优先于按技术分层。Use when 新建 package / 规划工程目录结构 / 评审分包方式（业务 vs 技术）时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 包命名
  - package naming
  - 反域名
  - 全小写
  - 分包方式
  - package by feature
effort: medium
context: inline
version: '1.0'
---
# Java · 包命名

> 本条只管「package 怎么命名 + 怎么分包」。类名见 [`class-naming.md`](./class-naming.md)。

## 规则

| 规则 | 说明 | 示例 |
|------|------|------|
| 全小写 | 不用驼峰、不用下划线、不用大写 | `com.example.order` |
| 反域名前缀 | 用组织域名倒序保证全局唯一 | `com.example.app` |
| 单词不分隔 | 多词包名直接连写（避免下划线/驼峰） | `orderservice`（非 `order_service` / `orderService`） |
| 不用 Java 保留字 | `int` / `package` 等不能做包段 | 用 `internal` 等替代 |

## 分包方式：按业务优先于按技术

```text
// ✅ 按业务（package by feature）—— 高内聚，改一个功能只动一个包
com.example.order
 ├── Order.java
 ├── OrderService.java
 ├── OrderController.java
 └── OrderRepository.java
com.example.user
 └── ...
```

```text
// ⚠️ 按技术分层（package by layer）—— 改一个功能要散动多个包
com.example.controller   // 所有 Controller 堆一起
com.example.service
com.example.repository
com.example.model
```

> 争议点：传统三层 `controller/service/repository` 分包在小项目里直观，但功能一多就低内聚（一个需求横跨四个包）。业界（DDD / 微服务）更推**按业务分包**，让包边界对齐领域边界。团队已有约定时以约定为准，新工程优先按业务分。

## 反例

```java
// ❌ 大写 / 驼峰 / 下划线
package com.example.OrderService;
package com.example.order_service;

// ❌ 无反域名前缀，易与第三方包冲突
package order;
```

## 自检

- [ ] 包名全小写、无下划线、无驼峰？
- [ ] 有反域名前缀（如 `com.example.*`）保证唯一？
- [ ] 优先按业务分包，而非把所有 Controller/Service 按技术堆在一起？
- [ ] 没有用 Java 保留字作包段？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`class-naming.md`](./class-naming.md)（类名）
- 兄弟：[`method-naming.md`](./method-naming.md)（方法名）
