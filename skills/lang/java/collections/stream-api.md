---
name: java-stream-api
description: Stream 正确用法 — collect/map/filter 主线、peek 不做副作用、parallelStream 慎用、toMap 处理重复 key。Use when 写 Stream 链 / 把循环改成 Stream / toMap 抛异常时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - Stream 流
  - collect map filter
  - peek 副作用
  - parallelStream 并行流
  - Collectors.toMap
  - duplicate key
  - 重复 key
effort: medium
context: inline
version: '1.0'
---
# Java · Stream API 用法

> 本条只管「Stream 链怎么写对」。选哪个集合实现见 [`collection-choice.md`](./collection-choice.md)；只读结果集见 [`immutable-collections.md`](./immutable-collections.md)。

## 规则

| 要点 | 规则 |
|------|------|
| 转换 / 过滤 / 收集 | 用 `map` / `filter` / `collect`，中间操作要无副作用 |
| `peek` | 只用于调试观察，**禁在 peek 里改状态 / 写库** |
| `parallelStream` | 默认串行；只在大数据量 + 无共享可变状态 + 无顺序依赖时才用 |
| `Collectors.toMap` | **必须**预判重复 key：传第三个 merge 参数，否则重复 key 抛 `IllegalStateException` |

## 正例

```java
// ✅ 主线用 map/filter/collect，纯函数无副作用
List<String> names = users.stream()
        .filter(u -> u.isActive())
        .map(User::getName)
        .collect(Collectors.toList());

// ✅ toMap 带 merge 函数，重复 key 时保留后者
Map<Long, User> byId = users.stream()
        .collect(Collectors.toMap(User::getId, u -> u, (a, b) -> b));
```

## 反例

```java
// ❌ peek 里做副作用：终端操作缺省时整链不执行，行为不可预测
users.stream().peek(u -> save(u)).collect(Collectors.toList());

// ❌ toMap 不给 merge 函数：出现重复 id 直接抛 IllegalStateException
Map<Long, User> byId = users.stream()
        .collect(Collectors.toMap(User::getId, u -> u));

// ❌ 小集合上 parallelStream，且累加到共享 list —— 线程不安全且更慢
List<String> out = new ArrayList<>();
users.parallelStream().forEach(u -> out.add(u.getName()));
```

理由：Stream 中间操作是惰性的，副作用塞进 `peek`/`map` 会因终端操作缺失而不执行；`parallelStream` 共享公共 `ForkJoinPool`，小数据量调度开销反而更高，写共享可变状态还会数据竞争。

## 自检

- [ ] 中间操作（map/filter）是纯函数，没有写库 / 改外部变量？
- [ ] 没有用 `peek` 做副作用，只用于调试？
- [ ] `Collectors.toMap` 都带了第三个 merge 参数处理重复 key？
- [ ] 用 `parallelStream` 前确认数据量大、无共享可变状态、无顺序依赖？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`collection-choice.md`](./collection-choice.md)（collect 到哪种集合）
- 兄弟：[`immutable-collections.md`](./immutable-collections.md)（返回只读结果集）
- 兄弟：[`concurrent-collections.md`](./concurrent-collections.md)（并行流下的共享容器）
