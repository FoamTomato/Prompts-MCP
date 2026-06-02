---
name: lang-java-datetime-index
description: Java 日期时间两件事 — 用 java.time 取代旧 Date/Calendar/SimpleDateFormat / 跨时区的存储与传递约定。Use when 写 Java 日期时间代码 / 处理时区 / 评审 LocalDateTime、Instant、时区相关 PR 时。
parent: ../index.md
children:
  - { name: java8-time, path: java8-time.md, tag: skill, note: 禁用 Date/Calendar/SimpleDateFormat，改用线程安全的 java.time }
  - { name: timezone-handling, path: timezone-handling.md, tag: skill, note: 存储用 UTC/Instant、显式 ZoneId、传递用 ISO-8601 }
when_to_descend: 写 / 评审任何涉及日期、时间、时区的 Java 代码
---

# Datetime · 子项索引

日期时间拆成两个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 选用哪套 API 表达 / 格式化日期时间（旧 Date/Calendar 还是 java.time） | [java8-time](java8-time.md) |
| 决定怎么存、怎么在前后端 / 数据库之间传递带时区的时刻 | [timezone-handling](timezone-handling.md) |
