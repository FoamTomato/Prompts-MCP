---
name: singleton-thread-safe
description: 线程安全单例的三种 Java 实现与取舍 — 枚举（首选）/ 静态内部类（懒加载）/ 双重检查锁（volatile 不可省）。Use when 写全局唯一实例 / 选单例实现 / 评审双重检查锁是否漏 volatile 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 单例
  - 线程安全单例
  - 双重检查锁
  - 静态内部类
  - 枚举单例
  - volatile
  - DCL
effort: medium
context: inline
version: '1.0'
---
# Singleton · 线程安全单例

> Spring 管理的 Bean 默认就是容器级单例，业务里优先交给 Spring；本条针对**不走容器**的纯 Java 单例。

## 规则

| 实现 | 线程安全 | 懒加载 | 防反射/序列化破坏 | 选用 |
|------|---------|-------|------------------|------|
| 枚举 | ✅（JVM 保证） | ❌ 类加载即建 | ✅ 天然防御 | **首选** |
| 静态内部类 | ✅（类加载机制） | ✅ 用到才加载 | ❌ | 需懒加载时 |
| 双重检查锁 DCL | ✅（须 `volatile`） | ✅ | ❌ | 一般不必，懂原理即可 |
| 饿汉式 | ✅ | ❌ | ❌ | 创建廉价且必用时 |

## 正例：枚举（首选）

```java
public enum Config {
    INSTANCE;
    private final Properties props = load();
    public String get(String key) { return props.getProperty(key); }
}
// 用：Config.INSTANCE.get("k")。天然防反射、防序列化生成第二个实例
```

## 正例：静态内部类（懒加载）

```java
public class Resource {
    private Resource() {}
    private static class Holder {            // 外类加载时不初始化
        static final Resource INSTANCE = new Resource();
    }
    public static Resource getInstance() {   // 首次调用才触发 Holder 加载
        return Holder.INSTANCE;
    }
}
```

## 双重检查锁：volatile 不可省

```java
public class Conn {
    private static volatile Conn instance;   // ❗ volatile 防指令重排
    private Conn() {}
    public static Conn getInstance() {
        if (instance == null) {              // 第一次检查（免锁）
            synchronized (Conn.class) {
                if (instance == null) {      // 第二次检查（持锁）
                    instance = new Conn();
                }
            }
        }
        return instance;
    }
}
```

漏 `volatile`：`new` 非原子（分配/构造/赋引用三步可重排），别的线程可能读到「已赋引用但未构造完」的半成品对象。

## 自检

- [ ] 无特殊需求优先枚举；要懒加载用静态内部类？
- [ ] 用了双重检查锁，字段是否 `volatile`？两次 null 检查都在？
- [ ] 构造器私有，没有别的入口能再造实例？
- [ ] 在 Spring 项目里，该交给容器单例的没有自己手写？

## 相关

- 父：[`./index.md`](./index.md)
- 相关原理：[`../../lang/java/concurrency/index.md`](../../lang/java/concurrency/index.md)（volatile / 可见性）
