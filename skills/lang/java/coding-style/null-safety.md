---
name: java-null-safety
description: Java 防 NPE — 参数 Objects.requireNonNull 校验、返回空集合不返回 null、@Nullable 标注、比较用 Objects.equals。Use when 写公开方法入参 / 返回集合 / 排查 NPE 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 空指针
  - NullPointerException
  - Objects.requireNonNull
  - 返回空集合
  - Nullable
  - Objects.equals
effort: medium
context: inline
version: '1.0'
---
# Java · 防 NPE

> 本条管「不产生 / 不传播 null」。返回值「可能没有」该用 Optional 见 [`optional-usage.md`](./optional-usage.md)。

## 规则

| 位置 | 做法 |
|------|------|
| 公开方法的入参 | 入口 `Objects.requireNonNull(x, "x 不能为空")` 快速失败 |
| 返回集合 / 数组 | 没数据返回 `Collections.emptyList()` / 空数组，**绝不返回 null** |
| 可空的字段 / 返回值 | 用 `@Nullable` 标注；保证非空用 `@NonNull` |
| 两个对象比较 | `Objects.equals(a, b)`，任一可能为 null 时避免 `a.equals(b)` |
| 已知常量在左 | `"PAID".equals(status)`，避免 status 为 null 触发 NPE |

## 正例

```java
public void register(@NonNull String email, @Nullable String invite) {
    Objects.requireNonNull(email, "email 不能为空");   // 入口快速失败
    // invite 标了 @Nullable，下面必须判空再用
    if (invite != null) { applyInvite(invite); }
}

// 返回空集合，调用方可直接 for 循环，不用判 null
public List<Order> findOrders(Long uid) {
    List<Order> list = repo.select(uid);
    return list != null ? list : Collections.emptyList();
}

// 任一可能 null 的相等比较
if (Objects.equals(order.getStatus(), expected)) { ... }
```

## 反例

```java
// ❌ 返回 null，调用方一个 forEach 就 NPE
public List<Order> findOrders(Long uid) {
    List<Order> list = repo.select(uid);
    return list.isEmpty() ? null : list;
}

// ❌ 左侧可能 null，直接 .equals 触发 NPE
if (status.equals("PAID")) { ... }

// ❌ 不校验，null 一路传到深处才崩，现场难定位
public void register(String email) {
    saveToDb(email.toLowerCase());   // email 为 null 在这里才炸
}
```

## 自检

- [ ] 公开方法的关键入参用 `Objects.requireNonNull` 在入口校验？
- [ ] 返回集合 / 数组的方法没有任何 `return null` 分支？
- [ ] 可空的字段 / 返回值标了 `@Nullable`？
- [ ] 相等比较用 `Objects.equals` 或把已知常量放等号左边？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`optional-usage.md`](./optional-usage.md)（用 Optional 表达「可能没有」的返回值）
- 兄弟：[`equals-hashcode.md`](./equals-hashcode.md)（equals 内部用 Objects.equals 比字段）
