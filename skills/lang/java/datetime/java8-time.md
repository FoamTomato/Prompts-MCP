---
name: java-java8-time
description: 用 java.time（LocalDateTime/Instant/DateTimeFormatter）取代线程不安全的 SimpleDateFormat 与旧 Date/Calendar。Use when 写日期时间代码 / 格式化解析时间 / 评审旧 Date 用法时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - java.time
  - LocalDateTime
  - Instant
  - DateTimeFormatter
  - SimpleDateFormat 线程不安全
  - 日期时间 API
effort: medium
context: inline
version: '1.0'
---
# Java · java.time 取代旧日期 API

> 本条只管「用哪套 API 表达 / 格式化日期时间」。跨时区怎么存、怎么传递见 [`timezone-handling.md`](./timezone-handling.md)。

## 规则

旧的 `java.util.Date` / `Calendar` 可变且语义混乱，`SimpleDateFormat` **线程不安全**（共享实例并发解析会出错乱数据），一律改用 `java.time`：

| 你要表达的 | 用 |
|-----------|-----|
| 纯日期（生日 / 账单日） | `LocalDate` |
| 日期+时间，不带时区 | `LocalDateTime` |
| 时间线上的绝对时刻（时间戳） | `Instant` |
| 带时区的时刻 | `ZonedDateTime` |
| 时间段 / 两点之差 | `Duration`（时分秒）/ `Period`（年月日） |
| 格式化 / 解析 | `DateTimeFormatter`（不可变、**线程安全**，可做 static 常量） |

## 反例：旧 API + 共享 SimpleDateFormat

```java
// ❌ SimpleDateFormat 非线程安全，static 共享并发下抛异常或返回错值
private static final SimpleDateFormat SDF = new SimpleDateFormat("yyyy-MM-dd");
Date now = new Date();              // 可变、月份从 0 开始等坑
String s = SDF.format(now);         // 多线程并发 format/parse 数据错乱
```

## 正例：java.time + 共享 DateTimeFormatter

```java
// ✅ DateTimeFormatter 不可变、线程安全，可放 static 常量复用
private static final DateTimeFormatter FMT =
    DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

LocalDateTime now = LocalDateTime.now();
String s = now.format(FMT);
LocalDateTime parsed = LocalDateTime.parse("2026-06-02 10:30:00", FMT);

// ✅ 时间戳用 Instant；做加减用不可变链式 API（返回新对象）
Instant ts = Instant.now();
LocalDate due = LocalDate.now().plusDays(7);
```

## 自检

- [ ] 没有新增 `java.util.Date` / `Calendar` / `SimpleDateFormat`？
- [ ] 格式化 / 解析用 `DateTimeFormatter`（且作为 static 常量复用，不每次 new）？
- [ ] 纯日期用 `LocalDate`、绝对时刻用 `Instant`，而不是一律 `LocalDateTime`？
- [ ] 日期加减用 `plusXxx`/`minusXxx` 链式 API（结果是新对象，原对象不变）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`timezone-handling.md`](./timezone-handling.md)（Instant / ZonedDateTime 跨时区怎么存与传递）
