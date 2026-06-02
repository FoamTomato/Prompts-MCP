---
name: java-string-handling
description: Java 字符串处理 — 循环拼接用 StringBuilder、比较用 equals 不用 ==、多变量格式化用 String.format、空判断用 isEmpty/isBlank。Use when 在循环里拼字符串 / 比较两个字符串 / 判断字符串是否为空时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 字符串拼接
  - StringBuilder
  - 字符串比较
  - String.format
  - isEmpty
  - isBlank
effort: medium
context: inline
version: '1.0'
---
# Java · 字符串处理

> 本条管字符串的拼接 / 比较 / 空判断。字符串字面量该不该抽常量见 [`no-magic-value.md`](./no-magic-value.md)。

## 规则

| 场景 | 做法 |
|------|------|
| 循环 / 大量拼接 | `StringBuilder.append`，**禁循环里 `+=`** |
| 少量定值拼接 | 直接 `+` 即可（编译器优化），无需 StringBuilder |
| 比较内容相等 | `a.equals(b)`，**禁 `==`**（== 比的是引用） |
| 多变量格式化 | `String.format` / 文本块，胜过一长串 `+` |
| 判断空 | 只判空用 `isEmpty()`；连空白也算空用 `isBlank()`（JDK 11+） |
| 比较时防 null | 已知常量放左边：`"PAID".equals(status)` |

## 正例

```java
// 循环拼接用 StringBuilder
StringBuilder sb = new StringBuilder();
for (Item it : items) {
    sb.append(it.getName()).append(',');
}
String csv = sb.toString();

// 内容比较用 equals；多变量用 format
if ("PAID".equals(order.getStatus())) { ... }
String msg = String.format("订单 %s 金额 %.2f", id, amount);

// 空判断
if (name == null || name.isBlank()) {   // 拦截 null、""、"   "
    throw new BusinessException("名称不能为空");
}
```

## 反例

```java
// ❌ 循环里 += 每次都新建 String 对象，O(n²)
String csv = "";
for (Item it : items) { csv += it.getName() + ","; }

// ❌ == 比较内容：堆上不同对象即便内容相同也 false
if (status == "PAID") { ... }

// ❌ 一长串 + 拼出来可读性差，易漏空格/类型错
String msg = "订单 " + id + " 金额 " + amount;
```

## 自检

- [ ] 循环里的字符串拼接用了 `StringBuilder`，没有 `+=`？
- [ ] 字符串内容比较用 `equals`，没有 `==`？
- [ ] 多变量拼接用 `String.format` / 文本块而非长串 `+`？
- [ ] 空判断按需用 `isEmpty` / `isBlank`，且先防了 null？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`no-magic-value.md`](./no-magic-value.md)（字符串字面量抽常量）
- 兄弟：[`null-safety.md`](./null-safety.md)（比较前防 null、Objects.equals）
