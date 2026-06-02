---
name: mybatis-mapper-interface
description: MyBatis Mapper 接口规范 — @Mapper / @MapperScan 注册、方法名语义化、多参数加 @Param、返回类型约定。Use when 新建 Mapper 接口 / 加查询方法 / 评审持久层接口签名时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 映射器接口
  - Mapper 接口
  - '@Mapper'
  - '@MapperScan'
  - '@Param'
  - 返回类型
effort: medium
context: inline
version: '1.0'
---
# MyBatis · Mapper 接口规范

> 本条只管「Mapper 接口怎么写」。对应的 XML 怎么写见 [`xml-design.md`](./xml-design.md)；动态条件见 [`dynamic-sql.md`](./dynamic-sql.md)。

## 规则

| 事项 | 约定 |
|------|------|
| 注册方式 | 接口加 `@Mapper`，或在配置类用 `@MapperScan("com.x.mapper")` 统一扫描（二选一，不重复） |
| 方法名 | 语义化前缀：`selectById` / `listByStatus` / `insert` / `update` / `deleteById` / `countBy...` |
| 多参数 | ≥2 个参数**每个都加 `@Param`**，XML 里用 `#{paramName}` 引用 |
| 单参数对象 | 传 POJO / Map 时可不加 `@Param`，XML 直接用属性名 |
| 返回单条 | 返回实体或 `Optional<T>`，不存在返回 null / 空 Optional |
| 返回多条 | 返回 `List<T>`，**查不到返回空集合**，绝不返回 null |
| 返回计数 | `count` 类方法返回 `long` |

## 正例

```java
@Mapper
public interface UserMapper {

    User selectById(@Param("id") Long id);

    // 多参数：每个都标 @Param，XML 用 #{status}/#{deptId}
    List<User> listByStatusAndDept(@Param("status") Integer status,
                                   @Param("deptId") Long deptId);

    // 单 POJO 参数可不加 @Param，XML 直接用 #{name}/#{email}
    int insert(User user);

    long countByStatus(@Param("status") Integer status);
}
```

## 反例

```java
// ❌ 多参数不加 @Param —— XML 里只能用 #{param1}/#{arg0}，可读性差且易错
List<User> list(Integer status, Long deptId);

// ❌ 方法名无语义（get/query 含糊）+ 返回 null 列表
List<User> get(Integer s);   // 调用方 forEach 直接 NPE
```

理由：列表返回 null 会让调用方每次都判空，违背集合「空而非 null」惯例；多参数不加 `@Param` 时 XML 引用名不稳定。

## 自检

- [ ] 接口只用一种注册方式（`@Mapper` 或 `@MapperScan`），没重复？
- [ ] 方法名带语义前缀（select/list/insert/update/delete/count）？
- [ ] ≥2 参数的方法每个参数都加了 `@Param`？
- [ ] 返回 `List` 的方法保证空集合而非 null？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`xml-design.md`](./xml-design.md)（接口对应的 XML 怎么写）
- 兄弟：[`dynamic-sql.md`](./dynamic-sql.md)（多参数的动态条件拼接）
