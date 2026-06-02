---
name: mybatis-sql-injection-safety
description: "MyBatis 防 SQL 注入红线 — #{} 走预编译占位符，${} 是字符串拼接仅用于表名/列名等无法占位处且必须白名单校验。Use when XML 里拼参数 / 写 order by 动态列 / 评审含 ${} 的 SQL 时。"
parent: ./index.md
paths:
- '*.xml'
triggers:
  keywords:
  - SQL 注入
  - 预编译
  - SQL injection
  - 占位符
  - 白名单校验
  - order by 注入
effort: high
context: inline
version: '1.0'
---
# MyBatis · #{} vs ${} 注入安全

> 本条只管「防注入：何时用 `#{}`、何时不得不用 `${}`」。条件拼接标签见 [`dynamic-sql.md`](./dynamic-sql.md)。

## 规则（安全红线）

| 写法 | 机制 | 何时用 |
|------|------|--------|
| `#{param}` | 生成 `?` **预编译占位符**，值经 JDBC 转义 | **默认全用这个**，所有传入值 |
| `${param}` | 直接**字符串拼接**进 SQL，不转义 | 仅限无法占位的位置：表名 / 列名 / `order by` 字段 / `asc·desc` |

> `${}` 任何来自用户输入的值都是注入入口。用 `${}` 时该值**必须先经白名单校验**（枚举允许的列名/方向），绝不直接拼请求参数。

## 正例

```xml
<!-- ✅ 普通条件值一律 #{} -->
<select id="findByName" resultMap="BaseResultMap">
  select * from user where user_name = #{name} and status = #{status}
</select>
```

```java
// ✅ 排序列必须 ${}（列名不能占位），先白名单校验再传入
private static final Set<String> SORTABLE = Set.of("created_at", "user_name");

public List<User> list(String sortColumn, String dir) {
    if (!SORTABLE.contains(sortColumn)) throw new IllegalArgumentException("非法排序列");
    String d = "DESC".equalsIgnoreCase(dir) ? "DESC" : "ASC";  // 方向也白名单
    return userMapper.list(sortColumn, d);
}
```
```xml
<select id="list" resultMap="BaseResultMap">
  select * from user order by ${sortColumn} ${dir}
</select>
```

## 反例

```xml
<!-- ❌ 用 ${} 拼条件值 —— 经典注入：name=' or '1'='1 拖库 -->
<select id="findByName">select * from user where user_name = '${name}'</select>

<!-- ❌ order by 直接拼未校验的请求参数 -->
<select id="list">select * from user order by ${sortColumn}</select>
```

理由：`${}` 把值原样拼进 SQL，攻击者可闭合引号注入任意语句；`#{}` 走预编译，参数永远是数据而非 SQL 结构。

## 自检

- [ ] 所有条件值、写入值都用 `#{}`，没有一个 `${}`？
- [ ] 仅表名/列名/排序方向不得不用 `${}`？
- [ ] 每个 `${}` 的值都经过白名单（枚举集合）校验，非直接拼请求参数？
- [ ] `order by` 的字段名和 asc/desc 方向都白名单了？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`dynamic-sql.md`](./dynamic-sql.md)（动态条件拼接里的占位）
- 兄弟：[`xml-design.md`](./xml-design.md)（XML 整体结构）
