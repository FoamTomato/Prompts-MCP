---
name: java-timezone-handling
description: 跨时区时刻的存储与传递约定 — 内部统一存 UTC/Instant、ZoneId 显式指定、前后端传 ISO-8601 字符串、数据库存 UTC timestamp。Use when 处理跨时区时间 / 设计时间字段的存储与接口格式 / 排查时间差 8 小时类 bug 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 时区处理
  - timezone
  - ZoneId
  - Instant UTC
  - ISO-8601
  - ZonedDateTime
effort: medium
context: inline
version: '1.0'
---
# Java · 时区处理约定

> 本条只管「带时区的时刻怎么存、怎么传」。基础 API 选型（LocalDateTime vs Instant）见 [`java8-time.md`](./java8-time.md)。

## 规则

| 环节 | 约定 |
|------|------|
| 内部存储 / 运算 | 用 `Instant`（UTC 绝对时刻），不带本地时区漂移 |
| 转本地时间 | 必须**显式** `ZoneId`，禁用 `ZoneId.systemDefault()`（依赖部署机器，环境间不一致）|
| 前后端传递 | ISO-8601 字符串（如 `2026-06-02T10:30:00Z` 或带偏移 `+08:00`），不传时间戳裸数字 / 不传无时区的本地串 |
| 数据库存储 | 存 UTC 的 `timestamp`（或 `TIMESTAMP WITH TIME ZONE`），统一 UTC 入库、展示时再按用户时区转换 |

核心原则：**存与算用 UTC，只在展示边界按显式时区转换。**

## 反例：依赖系统默认时区

```java
// ❌ systemDefault 取决于 JVM 所在机器，本地跑对了线上差 8 小时
ZonedDateTime z = instant.atZone(ZoneId.systemDefault());

// ❌ 把无时区的 LocalDateTime 直接当成 UTC 或本地存库 / 传出，含义全靠猜
String wire = LocalDateTime.now().toString();   // "2026-06-02T10:30" 没有时区信息
```

## 正例：UTC 存储 + 显式时区展示

```java
// ✅ 入库 / 运算用 UTC Instant
Instant createdAt = Instant.now();

// ✅ 接口输出 ISO-8601（带 Z 表示 UTC，信息自包含）
String wire = createdAt.toString();             // "2026-06-02T10:30:00Z"

// ✅ 展示给用户时按显式时区转换
ZoneId userZone = ZoneId.of("Asia/Shanghai");
ZonedDateTime shown = createdAt.atZone(userZone);

// ✅ 接收方按 ISO-8601 解析回 Instant
Instant back = Instant.parse("2026-06-02T10:30:00Z");
```

## 自检

- [ ] 存储与运算用 `Instant`（UTC），而非带隐含本地时区的 `LocalDateTime`？
- [ ] 所有 `ZoneId` 都显式指定（`ZoneId.of("Asia/Shanghai")`），没有 `systemDefault()`？
- [ ] 前后端 / 接口传递用带时区信息的 ISO-8601 字符串？
- [ ] 数据库统一存 UTC timestamp，仅展示时按用户时区转换？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`java8-time.md`](./java8-time.md)（Instant / ZonedDateTime / LocalDateTime 的基础 API 选型）
