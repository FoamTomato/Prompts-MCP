---
name: proxy-jdk-vs-cglib
description: JDK 动态代理 vs CGLIB 取舍 — JDK 基于接口、CGLIB 基于子类，Spring AOP 有接口走 JDK 否则 CGLIB。Use when 写动态代理 / 排查 AOP 自调用或 final 方法不生效 / 强制代理方式时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 动态代理
  - JDK 代理
  - CGLIB
  - Spring AOP
  - 代理失效
  - InvocationHandler
effort: medium
context: inline
version: '1.0'
---
# Proxy · JDK 动态代理 vs CGLIB

## 规则

| 维度 | JDK 动态代理 | CGLIB |
|------|-------------|-------|
| 基于 | **接口**（`java.lang.reflect.Proxy`） | **子类**（运行时生成子类字节码） |
| 前提 | 目标类必须实现接口 | 目标类不能是 `final`、方法不能 `final`/`private` |
| Spring AOP 默认 | 有接口时用它 | 无接口时自动切换；`proxyTargetClass=true` 强制用它 |
| 性能 | 调用走反射 | 直接调用子类方法，略快 |

## JDK 动态代理示例

```java
public interface UserService { void save(); }

UserService proxy = (UserService) Proxy.newProxyInstance(
    UserService.class.getClassLoader(),
    new Class[]{ UserService.class },
    (obj, method, args) -> {
        System.out.println("before " + method.getName());
        return method.invoke(target, args);   // 调真实对象
    });
```

## Spring AOP 怎么选

- 目标类**实现了接口** → 默认 JDK 代理（注入时按接口类型）。
- 目标类**没有接口** → Spring 自动用 CGLIB。
- Spring Boot 默认 `spring.aop.proxy-target-class=true`，即全量 CGLIB（避免「按接口注入还是按类注入」的踩坑）。

## 代理失效的两个常见坑

```java
// ❌ 同类内自调用：this.bar() 不走代理，@Transactional/@Cacheable 失效
@Service
public class OrderService {
    public void foo() { this.bar(); }       // 走的是原始对象，不是代理
    @Transactional public void bar() { }
}
// ✅ 自注入自己 或 抽到另一个 Bean 调用，让调用经过代理

// ❌ CGLIB 无法代理 final 方法 / final 类 → 增强直接不生效（无报错）
```

## 自检

- [ ] 清楚目标类有无接口，从而知道走的是 JDK 还是 CGLIB？
- [ ] AOP 注解（@Transactional/@Async/@Cacheable）所在方法是 public 且**非同类自调用**？
- [ ] 用 CGLIB 时，被增强的方法/类没有 `final`？
- [ ] 需要强制 CGLIB 时设了 `proxyTargetClass=true`？

## 相关

- 父：[`./index.md`](./index.md)
- 框架相关：[`../../framework/spring-boot/transaction.md`](../../framework/spring-boot/transaction.md)（事务代理与自调用失效）
