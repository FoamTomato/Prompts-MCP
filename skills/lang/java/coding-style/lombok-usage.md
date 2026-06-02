---
name: java-lombok-usage
description: Lombok 注解约定 — @Data 慎用（暴露 setter）、优先 @Getter/@Builder/@RequiredArgsConstructor、@EqualsAndHashCode 继承坑。Use when 给类加 Lombok 注解 / 写实体或 DTO 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - Lombok
  - Lombok 注解
  - '@Data'
  - '@Builder'
  - '@Getter'
  - 实体类注解
  - RequiredArgsConstructor
  - EqualsAndHashCode
effort: medium
context: inline
version: '1.0'
---
# Java · Lombok 约定

> 本条管 Lombok 注解选型。equals/hashCode 的语义契约本身见 [`equals-hashcode.md`](./equals-hashcode.md)。

## 规则

| 注解 | 用法约定 |
|------|---------|
| `@Data` | **慎用**：它打包了 setter + equals + hashCode + toString，会给本应不可变的对象暴露全字段 setter |
| `@Getter` | 默认首选，只读暴露 |
| `@Builder` | 多字段对象构造，替代长参数构造函数 |
| `@RequiredArgsConstructor` | 配 `final` 字段做构造器注入（Spring Bean 首选） |
| `@Value` | 需要不可变对象时用它（全 final + 仅 getter） |
| `@EqualsAndHashCode` | 显式 `of = {...}` 指定标识字段；有继承时配 `callSuper` |

## 正例

```java
// Spring 服务：final 字段 + 构造器注入
@Service
@RequiredArgsConstructor
public class OrderService {
    private final OrderRepository repo;   // 自动生成构造器注入
}

// 实体：只读 getter + 显式选 equals 字段
@Getter
@Builder
@EqualsAndHashCode(of = "id")            // 只用 id，不是全字段
public class Order {
    private final Long id;
    private String status;
}
```

## 反例

```java
// ❌ 实体上 @Data：自动 setter 让本该受控的字段被随处改
@Data
public class Order {
    private Long id;
    private String status;   // 任何地方都能 order.setStatus(...)
}

// ❌ @EqualsAndHashCode 默认拿全部字段：可变字段一改，HashSet 里就丢
@Data   // 等同 @EqualsAndHashCode 全字段
public class Order { private Long id; private String status; }

// ❌ 子类继承却没 callSuper，父类字段被忽略
@EqualsAndHashCode   // 缺 callSuper = true
public class VipOrder extends Order { ... }
```

## 自检

- [ ] 实体 / DTO 避免无脑 `@Data`，按需用 `@Getter` / `@Builder`？
- [ ] Spring Bean 用 `@RequiredArgsConstructor` + `final` 字段注入？
- [ ] `@EqualsAndHashCode` 用 `of` 显式指定标识字段，不是全字段？
- [ ] 有继承的类配了 `@EqualsAndHashCode(callSuper = true)`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`equals-hashcode.md`](./equals-hashcode.md)（生成 equals/hashCode 的语义契约）
- 兄弟：[`null-safety.md`](./null-safety.md)（@NonNull 配合 Lombok 生成判空）
