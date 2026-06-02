---
name: java-immutable-collections
description: 暴露只读集合 — List.of/Map.of、Collections.unmodifiableList、防御性拷贝，以及 Arrays.asList 的固定长度坑。Use when 返回内部集合给外部 / 定义常量集合 / 接收外部传入集合做字段时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 不可变集合
  - immutable collection
  - List.of Map.of
  - unmodifiableList
  - 防御性拷贝
  - defensive copy
  - Arrays.asList
effort: medium
context: inline
version: '1.0'
---
# Java · 不可变与只读集合

> 本条只管「怎么不让集合被外部改坏」。选哪个实现见 [`collection-choice.md`](./collection-choice.md)；并发安全见 [`concurrent-collections.md`](./concurrent-collections.md)。

## 规则

| 场景 | 用 |
|------|-----|
| 定义常量集合 / 真不可变集合 | `List.of(...)` / `Map.of(...)` / `Set.of(...)`（Java 9+） |
| 把可变集合包成只读视图返回 | `Collections.unmodifiableList(...)` |
| getter 返回内部集合 / 构造器接收外部集合存为字段 | **防御性拷贝**：`new ArrayList<>(src)` |

`unmodifiableList` 是**视图**：底层原集合改了视图跟着变，所以包之前通常要先拷贝。

## 正例

```java
// ✅ 常量集合用 List.of，本身不可变、不含 null
private static final List<String> ROLES = List.of("ADMIN", "USER");

// ✅ getter 防御性拷贝，外部拿到的改动不影响内部
public List<Order> getOrders() {
    return new ArrayList<>(this.orders);
}

// ✅ 构造器接收外部集合也要拷贝，切断外部引用
public Cart(List<Item> items) {
    this.items = new ArrayList<>(items);
}
```

## 反例

```java
// ❌ Arrays.asList 返回定长视图：add/remove 抛 UnsupportedOperationException，
//    且改数组会串改 list
List<Integer> nums = Arrays.asList(1, 2, 3);
nums.add(4);  // UnsupportedOperationException

// ❌ 直接返回内部集合：外部可随意 add/remove，破坏封装
public List<Order> getOrders() {
    return this.orders;
}
```

理由：`Arrays.asList` 既不是真不可变也不是普通 ArrayList，是个长度固定的桥接视图；直接返回内部集合等于把私有状态交给外部修改。`List.of` 返回的集合既不可变也禁止 `null` 元素。

## 自检

- [ ] 常量集合用 `List.of` / `Map.of` / `Set.of`，没用 `Arrays.asList` 凑数？
- [ ] getter 返回内部集合时做了防御性拷贝（或包 `unmodifiableXxx`）？
- [ ] 构造器/setter 接收外部集合时拷贝了，没直接存引用？
- [ ] 清楚 `unmodifiableList` 是视图、底层变它也变？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`collection-choice.md`](./collection-choice.md)（拷贝成哪种实现）
- 兄弟：[`concurrent-collections.md`](./concurrent-collections.md)（并发下的安全共享）
- 兄弟：[`stream-api.md`](./stream-api.md)（collect 出只读结果集）
