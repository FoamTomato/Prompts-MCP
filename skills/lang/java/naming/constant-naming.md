---
name: java-constant-naming
description: Java 常量命名 — UPPER_SNAKE_CASE 且 static final，一组相关常量优先用 enum 而非 int。Use when 声明常量 / 替换魔法值 / 评审 int 常量该不该改枚举时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 常量命名
  - constant naming
  - UPPER_SNAKE_CASE
  - static final
  - 枚举优先
  - enum vs int
effort: medium
context: inline
version: '1.0'
---
# Java · 常量命名

> 本条只管「常量怎么起名 + 该不该用枚举」。普通字段/变量见 [`variable-naming.md`](./variable-naming.md)；类名见 [`class-naming.md`](./class-naming.md)。

## 规则

| 场景 | 约定 | 示例 |
|------|------|------|
| 常量名 | **UPPER_SNAKE_CASE**，单词全大写下划线分隔 | `MAX_RETRY_COUNT` / `DEFAULT_TIMEOUT_MS` |
| 常量声明 | 必须 `static final`（类常量），含义不可变 | `public static final int MAX = 100;` |
| 一组相关取值 | **优先 enum，不用 int 常量** | `OrderStatus.PAID` 而非 `STATUS_PAID = 1` |
| 单个独立配置值 | `static final` 常量即可 | `static final String CHARSET = "UTF-8";` |

## 正例

```java
// ✅ 单个常量：UPPER_SNAKE_CASE + static final
public static final int MAX_RETRY_COUNT = 3;
public static final Duration DEFAULT_TIMEOUT = Duration.ofSeconds(5);

// ✅ 一组相关取值用枚举（类型安全、可带行为/字段）
public enum OrderStatus {
    PENDING, PAID, SHIPPED, CANCELLED;
}
```

## 反例

```java
// ❌ 大小写不对（看起来像普通变量）
static final int maxRetryCount = 3;        // 应为 MAX_RETRY_COUNT

// ❌ 漏 final，常量可被改写
static int MAX_RETRY_COUNT = 3;            // 应加 final

// ❌ 用 int 常量表达一组状态：无类型安全，可传任意 int
public static final int STATUS_PAID = 1;
public static final int STATUS_SHIPPED = 2;   // 应改 enum OrderStatus
```

## 自检

- [ ] 常量名是 UPPER_SNAKE_CASE？
- [ ] 声明为 `static final`（值不可变）？
- [ ] 一组相关取值用了 `enum` 而不是一堆 `int` / `String` 常量？
- [ ] 没有把可变配置硬塞成 `static final`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`variable-naming.md`](./variable-naming.md)（普通字段/变量名）
- 兄弟：[`method-naming.md`](./method-naming.md)（方法名）
- 兄弟：[`class-naming.md`](./class-naming.md)（类名，含 `*Status` 枚举命名）
