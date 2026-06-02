---
name: mybatis-plus-logic-delete
description: MyBatis-Plus 逻辑删除用 @TableLogic 标记删除字段，delete 改为 update deleted=1，查询自动追加 deleted=0。Use when 做软删除 / 加 @TableLogic / 排查删过的数据仍被查出时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 逻辑删除
  - 软删除
  - '@TableLogic'
  - deleted 字段
  - logic-delete-field
effort: medium
context: inline
version: '1.0'
---
# MyBatis-Plus · 逻辑删除

> 本条只管「软删除怎么配」。物理删除/更新条件构造见 [`lambda-wrapper.md`](./lambda-wrapper.md)。

## 规则

| 事项 | 约定 |
|------|------|
| 标记字段 | 删除标记字段（如 `deleted`）加 `@TableLogic`，类型用 `Integer`/`Boolean` |
| 删除行为 | 加注解后 `deleteById` 等**自动改为 `UPDATE ... SET deleted=1`**，不真删行 |
| 查询行为 | 所有 MP 内置查询**自动追加 `WHERE deleted=0`**，删过的数据查不出来 |
| 全局配置 | 字段名/删除值/未删值统一在 `mybatis-plus.global-config.db-config` 配：`logic-delete-field`、`logic-delete-value`、`logic-not-delete-value` |
| XML 不自动 | 手写 XML 的 SQL **不会**自动加 `deleted=0`，需自己在 where 里写 |
| 唯一索引坑 | 逻辑删除后旧行还在，唯一索引可能冲突；唯一键需带 deleted 或用其它去重策略 |

## 正例

```java
// ✅ 实体：删除标记加 @TableLogic
public class User {
    @TableId
    private Long id;
    private String name;

    @TableLogic           // 0=未删 1=已删，可全局配置默认值
    private Integer deleted;
}

// 调用：底层是 UPDATE user SET deleted=1 WHERE id=? AND deleted=0
userMapper.deleteById(id);
// 查询：底层自动 SELECT ... WHERE deleted=0
userMapper.selectList(Wrappers.<User>lambdaQuery().eq(User::getStatus, 1));
```

## 反例

```java
// ❌ 手写 XML 误以为也会自动过滤 —— XML 的 SQL 不享受逻辑删除拦截
//    <select id="listAll">SELECT * FROM user</select>   会把已删的也查出来
List<User> all = userMapper.listAll();   // 含 deleted=1 的脏数据
```

理由：逻辑删除靠 MP 注入的内置方法与 Wrapper 拦截实现，手写 XML 不经过这层，必须自己在 `where` 显式加 `deleted = 0`。

## 自检

- [ ] 删除标记字段加了 `@TableLogic`（或配了全局 `logic-delete-field`）？
- [ ] 确认内置查询自动带 `deleted=0`，无需手写？
- [ ] 手写 XML 的查询自己加了 `deleted = 0` 条件？
- [ ] 评估了逻辑删除对唯一索引的影响？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`coexist-with-xml.md`](./coexist-with-xml.md)（XML 不享受逻辑删除拦截，注意分工）
- 兄弟：[`auto-fill.md`](./auto-fill.md)（删除时间等审计字段填充）
