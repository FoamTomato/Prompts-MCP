---
name: mybatis-dynamic-sql
description: MyBatis 动态 SQL 标签 — if 条件拼接、where 自动去 AND/OR 前缀、foreach 批量插入与 IN、choose 多分支。Use when 写带可选条件的查询 / 拼 IN 列表 / 批量 insert / 评审手拼 where 的 XML 时。
parent: ./index.md
paths:
- '*.xml'
triggers:
  keywords:
  - 动态 SQL
  - foreach 批量
  - dynamic SQL
  - if where choose
  - 批量插入
  - IN 查询
effort: medium
context: inline
version: '1.0'
---
# MyBatis · 动态 SQL

> 本条只管「条件/批量怎么动态拼」。`#{}` vs `${}` 的注入安全见 [`sql-injection-safety.md`](./sql-injection-safety.md)；XML 整体结构见 [`xml-design.md`](./xml-design.md)。

## 规则

| 标签 | 用途 |
|------|------|
| `<if test="...">` | 参数非空才拼这段条件 |
| `<where>` | 包裹条件，**自动加 where 并去掉开头多余的 AND/OR** |
| `<foreach>` | 遍历集合：拼 `IN (...)` 或批量 `insert` 的 values |
| `<choose>/<when>/<otherwise>` | 多选一分支（类似 switch） |
| `<set>` | update 时自动去掉末尾逗号 |

## 正例

```xml
<!-- where 自动处理首个 AND；if 控制可选条件 -->
<select id="list" resultMap="BaseResultMap">
  select <include refid="Base_Column_List"/> from user
  <where>
    <if test="status != null">  and status = #{status}  </if>
    <if test="name != null and name != ''"> and user_name = #{name} </if>
  </where>
</select>

<!-- foreach 拼 IN -->
<select id="listByIds" resultMap="BaseResultMap">
  select <include refid="Base_Column_List"/> from user
  where id in
  <foreach collection="ids" item="id" open="(" separator="," close=")">#{id}</foreach>
</select>

<!-- foreach 批量插入：一条 INSERT 多组 values -->
<insert id="batchInsert">
  insert into user (user_name, dept_id) values
  <foreach collection="list" item="u" separator=",">(#{u.userName}, #{u.deptId})</foreach>
</insert>
```

## 反例

```xml
<!-- ❌ 手写 where 1=1 凑前缀 —— 多余、且每次全表扫描没省事 -->
<select id="list">select * from user where 1=1
  <if test="status != null"> and status = #{status}</if>
</select>

<!-- ❌ 循环里单条 insert（见 n-plus-one）：N 次往返，应改 foreach 批量 -->
```

理由：`<where>` 已自动补 `where` 并裁掉第一个 `AND`，`where 1=1` 是冗余 hack；批量 insert 必须 `foreach` 拼一条语句，避免逐条往返。

## 自检

- [ ] 可选条件用 `<where>` + `<if>`，没写 `where 1=1`？
- [ ] update 用 `<set>` 而非手拼逗号？
- [ ] `IN` 列表用 `<foreach>`，没字符串拼接？
- [ ] 批量写库用 `foreach` 拼一条 insert，不在 Java 循环里单条执行？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`sql-injection-safety.md`](./sql-injection-safety.md)（拼接里 `#{}` vs `${}`）
- 兄弟：[`xml-design.md`](./xml-design.md)（XML 结构与片段复用）
- 兄弟：[`n-plus-one.md`](./n-plus-one.md)（批量查替代循环单查）
