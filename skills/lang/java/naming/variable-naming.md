---
name: java-variable-naming
description: Java 变量/字段命名 — camelCase、语义明确、集合用复数，单字母仅限循环计数器。Use when 写 Java 局部变量或字段 / 命名集合 / 评审变量名的 PR 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 变量命名
  - 字段命名
  - variable naming
  - camelCase
  - 集合复数
  - 单字母变量
effort: medium
context: inline
version: '1.0'
---
# Java · 变量/字段命名

> 本条只管「变量与字段怎么起名」。常量（`static final`）见 [`constant-naming.md`](./constant-naming.md)；方法见 [`method-naming.md`](./method-naming.md)。

## 规则

| 场景 | 约定 | 示例 |
|------|------|------|
| 局部变量 / 字段 | camelCase，名词，**语义明确** | `userName` / `orderCount` |
| 集合（List/Set/数组） | **复数** | `users` / `orderItems` / `ids` |
| Map | `keyToValue` 或 `xxxMap` | `idToUser` / `userMap` |
| boolean 字段 | `is` / `has` / `can` 前缀 | `isActive` / `hasError` |
| 循环计数器 | 单字母 `i` / `j` / `k` 可接受 | `for (int i = 0; ...)` |
| 临时 lambda 参数 | 短名可接受，但优于单字母 | `users.forEach(user -> ...)` |

## 正例

```java
List<User> activeUsers = repository.findActive();   // 集合用复数
Map<Long, User> idToUser = toMap(activeUsers);       // Map 表达键值关系
int retryCount = 0;                                  // 名词 + 语义
boolean hasPermission = checkAccess(user);           // boolean 带 has

for (int i = 0; i < size; i++) { ... }               // 循环计数器允许单字母
```

## 反例

```java
// ❌ 单字母 / 无意义，看不出装的是什么
List<User> l = repository.findActive();      // 应为 activeUsers
int n = 0;                                   // 应为 retryCount 等

// ❌ 集合用单数，误导成单个对象
List<User> user = repository.findActive();   // 应为 users

// ❌ 缩写
String usrNm;                                // 应为 userName

// ❌ 用类型/编号占位，无业务含义
String str1, str2;                           // 应表达各自含义
```

## 自检

- [ ] 变量名是语义明确的名词，能看出它装的是什么？
- [ ] 集合/数组用复数，单个对象用单数？
- [ ] 除循环计数器外，没有单字母变量？
- [ ] 没有缩写、没有 `str1` / `temp` / `data` 这类无含义占位名？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`constant-naming.md`](./constant-naming.md)（常量名）
- 兄弟：[`method-naming.md`](./method-naming.md)（方法名）
- 兄弟：[`class-naming.md`](./class-naming.md)（类名）
