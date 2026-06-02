---
name: mybatis-plus-auto-fill
description: MyBatis-Plus 自动填充用 @TableField(fill) 标字段加 MetaObjectHandler 实现，统一写 createTime/updateTime，不在业务里手填。Use when 配审计字段自动填充 / 实现 MetaObjectHandler / 排查填充不生效时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 自动填充
  - 审计字段
  - MetaObjectHandler
  - '@TableField'
  - createTime
  - updateTime
effort: medium
context: inline
version: '1.0'
---
# MyBatis-Plus · 自动填充

> 本条只管「createTime/updateTime 等审计字段怎么自动填」。删除标记的填充另见 [`logic-delete.md`](./logic-delete.md)。

## 规则

| 事项 | 约定 |
|------|------|
| 标记字段 | 字段加 `@TableField(fill = FieldFill.INSERT)` 或 `INSERT_UPDATE`，标明何时填 |
| 处理器 | 实现 `MetaObjectHandler` 并 `@Component` 注册，重写 `insertFill` / `updateFill` |
| 填充时机 | `createTime` 用 `INSERT`；`updateTime` 用 `INSERT_UPDATE`（插入和更新都填） |
| 严格填充 | 优先用 `strictInsertFill` / `strictUpdateFill`，按字段类型安全赋值 |
| 仅内置方法 | 自动填充只在 MP 内置 `insert`/`update` 生效；手写 XML 的 insert 不会触发 |
| 别业务里手填 | 不在 Service 里到处 `setCreateTime(now())`，统一交处理器，避免遗漏与不一致 |

## 正例

```java
// ✅ 实体：标注填充时机
public class User {
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;

    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;
}
```

```java
// ✅ 处理器：统一填充，业务层无需关心
@Component
public class AuditMetaHandler implements MetaObjectHandler {
    @Override
    public void insertFill(MetaObject metaObject) {
        final LocalDateTime now = LocalDateTime.now();
        this.strictInsertFill(metaObject, "createTime", LocalDateTime.class, now);
        this.strictInsertFill(metaObject, "updateTime", LocalDateTime.class, now);
    }
    @Override
    public void updateFill(MetaObject metaObject) {
        this.strictUpdateFill(metaObject, "updateTime", LocalDateTime.class, LocalDateTime.now());
    }
}
```

## 反例

```java
// ❌ 字段没标 @TableField(fill=...)，处理器再写也不触发 —— 填充不生效
private LocalDateTime createTime;   // 缺 fill 标记

// ❌ 在每个 Service 方法里手填，漏一处就脏一条
user.setCreateTime(LocalDateTime.now());   // 散落各处，迟早遗漏
userMapper.insert(user);
```

理由：自动填充靠「字段 fill 标记 + MetaObjectHandler」两者配合，缺一不生效；手工 set 散落各处迟早漏填，正是自动填充要消除的。

## 自检

- [ ] 审计字段加了 `@TableField(fill = ...)` 且时机正确（create 用 INSERT，update 用 INSERT_UPDATE）？
- [ ] `MetaObjectHandler` 实现类加了 `@Component`？
- [ ] 用了 `strictInsertFill` / `strictUpdateFill`？
- [ ] 业务层不再手动 `setCreateTime/setUpdateTime`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`logic-delete.md`](./logic-delete.md)（删除标记字段填充，同样不走 XML）
- 兄弟：[`coexist-with-xml.md`](./coexist-with-xml.md)（手写 XML 不触发自动填充）
