---
name: java-utility-class-design
description: 自己写的工具类标准结构 — final class + 私有构造防实例化 + 全 static 方法 + 无状态，命名 *Utils/*Helper。Use when 新建 XxxUtils 工具类 / 抽公共静态方法 / 评审工具类设计时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 工具类
  - utility class
  - 私有构造
  - private constructor
  - static 方法
  - Utils
  - Helper
effort: low
context: inline
version: '1.0'
---
# Java · 工具类设计

> 本条只管「自己写工具类时类结构怎么定」。优先用现成库别造轮子见 [`prefer-common-libs.md`](./prefer-common-libs.md)；Bean 拷贝见 [`bean-copy.md`](./bean-copy.md)。

## 规则

| 维度 | 要求 |
|------|------|
| 类修饰 | `public final class`，禁被继承 |
| 构造器 | **唯一一个 `private` 空构造**，防实例化 |
| 方法 | 全部 `public static`，纯函数，不依赖实例字段 |
| 状态 | **无可变状态**；常量用 `private static final`，集合常量要不可变 |
| 命名 | `*Utils`（工具）/ `*Helper`（带上下文的辅助），与领域名词搭配如 `DateUtils` |

## 正例

```java
public final class DateUtils {

    private static final DateTimeFormatter ISO_DATE =
            DateTimeFormatter.ofPattern("yyyy-MM-dd");

    // 私有构造：阻止 new DateUtils()，也阻止被子类化
    private DateUtils() {
        throw new UnsupportedOperationException("工具类禁止实例化");
    }

    public static String formatIso(LocalDate date) {
        return date.format(ISO_DATE);
    }
}
```

要点：`final` 挡继承、`private` 构造挡实例化、构造体抛异常挡反射 `setAccessible` 强行 new。

## 反例

```java
// ❌ 普通 class + 默认 public 构造：可被 new、可被继承
public class StringHelper {
    public int count = 0;            // ❌ 可变实例状态，多线程下踩踏
    public String trim(String s) {    // ❌ 非 static，逼调用方先 new
        count++;
        return s == null ? "" : s.trim();
    }
}
```

- 有可变字段 `count` → 工具类本应无状态，这里成了线程不安全的隐患。
- 实例方法 → 调用方被迫 `new StringHelper().trim(...)`，毫无必要。

## 自检

- [ ] 类是 `public final class`，不会被继承？
- [ ] 只有一个 `private` 构造器，且抛异常防反射实例化？
- [ ] 所有方法都是 `static` 且为纯函数？
- [ ] 没有任何可变实例 / 静态字段（常量用 `static final` 且不可变）？
- [ ] 命名以 `Utils` / `Helper` 结尾？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`prefer-common-libs.md`](./prefer-common-libs.md)（写之前先确认轮子是否已存在）
- 兄弟：[`bean-copy.md`](./bean-copy.md)（拷贝逻辑别自己写工具类）
