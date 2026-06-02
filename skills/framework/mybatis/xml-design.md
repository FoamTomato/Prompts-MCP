---
name: mybatis-xml-design
description: MyBatis Mapper XML 设计 — namespace 对应接口全限定名、resultMap 显式映射不靠隐式驼峰、sql 片段 + include 复用列名。Use when 写 Mapper XML / 设计结果映射 / 评审 XML 重复列名时。
parent: ./index.md
paths:
- '*.xml'
triggers:
  keywords:
  - 结果映射
  - resultMap
  - namespace
  - sql 片段
  - include
  - 驼峰映射
effort: medium
context: inline
version: '1.0'
---
# MyBatis · Mapper XML 设计

> 本条只管「XML 的结构怎么搭」。接口怎么写见 [`mapper-interface.md`](./mapper-interface.md)；动态条件见 [`dynamic-sql.md`](./dynamic-sql.md)。

## 规则

| 事项 | 约定 |
|------|------|
| namespace | 等于对应 Mapper 接口的**全限定名**，一字不差 |
| 结果映射 | 用 `resultMap` **显式映射**列↔字段，不依赖隐式下划线转驼峰 |
| 列清单 | 抽成 `<sql id="Base_Column_List">` 片段，靠 `<include>` 复用 |
| id 引用 | `select` 的 `id` 等于接口方法名；`parameterType` 可省，靠 `#{}` 推断 |
| 返回声明 | 返回 POJO 用 `resultMap`（或 `resultType`），别同时写两个 |

## 正例

```xml
<mapper namespace="com.x.mapper.UserMapper">

  <resultMap id="BaseResultMap" type="com.x.entity.User">
    <id     column="id"        property="id"/>
    <result column="user_name" property="userName"/>
    <result column="dept_id"   property="deptId"/>
  </resultMap>

  <sql id="Base_Column_List">
    id, user_name, dept_id
  </sql>

  <select id="selectById" resultMap="BaseResultMap">
    select <include refid="Base_Column_List"/>
    from user where id = #{id}
  </select>
</mapper>
```

## 反例

```xml
<!-- ❌ 靠隐式驼峰：没开 mapUnderscoreToCamelCase 时 user_name 映射不到 userName -->
<select id="selectById" resultType="com.x.entity.User">
  select id, user_name, dept_id from user where id = #{id}
</select>

<!-- ❌ 列名硬抄三遍：新增字段要改 N 处，必漏 -->
<select id="list" resultType="...">select id, user_name, dept_id from user</select>
```

理由：隐式驼峰依赖全局开关，跨项目/跨配置不可靠；显式 `resultMap` 把映射写死、可读可控。列清单抽片段后只维护一处。

## 自检

- [ ] `namespace` 与 Mapper 接口全限定名完全一致？
- [ ] 列↔字段用 `resultMap` 显式映射，没指望隐式驼峰？
- [ ] 列清单抽成 `<sql>` + `<include>`，没有多处硬抄？
- [ ] `select` 的 `id` 与接口方法名一致？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mapper-interface.md`](./mapper-interface.md)（XML 对应的接口）
- 兄弟：[`dynamic-sql.md`](./dynamic-sql.md)（XML 里的动态条件）
- 兄弟：[`n-plus-one.md`](./n-plus-one.md)（resultMap 嵌套关联映射）
