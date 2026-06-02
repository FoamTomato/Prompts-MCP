---
name: java-wildcard-pecs
description: 泛型通配符 PECS 原则 — 只读集合用 ? extends（生产者），只写集合用 ? super（消费者），自身既读又写用泛型方法 <T>。Use when 写 Java 泛型方法签名 / 给 List 参数选通配符 / 评审泛型 API 灵活性时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - PECS
  - 通配符
  - wildcard
  - ? extends
  - ? super
  - 泛型方法
  - generic method
  - 协变 逆变
effort: medium
context: inline
version: '1.0'
---
# Java · 泛型通配符 PECS

> 本条只管「通配符边界怎么选」。擦除导致的 `new T[]` / `instanceof` 坑见 [`type-erasure-pitfalls.md`](./type-erasure-pitfalls.md)。

## 规则

**PECS = Producer Extends, Consumer Super**。判据：这个参数对调用方法体来说是「数据来源」还是「数据去处」？

| 参数角色 | 你对它做什么 | 用 |
|---------|-------------|-----|
| 生产者（producer） | 只从中**读**元素 | `? extends T` |
| 消费者（consumer） | 只往里**写**元素 | `? super T` |
| 既读又写 / 类型要联动 | 同一个 `T` 进出 | 泛型方法 `<T>`，不用通配符 |
| 完全不关心元素类型 | 只 `size()` / `clear()` | 无界 `<?>` |

口诀：`? extends` 能读不能写（写不进去，编译器不知具体子类）；`? super` 能写不能精确读（读出来只能当 `Object`）。

## 正例

```java
// src 是生产者：只读 → extends；dst 是消费者：只写 → super
public static <T> void copy(List<? extends T> src, List<? super T> dst) {
    for (T t : src) {     // 从 src 读 T，OK
        dst.add(t);       // 往 dst 写 T，OK
    }
}

// 调用方因此能跨子类型组合
List<Integer> ints = List.of(1, 2, 3);
List<Number> nums = new ArrayList<>();
copy(ints, nums);         // Integer extends Number，成立
```

```java
// 入参类型与返回类型联动 → 用泛型方法，别用通配符
public static <T extends Comparable<? super T>> T max(List<? extends T> list) {
    T best = list.get(0);
    for (T t : list) if (t.compareTo(best) > 0) best = t;
    return best;          // 返回精确 T，通配符做不到
}
```

## 反例

```java
// ❌ 想往 ? extends 集合里写 —— 编译不过
List<? extends Number> nums = new ArrayList<Integer>();
nums.add(1);              // 编译错：无法确认元素恰好是 Integer

// ❌ 入参/返回都是同一 T 却用裸 Object 退化，丢类型信息
public static Object first(List<?> list) { return list.get(0); }
// 调用方拿到 Object 还要强转 —— 应写成 <T> T first(List<T> list)
```

理由：`? extends T` 是上界、只保证「至少是 T」，所以可读出 T、不可写入；`? super T` 是下界、只保证「至多到 T」，所以可写入 T、读出只能当 `Object`。返回值需要精确类型时通配符无能为力，必须升级成泛型方法。

## 自检

- [ ] 只读的集合参数用了 `? extends`（生产者）？
- [ ] 只写的集合参数用了 `? super`（消费者）？
- [ ] 入参与返回类型联动的场景用泛型方法 `<T>` 而非通配符？
- [ ] 没有试图往 `? extends` 集合 `add`、也没把 `? super` 读出的值当具体类型用？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`type-erasure-pitfalls.md`](./type-erasure-pitfalls.md)（擦除导致的运行期类型坑）
