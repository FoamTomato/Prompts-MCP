---
name: java-type-erasure-pitfalls
description: 类型擦除导致的运行期坑 — 不能 new T[]、不能 instanceof 泛型、按泛型重载冲突，靠 Class<T> / TypeReference 把类型传到运行期。Use when 写 Java 泛型容器 / 反序列化泛型 / 排查 erasure 相关编译错误时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 类型擦除
  - type erasure
  - new T[]
  - instanceof 泛型
  - Class<T>
  - TypeReference
  - 泛型重载冲突
  - reified
effort: medium
context: inline
version: '1.0'
---
# Java · 类型擦除的坑

> 本条只管「擦除导致运行期拿不到类型时怎么办」。通配符边界怎么选见 [`wildcard-pecs.md`](./wildcard-pecs.md)。

## 规则

Java 泛型只存在于**编译期**，运行期 `T` 被擦除成 `Object`（或上界）。凡是运行期需要真实类型的操作都失效，必须显式把 `Class<T>` / `TypeReference` 传进来。

| 想做的事 | 为什么不行 | 改成 |
|---------|-----------|------|
| `new T[n]` | 运行期不知 T，无法分配数组 | 传 `Class<T>` + `Array.newInstance` 或返回 `List<T>` |
| `obj instanceof List<String>` | 擦除后只剩 `List`，无法判元素类型 | 判 `instanceof List<?>`，元素逐个 check |
| `void f(List<String>)` + `void f(List<Integer>)` | 擦除后签名相同 → 重载冲突 | 改方法名 / 加非泛型参数区分 |
| 反序列化成 `List<User>` | 擦除后框架不知道元素是 User | 传 `TypeReference` / `Class<User>` |

## 正例

```java
// ✅ 需要建泛型数组 → 把 Class<T> 传进来
public static <T> T[] newArray(Class<T> type, int len) {
    @SuppressWarnings("unchecked")
    T[] arr = (T[]) java.lang.reflect.Array.newInstance(type, len);
    return arr;
}

// ✅ Jackson 反序列化泛型集合：用 TypeReference 保住元素类型
List<User> users = mapper.readValue(json, new TypeReference<List<User>>() {});

// ✅ 反序列化单个对象：传 Class<T>
public <T> T parse(String json, Class<T> clazz) {
    return mapper.readValue(json, clazz);
}
```

## 反例

```java
// ❌ 编译不过：运行期没有 T，无法 new T[]
public <T> T[] toArray(List<T> list) {
    T[] arr = new T[list.size()];   // error: generic array creation
    return arr;
}

// ❌ 编译不过：泛型参数无法 instanceof
if (obj instanceof List<String>) { ... }   // error: illegal generic type

// ❌ 编译不过：擦除后两个签名都是 print(List)
void print(List<String> s) {}
void print(List<Integer> i) {}              // name clash, same erasure

// ❌ 丢类型：用 Object.class 反序列化，拿回来还是 LinkedHashMap
List<User> users = mapper.readValue(json, List.class);  // 元素其实是 Map，不是 User
```

理由：擦除后 `List<String>` 与 `List<Integer>` 在字节码里都是 `List`，所以既无法 `instanceof` 也无法重载区分；数组要求运行期具体类型，而 `T` 已不存在。把类型「物化」为 `Class<T>` / `TypeReference` 参数，是 Java 没有 reified 泛型时的标准绕法。

## 自检

- [ ] 没有 `new T[]` / `new List<String>[]` 这类泛型数组创建？
- [ ] 没有对带类型参数的泛型做 `instanceof`（只对 `List<?>` / 原始类型判）？
- [ ] 没有仅靠泛型参数区分的重载（擦除后签名会撞）？
- [ ] 反序列化泛型集合用了 `TypeReference`，单对象用了 `Class<T>`，而非 `List.class` / `Object.class`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`wildcard-pecs.md`](./wildcard-pecs.md)（编译期的通配符边界选型）
