---
name: java-equals-hashcode
description: equals 与 hashCode 必须成对重写、用 Objects.hash 实现、与 compareTo 一致、优先 IDE/Lombok 生成。Use when 重写 equals / 把对象放进 HashSet 或 HashMap key 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - equals
  - hashCode
  - Objects.hash
  - compareTo
  - HashSet
  - 哈希一致性
effort: medium
context: inline
version: '1.0'
---
# Java · equals / hashCode

> 本条只管「equals/hashCode 怎么写」。Lombok 生成它们的坑见 [`lombok-usage.md`](./lombok-usage.md)；字段比 null 安全见 [`null-safety.md`](./null-safety.md)。

## 规则

| 约束 | 说明 |
|------|------|
| 成对重写 | 重写 `equals` 必须**同时**重写 `hashCode`（反之亦然） |
| 一致性 | `a.equals(b)` 为 true ⇒ `a.hashCode() == b.hashCode()` |
| 与 compareTo 一致 | 实现 `Comparable` 时，`compareTo == 0` 应与 `equals` 结果一致 |
| 实现方式 | 字段比较用 `Objects.equals`，hashCode 用 `Objects.hash`；或直接 IDE / Lombok 生成 |
| 选哪些字段 | 用**业务主键 / 标识字段**，不要把全部字段都塞进去 |

## 正例

```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    User user = (User) o;
    return Objects.equals(id, user.id);   // 用标识字段
}

@Override
public int hashCode() {
    return Objects.hash(id);   // 与 equals 选用同一组字段
}
```

## 反例

```java
// ❌ 只重写 equals 不重写 hashCode → 放进 HashSet 去重失效、HashMap 取不到
@Override
public boolean equals(Object o) { ... }
// hashCode 没重写，仍是对象地址

// ❌ 两个方法选用的字段不一致 → 违反一致性契约
public boolean equals(Object o) { return Objects.equals(id, ((User)o).id); }
public int hashCode() { return Objects.hash(name); }   // 用了 name，对不上
```

## 自检

- [ ] equals 与 hashCode **同时**重写，没有只改其一？
- [ ] 两者选用**同一组字段**，满足一致性契约？
- [ ] 实现 Comparable 时 `compareTo == 0` 与 `equals` 一致？
- [ ] 字段比较用 `Objects.equals`、hashCode 用 `Objects.hash`（或 IDE / Lombok 生成）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`lombok-usage.md`](./lombok-usage.md)（@EqualsAndHashCode 的字段选择与继承坑）
- 兄弟：[`null-safety.md`](./null-safety.md)（equals 内部用 Objects.equals 比可空字段）
