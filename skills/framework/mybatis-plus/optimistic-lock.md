---
name: mybatis-plus-optimistic-lock
description: MyBatis-Plus 乐观锁用 @Version 标记版本字段，更新自动加 version 条件并自增，防并发丢失更新。Use when 防并发覆盖 / 加 @Version / 配 OptimisticLockerInnerInterceptor 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 乐观锁
  - 丢失更新
  - '@Version'
  - 版本号
  - OptimisticLockerInnerInterceptor
effort: medium
context: inline
version: '1.0'
---
# MyBatis-Plus · 乐观锁

> 本条只管「乐观锁版本号怎么配」。分页等其它内部拦截器的注册见 [`pagination.md`](./pagination.md)。

## 规则

| 事项 | 约定 |
|------|------|
| 版本字段 | 实体加 `@Version` 字段（`Integer`/`Long`/时间戳），表里建对应列 |
| 必配拦截器 | 注册 `OptimisticLockerInnerInterceptor` 到 `MybatisPlusInterceptor`，**不配则 @Version 不生效** |
| 更新行为 | `updateById` 自动改为 `SET ... version=version+1 WHERE id=? AND version=?` |
| 必带版本值 | 更新前实体里**必须有查出来的 version 值**，否则条件命中不到行 |
| 判断结果 | 更新返回**影响行数**：返回 0 说明版本已被改、更新失败，业务要重试或报错 |
| 生效范围 | 仅对 `updateById` / `update(entity, wrapper)` 生效；自定义 SQL 不自动加版本条件 |

## 正例

```java
// ✅ 实体：版本字段加 @Version
public class Account {
    @TableId
    private Long id;
    private Long balance;

    @Version          // 配合 OptimisticLockerInnerInterceptor 生效
    private Integer version;
}

// 先查（拿到 version），改，再 updateById：
final Account acc = accountMapper.selectById(id);
acc.setBalance(acc.getBalance() - amount);
// 底层 UPDATE ... version=version+1 WHERE id=? AND version=?
final int rows = accountMapper.updateById(acc);
if (rows == 0) {
    throw new BizException("并发更新冲突，请重试");   // 版本已变
}
```

## 反例

```java
// ❌ 不先查直接 new 一个没 version 的实体去更新 —— version 为 null
//    WHERE version=null 命中不到行，更新静默失败
Account acc = new Account();
acc.setId(id);
acc.setBalance(newBalance);
accountMapper.updateById(acc);   // rows=0 且没人检查，丢更新

// ❌ 忽略返回行数 —— 冲突时悄无声息地丢失更新
accountMapper.updateById(acc);   // 没判断 rows
```

理由：乐观锁靠 `WHERE version=?` 实现，更新实体必须携带查询时的旧 version；且冲突时影响行数为 0，不检查返回值等于没有乐观锁。

## 自检

- [ ] 版本字段加了 `@Version`，表里有对应列？
- [ ] 注册了 `OptimisticLockerInnerInterceptor`？
- [ ] 更新前先查出实体（带 version），不是 new 空对象？
- [ ] 检查了 `updateById` 返回行数，为 0 时重试或报错？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`pagination.md`](./pagination.md)（同为内部拦截器，注意注册顺序）
- 兄弟：[`lambda-wrapper.md`](./lambda-wrapper.md)（自定义 update 条件不自动加版本号）
