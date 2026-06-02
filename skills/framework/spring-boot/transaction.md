---
name: spring-boot-transaction
description: Spring Boot 事务 — @Transactional 失效场景（自调用/非 public/异常被 catch/默认只回滚 RuntimeException）、传播行为、只读事务。Use when 加 @Transactional 不回滚 / 排查事务不生效 / 选传播级别时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 事务失效
  - 事务回滚
  - '@Transactional'
  - 传播行为
  - rollbackFor
  - 只读事务
effort: medium
context: inline
version: '1.0'
---
# Spring Boot · 事务

> 本条只管「@Transactional 为什么不生效 / 不回滚，以及传播怎么选」。异常类型选型见 [`checked-vs-runtime.md`](../../lang/java/error-handling/checked-vs-runtime.md)。

## 失效场景（最常见的坑）

| 失效原因 | 为什么 | 修法 |
|----------|--------|------|
| 同类内 `this.方法()` 自调用 | 没走 Spring 代理，注解被跳过 | 拆到另一个 Bean，或注入自身代理 |
| 方法非 `public` | 代理只增强 public 方法 | 改 public |
| 异常被自己 catch 没重抛 | 代理感知不到异常，不回滚 | catch 后重抛，或手动 `setRollbackOnly` |
| 抛的是 Checked 异常 | 默认**只回滚 RuntimeException/Error** | `@Transactional(rollbackFor = Exception.class)` |
| 方法所在类没被 Spring 管理 | 没代理 | 标 `@Service` 等纳入容器 |

## 传播与只读

| 配置 | 含义 |
|------|------|
| `REQUIRED`（默认） | 有事务就加入，没有就新建 |
| `REQUIRES_NEW` | 总是新建独立事务，挂起外层（如日志要独立提交） |
| `NESTED` | 嵌套保存点，外层回滚带着它回 |
| `readOnly = true` | 纯查询方法标只读，给数据库/连接池优化提示 |

## 正例

```java
@Service
@RequiredArgsConstructor
public class OrderService {

    // ✅ rollbackFor 让 Checked 异常也回滚
    @Transactional(rollbackFor = Exception.class)
    public void placeOrder(OrderDTO dto) throws BizCheckedException {
        orderMapper.insert(dto);
        inventoryService.deduct(dto);  // 失败则整体回滚
    }

    @Transactional(readOnly = true)
    public OrderVO detail(Long id) {
        return orderMapper.selectById(id);
    }
}
```

## 反例

```java
// ❌ 自调用：save() 上的 @Transactional 完全不生效
@Service
public class OrderService {
    public void handle(OrderDTO dto) {
        this.save(dto);   // 走 this，绕过代理
    }
    @Transactional
    public void save(OrderDTO dto) { /* ... */ }
}
```

```java
// ❌ 抛 Checked 但没配 rollbackFor —— 数据已写入，不回滚
@Transactional
public void save() throws IOException {
    mapper.insert(x);
    throw new IOException(); // 不触发回滚！
}
```

## 自检

- [ ] 没有同类自调用 `this.事务方法()`（否则注解失效）？
- [ ] `@Transactional` 标在 `public` 方法上？
- [ ] catch 了异常的话有重抛或 `setRollbackOnly`，没静默吞？
- [ ] 需要 Checked 异常回滚时配了 `rollbackFor`？
- [ ] 纯查询方法标了 `readOnly = true`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`bean-injection.md`](./bean-injection.md)（自调用绕过代理与注入相关）
- 跨模块：[`checked-vs-runtime.md`](../../lang/java/error-handling/checked-vs-runtime.md)（Checked vs Runtime 选型，影响默认回滚）
