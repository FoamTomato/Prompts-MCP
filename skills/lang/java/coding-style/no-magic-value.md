---
name: java-no-magic-value
description: Java 禁魔法值 — 散落的数字/字符串字面量抽成常量、枚举或配置项。Use when 写 Java 业务判断 / 出现 if x == 3 这种字面量 / 评审散落常量的 PR 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 魔法值
  - magic number
  - 常量提取
  - static final
  - 枚举
  - Enum
effort: medium
context: inline
version: '1.0'
---
# Java · 禁魔法值

> 本条只管「字面量怎么抽」。命名好不好见 [`../naming/index.md`](../naming/index.md)；字符串拼接见 [`string-handling.md`](./string-handling.md)。

## 规则

代码里**禁止散落裸数字 / 字符串字面量**，按语义抽到下表对应载体：

| 字面量类型 | 抽成 |
|-----------|------|
| 业务状态 / 角色 / 类型（有限集合） | `enum` |
| 固定阈值 / 物理上限（重试次数、最大长度） | `public static final` 常量 |
| 环境相关（超时、URL、开关） | 配置项（`@Value` / `@ConfigurationProperties`） |
| 同模块复用的提示文案 | 常量或资源文件 |

## 正例

```java
// 有限取值集合 → 枚举
public enum OrderStatus {
    PENDING, PAID, CANCELLED
}
if (order.getStatus() == OrderStatus.PENDING) { ... }

// 固定阈值 → 常量
private static final int MAX_RETRY = 3;
private static final long ONE_DAY_MILLIS = 24L * 60 * 60 * 1000;

// 环境相关 → 配置注入
@Value("${order.timeout-seconds}")
private int timeoutSeconds;
```

## 反例

```java
// ❌ 3 是什么？两年后没人知道
if (user.getRole() == 3) { ... }

// ❌ 字符串字面量散落，拼错编译期发现不了
if ("pending".equals(order.getStatus())) { ... }

// ❌ 一天毫秒数硬编码，含义靠注释
Thread.sleep(86400000);
```

- 裸数字 / 字符串无法表达意图，改一处要全局搜替。
- 字符串字面量拼错不报错，只在运行时静默失配。

## 唯一例外

| 例外 | 为什么 |
|------|--------|
| `0` / `1`（计数 / index / 边界） | 含义明显 |
| 空串 `""` / `null` 的特定语义 | 含义明显 |
| 单元测试里的样本数据 | 测试上下文已足够清晰 |
| 数学常量（如 `Math.PI`） | 标准库已有或含义已知 |

## 自检

- [ ] 有限取值集合用 `enum` 而非散落 int / String？
- [ ] 固定阈值用 `static final` 命名常量？
- [ ] 环境相关值走配置注入，没硬编码？
- [ ] 没有 `if x == 3` / `"pending".equals(...)` 这种裸字面量？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`string-handling.md`](./string-handling.md)（字符串字面量比较与拼接）
- 跨维度：[`../../../habit/code-quality/no-magic-values.md`](../../../habit/code-quality/no-magic-values.md)（跨语言通则：枚举 / 常量分类）
