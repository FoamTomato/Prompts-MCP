---
name: java-optional-usage
description: Optional 正确用法 — 只用于返回值不用于字段/参数，禁裸 get()，orElse vs orElseGet，用 ifPresent/map。Use when 写返回可能为空的方法 / 处理 Optional / 评审 Optional.get() 调用时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - Optional
  - Optional.get
  - orElse
  - orElseGet
  - ifPresent
  - 空值返回
effort: medium
context: inline
version: '1.0'
---
# Java · Optional 正确用法

> 本条只管「Optional 怎么用」。防 NPE 的整体策略（参数校验 / 返回空集合）见 [`null-safety.md`](./null-safety.md)。

## 规则

| 场景 | 做法 |
|------|------|
| 方法可能返回不到值 | 返回类型用 `Optional<T>` |
| 字段 / 方法参数 / 集合元素 | **禁用** Optional（增加序列化与可空层级） |
| 取值 | 用 `orElse` / `orElseGet` / `orElseThrow` / `map` / `ifPresent`，**禁裸 `get()`** |
| 默认值是常量 | `orElse(default)` |
| 默认值要现算 / 有开销 | `orElseGet(() -> ...)`（惰性，不命中才执行） |

## 正例

```java
// 返回值用 Optional 表达「可能没有」
public Optional<User> findByEmail(String email) {
    return Optional.ofNullable(repo.selectByEmail(email));
}

// 链式取值，不解包就处理
findByEmail(email)
    .map(User::getName)
    .ifPresent(name -> log.info("found {}", name));

// 取不到就抛业务异常
User u = findByEmail(email)
    .orElseThrow(() -> new BusinessException("用户不存在"));

// 默认值有开销 → orElseGet 惰性求值
Config c = loadCustom().orElseGet(this::buildDefaultConfig);
```

## 反例

```java
// ❌ 裸 get() 不判断，Optional 退化成更啰嗦的 NPE
User u = findByEmail(email).get();

// ❌ Optional 当字段，徒增可空层级 + 序列化坑
public class Order {
    private Optional<Coupon> coupon;   // 用 Coupon coupon; 即可
}

// ❌ orElse 里放有开销的调用：无论命不命中都会执行
Config c = loadCustom().orElse(buildDefaultConfig());  // 总是 build
```

## 自检

- [ ] Optional 只出现在**返回值**，没用作字段 / 参数 / 集合元素？
- [ ] 没有不先 `isPresent()` / 不带 orElse 的裸 `get()`？
- [ ] 默认值有开销时用了 `orElseGet` 而非 `orElse`？
- [ ] 能用 `map` / `ifPresent` 链式处理的没强行解包？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`null-safety.md`](./null-safety.md)（参数校验、返回空集合不返回 null）
