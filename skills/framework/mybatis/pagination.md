---
name: mybatis-pagination
description: MyBatis 物理分页 — PageHelper.startPage 或 MyBatis-Plus IPage 下推 limit，禁 RowBounds 全查内存分页，count 查询单独优化。Use when 写分页列表接口 / 排查分页慢或 OOM / 评审 RowBounds 用法时。
parent: ./index.md
paths:
- '*.java'
- '*.xml'
triggers:
  keywords:
  - 物理分页
  - PageHelper
  - IPage
  - RowBounds
  - 内存分页
  - count 优化
effort: medium
context: inline
version: '1.0'
---
# MyBatis · 分页

> 本条只管「分页怎么做对」。关联数据导致的循环查见 [`n-plus-one.md`](./n-plus-one.md)。

## 规则

| 事项 | 约定 |
|------|------|
| 分页方式 | **物理分页**：PageHelper 拦截器 或 MyBatis-Plus `IPage`，把 `limit/offset` 下推到 SQL |
| 禁用 | `RowBounds`（先全查再内存截断，大表 OOM）、`subList` 手动截断 |
| startPage 位置 | PageHelper 必须**紧贴**要分页的那条查询，中间不夹其它查询 |
| count | 框架自动生成 count；count 慢时手写 `countXxx`，去掉 join / order by |
| 深分页 | `offset` 很大时改用「游标 / 上次最大 id」键集分页 |

## 正例

```java
// ✅ PageHelper：startPage 紧贴下一条查询
PageHelper.startPage(pageNum, pageSize);
List<User> list = userMapper.listByStatus(status);   // 自动 limit
PageInfo<User> page = new PageInfo<>(list);           // total / pages 自动算
```

```java
// ✅ MyBatis-Plus IPage：分页对象下推
IPage<User> page = new Page<>(pageNum, pageSize);
userMapper.selectPage(page, new LambdaQueryWrapper<User>().eq(User::getStatus, status));
```

## 反例

```java
// ❌ RowBounds：MyBatis 把全表查进内存再截断 —— 百万行直接 OOM
userMapper.list(new RowBounds(offset, limit));

// ❌ 全查后 subList：同样把全量拉进内存
List<User> all = userMapper.listAll();
return all.subList(offset, offset + size);

// ❌ startPage 后先查了别的，分页作用到错的查询上
PageHelper.startPage(p, s);
userMapper.countSomething();   // 分页被它消费掉了
List<User> list = userMapper.list();
```

理由：`RowBounds` / `subList` 是逻辑分页，数据量一大就拉爆内存；PageHelper 的 `startPage` 只对其后第一条查询生效，插队的查询会把分页吃掉。

## 自检

- [ ] 用 PageHelper 或 IPage 物理分页，没用 RowBounds / subList？
- [ ] `startPage` 紧贴目标查询，中间无其它查询？
- [ ] count 慢时单独写了去 join / 去 order by 的 count？
- [ ] 深分页场景评估了键集分页？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`n-plus-one.md`](./n-plus-one.md)（分页列表再带关联数据时的循环查）
- 兄弟：[`mapper-interface.md`](./mapper-interface.md)（分页方法的返回类型）
