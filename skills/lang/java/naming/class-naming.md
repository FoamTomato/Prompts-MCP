---
name: java-class-naming
description: Java 类 PascalCase + 后缀 Service/Repository/Controller。Use when 写 Java
  代码 / 评审涉及 `class-naming` 的 PR。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - class
  - PascalCase
  - 后缀
effort: medium
context: inline
version: '1.0'
---
# Java · 类命名

## 规则

| 规则 | 示例 |
|------|------|
| PascalCase | `UserService` / `OrderRepository` |
| 类型后缀 | `*Service` / `*Repository` / `*Controller` / `*Dto` / `*Vo` |
| 接口可加 `I` 前缀（看团队风格） | `IUserRepository`（不推荐）/ `UserRepository`（推荐） |
| 抽象类 `Abstract*` | `AbstractBaseService` |
| 异常 `*Exception` | `OrderNotFoundException` |
| 枚举 `*Type` / `*Status` | `OrderStatus` / `UserType` |

## Spring 注解层级与类名对齐

```java
@RestController            UserController
@Service                   UserService
@Repository                UserRepository  (Spring Data)
@Configuration             AppConfig
@Component                 EmailNotifier
```

## 反例

```java
// ❌ 缩写
public class UsrSvc { }

// ❌ 缺后缀
public class User { }   // 应是 UserService / UserController 等
```

## 自检

- [ ] PascalCase？
- [ ] 后缀对齐层级（Service/Repository/Controller）？
- [ ] 无缩写？
- [ ] 异常类以 `Exception` 结尾？

## 相关

- 父：[`./index.md`](./index.md)

