---
name: solid-single-responsibility
description: 单一职责原则 SRP — 一个类只应有一个引起它变化的理由，混杂职责的类要按变化轴拆分。Use when 类越改越臃肿 / 一个类同时管数据与持久化与通知 / 重构上帝类时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 单一职责
  - SRP
  - 职责拆分
  - 上帝类
  - Single Responsibility
effort: medium
context: inline
version: '1.0'
---
# SOLID · 单一职责 SRP

> 本条只管「一个类该不该拆」。加功能不改老代码见 [`open-closed.md`](./open-closed.md)。

## 规则

| 判据 | 含义 |
|------|------|
| 一个变化理由 | 类只因**一种**业务变化而修改；出现第二个修改理由就该拆 |
| 按变化轴拆分 | 数据结构、持久化、格式化、通知是不同变化轴，分到不同类 |
| 高内聚 | 类内方法都围绕同一职责，没有「顺带也做」的方法 |
| 命名可验证 | 类名能用一句话说清职责；要用「和/与/Manager」才说得清就是混了 |

## 正例：职责分离

```java
// 数据只负责承载状态
public class Employee {
    private String name;
    private BigDecimal salary;
    // getter/setter
}

// 持久化职责独立
@Repository
public class EmployeeRepository {
    public void save(Employee e) { /* 落库 */ }
}

// 计税职责独立（计税规则变，不影响存储）
public class TaxCalculator {
    public BigDecimal calc(Employee e) { /* 计税 */ }
}
```

## 反例：上帝类

```java
// ❌ 一个类塞了三种变化轴：数据 + 落库 + 计税 + 导出
public class Employee {
    private String name;
    public void save() { /* JDBC 写库 */ }       // 存储变 → 改这里
    public BigDecimal calcTax() { /* 计税 */ }     // 税法变 → 改这里
    public String toCsv() { /* 导出 */ }           // 格式变 → 改这里
}
// 任意一个变化都要改 Employee，且互相牵连风险
```

## 自检

- [ ] 这个类只有**一个**会引起它修改的理由？
- [ ] 类名能用一句话（无「和/Manager」）说清职责？
- [ ] 数据、持久化、格式化、通知没有混在同一个类？
- [ ] 拆出的类各自高内聚，对外只暴露本职责方法？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`open-closed.md`](./open-closed.md)（拆好后如何扩展不改旧码）
- 兄弟：[`interface-segregation.md`](./interface-segregation.md)（接口层面的职责拆分）
