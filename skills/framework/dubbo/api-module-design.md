---
name: dubbo-api-module-design
description: Dubbo API 模块设计 — 接口与 DTO 独立成 api jar、DTO 必须 Serializable、版本兼容不删字段、provider/consumer 共享。Use when 设计 Dubbo RPC 接口 / 拆分 api 模块 / 改动跨服务 DTO 字段时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - API 模块
  - 序列化
  - 版本兼容
  - Serializable
  - DTO
  - api jar
effort: medium
context: inline
version: '1.0'
---
# Apache Dubbo · API 模块设计

> 本条只管「接口/DTO 怎么组织成共享 jar」。怎么暴露见 [`service-export.md`](./service-export.md)；怎么引用见 [`reference-config.md`](./reference-config.md)。

## 规则

| 项 | 约定 |
|----|------|
| 模块边界 | 接口 + DTO + 枚举 + 异常放独立 `xxx-api` jar，provider 与 consumer 都只依赖它 |
| 不含实现 | api jar 禁止含实现类、DAO、Spring 配置等 provider 私有代码 |
| 序列化 | 所有 DTO/入参/返回值 **必须 `implements Serializable`** 并显式声明 `serialVersionUID` |
| 版本兼容 | 演进**只加字段、不删不改类型**；删字段/改类型会让老 consumer 反序列化失败 |
| 内部类型 | DTO 字段只用 JDK/api 内的类型，禁暴露 provider 内部实体（如 JPA Entity） |

## 正例

```java
// xxx-api jar：DTO 实现 Serializable + 固定 serialVersionUID
public class OrderDTO implements Serializable {
    private static final long serialVersionUID = 1L;
    private Long id;
    private String status;
    // 演进时只追加新字段，旧 consumer 不受影响
    private String channel;   // v1.1 新增，老调用方反序列化为 null
    // getters / setters
}
```

```java
// xxx-api jar：只放接口
public interface OrderService {
    OrderDTO getById(Long id);
}
```

## 反例

```java
// ❌ DTO 未实现 Serializable —— 序列化阶段直接抛 NotSerializableException
public class OrderDTO {
    private Long id;
}
```

❌ 删除或重命名已上线 DTO 字段：老 consumer 用旧类反序列化时报错或丢数据。

❌ 接口返回 provider 的 JPA `OrderEntity`，把持久层细节泄漏给所有 consumer。

## 自检

- [ ] 接口/DTO/枚举/异常在独立 api jar，不含任何实现类？
- [ ] 每个 DTO `implements Serializable` 且声明 `serialVersionUID`？
- [ ] 字段演进只增不删、不改类型？
- [ ] 没有把 provider 内部实体（Entity）当返回值暴露？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`service-export.md`](./service-export.md)（provider 暴露 api 里的接口）
- 兄弟：[`reference-config.md`](./reference-config.md)（consumer 引用 api 里的接口）
- 兄弟：[`graceful-degradation.md`](./graceful-degradation.md)（接口异常怎么隔离）
