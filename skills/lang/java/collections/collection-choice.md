---
name: java-collection-choice
description: List/Set/Map 实现选型 — ArrayList vs LinkedList、HashMap/TreeMap/LinkedHashMap、HashSet/TreeSet，及初始容量预估。Use when 声明集合变量 / 纠结用哪个实现类 / 大集合担心 resize 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 集合选型
  - ArrayList LinkedList
  - HashMap TreeMap LinkedHashMap
  - HashSet TreeSet
  - 初始容量
  - initial capacity
  - collection implementation
effort: medium
context: inline
version: '1.0'
---
# Java · 集合实现选型

> 本条只管「选哪个实现类 + 初始容量」。Stream 用法见 [`stream-api.md`](./stream-api.md)；只读暴露见 [`immutable-collections.md`](./immutable-collections.md)；并发共享见 [`concurrent-collections.md`](./concurrent-collections.md)。

## 规则

| 需求 | 选 |
|------|-----|
| 随机访问、尾部增删（绝大多数场景默认） | `ArrayList` |
| 频繁头部 / 中间增删，或当队列/双端队列用 | `LinkedList`（更多时候用 `ArrayDeque`）|
| 普通键值，不要求顺序 | `HashMap` |
| 要按 key 排序遍历 / 范围查询 | `TreeMap` |
| 要保持插入顺序（或 LRU 访问顺序） | `LinkedHashMap` |
| 去重，不要求顺序 | `HashSet` |
| 去重且要排序 | `TreeSet` |

初始容量：已知元素数 `n` 时，按 `n / 0.75 + 1` 设容量，避免多次 resize 扩容。

## 正例

```java
// ✅ 默认就用 ArrayList，可随机访问
List<Order> orders = new ArrayList<>();

// ✅ 已知约 1000 个元素，预设容量避免反复扩容
Map<Long, User> cache = new HashMap<>((int) (1000 / 0.75f) + 1);

// ✅ 要按 key 升序输出报表
Map<LocalDate, BigDecimal> daily = new TreeMap<>();

// ✅ 队列 / 栈语义优先 ArrayDeque，而非 LinkedList
Deque<Task> queue = new ArrayDeque<>();
```

## 反例

```java
// ❌ 默认随手 LinkedList —— 随机访问 O(n)，内存开销也比 ArrayList 大
List<Order> orders = new LinkedList<>();

// ❌ HashMap(16) 装 10000 条 —— 反复 resize，rehash 拖慢
Map<Long, User> cache = new HashMap<>();
```

理由：`LinkedList` 的随机 `get(i)` 是 O(n)，绝大多数“增删快”的直觉场景其实 `ArrayList` 尾部操作更优；`ArrayDeque` 比 `LinkedList` 更适合做栈和队列。

## 自检

- [ ] List 默认 `ArrayList`，只有明确头部/中间高频增删才考虑 `LinkedList`？
- [ ] 需要排序遍历用 `TreeMap`/`TreeSet`，需要插入顺序用 `LinkedHashMap`？
- [ ] 队列 / 栈用了 `ArrayDeque` 而非 `LinkedList`？
- [ ] 已知大小的集合按 `n / 0.75 + 1` 预设了初始容量？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`stream-api.md`](./stream-api.md)（选好集合后怎么遍历处理）
- 兄弟：[`immutable-collections.md`](./immutable-collections.md)（要暴露只读集合时）
- 兄弟：[`concurrent-collections.md`](./concurrent-collections.md)（要在并发下共享时）
