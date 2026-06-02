---
name: solid-interface-segregation
description: 接口隔离原则 ISP — 接口要小而专，客户端不应被迫依赖它用不到的方法，胖接口按角色拆成多个小接口。Use when 实现类被迫空实现方法 / 设计接口粒度 / 评审一个接口塞太多方法时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 接口隔离
  - ISP
  - 胖接口拆分
  - 角色接口
  - Interface Segregation
effort: medium
context: inline
version: '1.0'
---
# SOLID · 接口隔离 ISP

> 本条只管「接口该多大」。类层面的职责拆分见 [`single-responsibility.md`](./single-responsibility.md)。

## 规则

| 判据 | 要求 |
|------|------|
| 小而专 | 一个接口只描述**一种角色/能力**，方法围绕同一用途 |
| 不强加依赖 | 客户端只看到自己用得到的方法 |
| 按角色拆 | 一个类可实现多个小接口，组合出完整能力 |
| 信号 | 实现类里出现空方法 / `throw new UnsupportedOperationException()` → 接口太胖 |

## 正例：按角色拆小接口

```java
public interface Readable { String read(); }
public interface Writable { void write(String data); }

// 只读设备只实现需要的接口
public class SensorDevice implements Readable {
    public String read() { return "..."; }
}

// 读写设备组合两个小接口
public class FileDevice implements Readable, Writable {
    public String read() { return "..."; }
    public void write(String data) { /* ... */ }
}
```

## 反例：胖接口逼迫空实现

```java
// ❌ 一个大接口塞所有能力
public interface Device {
    String read();
    void write(String data);
    void print();
    void scan();
}

// 只读传感器被迫实现一堆用不到的方法
public class SensorDevice implements Device {
    public String read() { return "..."; }
    public void write(String d) { throw new UnsupportedOperationException(); } // 坏味道
    public void print() { /* 空实现 */ }
    public void scan()  { /* 空实现 */ }
}
```

## 自检

- [ ] 每个接口只描述一种角色/能力，方法围绕同一用途？
- [ ] 没有实现类被迫写空方法或抛 UnsupportedOperationException？
- [ ] 需要多能力的类靠**实现多个小接口**组合，而非依赖一个胖接口？
- [ ] 客户端只看到它真正调用的方法？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`single-responsibility.md`](./single-responsibility.md)（类层面的同类拆分）
- 兄弟：[`liskov-substitution.md`](./liskov-substitution.md)（空实现也破坏替换）
