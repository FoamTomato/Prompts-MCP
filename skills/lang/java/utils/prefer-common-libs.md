---
name: java-prefer-common-libs
description: 通用工具优先用成熟库别造轮子 — Hutool / Guava / Apache Commons Lang3 的 StringUtils、CollectionUtils、ObjectUtils 对照。Use when 想自己写 isEmpty / 判空 / 集合判空 / null 处理时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 判空
  - isEmpty
  - StringUtils
  - CollectionUtils
  - ObjectUtils
  - Hutool
  - Guava
  - Apache Commons Lang3
effort: low
context: inline
version: '1.0'
---
# Java · 优先用成熟库别造轮子

> 本条只管「通用小工具该用哪个库而非手写」。自己确实要写工具类时的结构见 [`utility-class-design.md`](./utility-class-design.md)；Bean 拷贝见 [`bean-copy.md`](./bean-copy.md)。

## 规则

判空、集合操作、null 处理这类通用逻辑，**一律调成熟库**，不要在每个项目里重写一遍 `isEmpty`。手写版本边界条件（null / 空白串 / null 元素）容易漏，且各处实现不一致。

成熟库选型（已引入哪个就用哪个，避免同项目混用多套）：

| 库 | 定位 |
|----|------|
| Apache Commons Lang3 | 字符串 / 对象判空，最常见，`org.apache.commons.lang3.*` |
| Google Guava | 集合构造、`Preconditions` 校验、不可变集合 |
| Hutool | 国内常用全家桶，API 中文友好，`cn.hutool.core.util.*` |

## 常用方法对照表

| 你想干什么 | 别手写 | 用 |
|-----------|--------|-----|
| 字符串是否为 null 或 ""  | `s == null \|\| s.isEmpty()` | `StringUtils.isEmpty(s)` |
| 字符串是否为 null/""/空白 | 手写 trim 判断 | `StringUtils.isBlank(s)` |
| 集合是否为 null 或空 | `c == null \|\| c.isEmpty()` | `CollectionUtils.isEmpty(c)` |
| Map 是否为 null 或空 | 同上 | `MapUtils.isEmpty(m)` |
| 取默认值（null 兜底） | 三目运算 | `ObjectUtils.defaultIfNull(v, def)` |
| 对象 / 数组判空 | 各种 null 判断 | `ObjectUtils.isEmpty(o)` |
| 参数前置校验 | 手写 if-throw | `Preconditions.checkArgument(cond, msg)`（Guava） |

> `StringUtils` 指 `org.apache.commons.lang3.StringUtils`；Spring 项目也可用 `org.springframework.util.StringUtils`，但语义略不同（如 Spring 版无 `isBlank`），同一项目内别混用两套。

## 反例

```java
// ❌ 在第 N 个项目里又手写一遍判空，且漏了 isBlank 语义（" " 会被当非空）
public static boolean isEmpty(String s) {
    return s == null || s.length() == 0;
}

// ❌ 集合判空也手写，且没防 null
if (list.size() == 0) { ... }   // list 为 null 直接 NPE
```

## 正例

```java
// ✅ 直接用库，语义清晰、边界正确、全项目一致
if (StringUtils.isBlank(name)) {
    throw new BusinessException("名称不能为空", 400);
}
if (CollectionUtils.isEmpty(orders)) {
    return Collections.emptyList();
}
String region = ObjectUtils.defaultIfNull(req.getRegion(), "CN");
```

## 自检

- [ ] 没有手写 `isEmpty` / `isBlank` / 集合判空？已替换为库方法？
- [ ] 判空覆盖了 null + 空 + （字符串场景）空白串？
- [ ] 同一项目没有混用 Apache 与 Spring 的同名 `StringUtils`？
- [ ] 引入的库是项目已有依赖，没为一个判空新增整套依赖？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`utility-class-design.md`](./utility-class-design.md)（确实没有现成轮子、要自己写时的类结构）
- 兄弟：[`bean-copy.md`](./bean-copy.md)（拷贝也属"别造轮子"，但有专门选型）
