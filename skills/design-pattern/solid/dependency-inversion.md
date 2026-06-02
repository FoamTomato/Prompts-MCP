---
name: solid-dependency-inversion
description: 依赖倒置原则 DIP — 高层模块与低层实现都依赖抽象，配合 Spring 构造器注入接口而非 new 具体类。Use when 高层直接 new 低层实现 / 依赖难替换或难测 / 设计 Service 依赖注入时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 依赖倒置
  - DIP
  - 依赖注入
  - 面向接口编程
  - Dependency Inversion
  - Spring DI
effort: medium
context: inline
version: '1.0'
---
# SOLID · 依赖倒置 DIP

> 本条只管「依赖朝抽象还是朝实现」。开闭/多态扩展见 [`open-closed.md`](./open-closed.md)。

## 规则

| 判据 | 要求 |
|------|------|
| 都依赖抽象 | 高层模块和低层实现都依赖接口，而非高层依赖低层具体类 |
| 抽象不依赖细节 | 接口定义在高层语义上，由低层去实现 |
| 注入而非 new | 依赖由 Spring 构造器注入，类内不 `new` 具体实现 |
| 可替换可测 | 换实现/给测试塞 mock 都不改高层代码 |

## 正例：依赖接口 + 构造器注入

```java
// 高层定义抽象（它需要什么能力）
public interface NotifyChannel { void send(String to, String msg); }

@Component
public class SmsChannel implements NotifyChannel { /* ... */ }

// 高层只依赖接口；具体实现由 Spring 注入（推荐构造器注入，便于 final + 单测）
@Service
public class OrderService {
    private final NotifyChannel notifyChannel;
    public OrderService(NotifyChannel notifyChannel) {
        this.notifyChannel = notifyChannel;
    }
    public void confirm(Order o) {
        notifyChannel.send(o.getPhone(), "下单成功");  // 不关心是短信还是邮件
    }
}
```

换 `EmailChannel` 或单测注入 `mock(NotifyChannel.class)` 都不改 OrderService。

## 反例：高层 new 低层

```java
// ❌ Service 直接 new 具体实现，焊死依赖，无法替换/mock
@Service
public class OrderService {
    private final SmsChannel channel = new SmsChannel();   // 改成邮件要改这里
    // 单测被迫真发短信
}
```

## 自检

- [ ] 高层依赖的是接口，不是具体实现类？
- [ ] 依赖通过构造器注入（`final` 字段），类内没有 `new` 具体依赖？
- [ ] 换实现 / 注入 mock 不需要改高层代码？
- [ ] 抽象按高层的语义需求定义，而不是照搬某个低层实现的方法？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`open-closed.md`](./open-closed.md)（依赖抽象才能扩展不改码）
- 兄弟：[`interface-segregation.md`](./interface-segregation.md)（注入的接口要小而专）
