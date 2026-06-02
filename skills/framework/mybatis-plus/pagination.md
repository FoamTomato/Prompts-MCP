---
name: mybatis-plus-pagination
description: MyBatis-Plus 分页必须注册 PaginationInnerInterceptor 拦截器，否则 selectPage 不下推 limit、total 恒为 0。Use when 配 MP 分页 / 排查 page 不生效或 total 为 0 / 评审分页配置时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 分页插件
  - PaginationInnerInterceptor
  - MybatisPlusInterceptor
  - selectPage
  - IPage
  - 分页不生效
effort: medium
context: inline
version: '1.0'
---
# MyBatis-Plus · 分页插件配置

> 本条只管「MP 分页插件怎么配、怎么用」。物理分页 vs 内存分页的通用原理见 [`../mybatis/pagination.md`](../mybatis/pagination.md)。

## 规则

| 事项 | 约定 |
|------|------|
| 必配拦截器 | 注册 `MybatisPlusInterceptor` 并加 `PaginationInnerInterceptor`，**不配则 limit 不下推、total 恒为 0** |
| 指定数据库类型 | `new PaginationInnerInterceptor(DbType.MYSQL)`，让方言生成对应分页 SQL |
| 分页对象 | `IPage<T> page = new Page<>(current, size)`，`current` 从 1 起（不是 0） |
| 取结果 | `page.getRecords()` 拿列表，`page.getTotal()` 拿总数，框架自动算 count |
| 多插件顺序 | 分页拦截器要放在**乐观锁等其它内部拦截器之前**注册 |

## 正例

```java
// ✅ 配置类：注册分页拦截器（少这段则分页彻底不生效）
@Configuration
public class MybatisPlusConfig {
    @Bean
    public MybatisPlusInterceptor mybatisPlusInterceptor() {
        final MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
        interceptor.addInnerInterceptor(new PaginationInnerInterceptor(DbType.MYSQL));
        return interceptor;
    }
}
```

```java
// ✅ 使用：current 从 1 起，records + total 一并返回
final IPage<User> page = new Page<>(current, size);
final IPage<User> result = userMapper.selectPage(page,
        Wrappers.<User>lambdaQuery().eq(User::getStatus, status));
// result.getRecords() / result.getTotal()
```

## 反例

```java
// ❌ 没注册 PaginationInnerInterceptor：selectPage 退化成全表查
//    limit 不下推，getTotal() 永远是 0，page 形同虚设
IPage<User> page = new Page<>(1, 10);
userMapper.selectPage(page, wrapper);   // 全表拉进内存，大表 OOM
```

理由：MP 的分页是靠拦截器改写 SQL 实现的，不注册拦截器 `selectPage` 就只是普通全表查询，`limit` 不会拼进 SQL，`total` 也不会被计算。

## 自检

- [ ] 配置类注册了 `MybatisPlusInterceptor` + `PaginationInnerInterceptor`？
- [ ] 构造时指定了 `DbType`（如 MySQL）？
- [ ] `Page` 的 `current` 从 1 起，不是 0？
- [ ] 同时用乐观锁时，分页拦截器在乐观锁拦截器之前注册？

## 相关

- 父：[`./index.md`](./index.md)
- 通用分页原理：[`../mybatis/pagination.md`](../mybatis/pagination.md)（物理 vs 内存分页、深分页）
- 兄弟：[`optimistic-lock.md`](./optimistic-lock.md)（同为内部拦截器，注意注册顺序）
