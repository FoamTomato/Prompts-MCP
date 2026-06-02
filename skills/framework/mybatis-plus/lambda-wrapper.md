---
name: mybatis-plus-lambda-wrapper
description: MyBatis-Plus 条件构造器优先用 LambdaQueryWrapper，方法引用代替字段名硬编码字符串，编译期校验、改名重构安全。Use when 拼查询/更新条件 / 改 QueryWrapper 字符串字段名 / 评审 Wrapper 用法时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 条件构造器
  - 字段名硬编码
  - LambdaQueryWrapper
  - LambdaUpdateWrapper
  - 方法引用
  - QueryWrapper
effort: medium
context: inline
version: '1.0'
---
# MyBatis-Plus · 条件构造器类型安全

> 本条只管「条件构造器怎么写才安全」。复杂业务 SQL 该不该用 Wrapper 见 [`coexist-with-xml.md`](./coexist-with-xml.md)。

## 规则

| 事项 | 约定 |
|------|------|
| 优先 Lambda 版 | 用 `LambdaQueryWrapper` / `LambdaUpdateWrapper`，字段用方法引用 `User::getStatus`，**不写字符串列名** |
| 禁字符串列名 | 普通 `QueryWrapper.eq("staus", x)` 拼错字段名编译期发现不了，运行时才报错 |
| 条件留空保护 | 用 `condition` 重载：`.eq(status != null, User::getStatus, status)`，null 不拼该条件 |
| select 指定列 | 只查需要列用 `.select(User::getId, User::getName)`，别 `select *` 拉大字段 |
| 链式入口 | 也可 `new LambdaQueryWrapper<User>()` 或 `Wrappers.lambdaQuery(User.class)` |

## 正例

```java
// ✅ 方法引用：字段名编译期校验，改名 IDE 自动重构
final LambdaQueryWrapper<User> wrapper = Wrappers.<User>lambdaQuery()
        .eq(User::getStatus, status)
        // condition 重载：keyword 为空就不拼这条
        .like(StringUtils.hasText(keyword), User::getName, keyword)
        .orderByDesc(User::getCreateTime);
final List<User> list = userMapper.selectList(wrapper);
```

## 反例

```java
// ❌ 字符串列名：拼错 "staus" 编译通过、运行才炸；字段改名不会提示
QueryWrapper<User> wrapper = new QueryWrapper<>();
wrapper.eq("staus", status)        // 列名拼错，无编译期保护
       .like("name", keyword);     // keyword 为 null 也照拼，结果错
```

理由：字符串列名绕过编译器，字段重命名后这些字符串成「哑弹」；Lambda 方法引用让列名跟着实体字段走，改名即报错。

## 自检

- [ ] 用的是 `LambdaQueryWrapper` / `LambdaUpdateWrapper`，没有字符串列名？
- [ ] 可空入参用了 `condition` 重载，避免拼出错误条件？
- [ ] 大字段表用 `.select(...)` 限定了列，没有隐式 `select *`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`coexist-with-xml.md`](./coexist-with-xml.md)（复杂 SQL 别用 Wrapper 拼，走 XML）
- 兄弟：[`pagination.md`](./pagination.md)（Wrapper 配合 `IPage` 分页）
