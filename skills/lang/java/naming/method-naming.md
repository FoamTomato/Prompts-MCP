---
name: java-method-naming
description: Java 方法命名 — 动词开头表动作，boolean 用 is/has/can 前缀，禁缩写。Use when 写 Java 方法 / 命名 getter setter / 评审方法名的 PR 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 方法命名
  - method naming
  - 动词开头
  - boolean 方法
  - isXxx
  - getter setter
effort: medium
context: inline
version: '1.0'
---
# Java · 方法命名

> 本条只管「方法名怎么起」。类名见 [`class-naming.md`](./class-naming.md)；变量/字段见 [`variable-naming.md`](./variable-naming.md)。

## 规则

| 场景 | 约定 | 示例 |
|------|------|------|
| 一般方法 | camelCase，**动词/动词短语开头**表动作 | `sendEmail()` / `calculateTotal()` |
| 取值 | `get` + 名词 | `getUserName()` |
| 设值 | `set` + 名词 | `setUserName(String name)` |
| boolean 返回 | `is` / `has` / `can` / `should` 前缀 | `isActive()` / `hasPermission()` / `canRetry()` |
| 转换 | `to` + 目标类型 | `toDto()` / `toString()` |
| 工厂/构造 | `of` / `from` / `create` / `new` | `User.of(id)` / `LocalDate.from(temporal)` |

## 正例

```java
public boolean isExpired() { ... }       // boolean 用 is
public boolean hasChildren() { ... }      // 存在性用 has
public boolean canEdit(User u) { ... }    // 能力用 can
public BigDecimal calculateTax() { ... }  // 动词开头，明确动作
public UserDto toDto() { ... }            // 转换用 to
```

## 反例

```java
// ❌ 名词开头，看不出是动作还是属性
public BigDecimal tax() { }            // 应为 calculateTax()

// ❌ boolean 方法不带 is/has，调用处读起来像取对象
public boolean expired() { }           // 应为 isExpired()
public boolean active() { }            // 应为 isActive()

// ❌ 缩写，降低可读性
public void clacAmt() { }              // 应为 calculateAmount()
public User getUsrInfo() { }           // 应为 getUserInfo()
```

## 自检

- [ ] 普通方法以动词/动词短语开头，能看出它「做什么」？
- [ ] 返回 boolean 的方法用 `is` / `has` / `can` / `should` 前缀？
- [ ] getter/setter 遵循 `getXxx` / `setXxx`（boolean getter 用 `isXxx`）？
- [ ] 没有缩写（`calc` / `usr` / `info` 拼写成全词）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`class-naming.md`](./class-naming.md)（类名）
- 兄弟：[`variable-naming.md`](./variable-naming.md)（变量/字段名）
- 兄弟：[`constant-naming.md`](./constant-naming.md)（常量名）
