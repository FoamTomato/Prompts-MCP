---
name: dubbo-service-export
description: Dubbo provider 端用 @DubboService 暴露服务，含 version/group 多版本、timeout 超时、接口与实现分离。Use when 写 Dubbo provider / 暴露 RPC 服务 / 配置服务多版本与超时时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 服务暴露
  - 多版本
  - '@DubboService'
  - version
  - group
  - provider timeout
effort: medium
context: inline
version: '1.0'
---
# Apache Dubbo · 服务暴露（provider）

> 本条只管「provider 怎么暴露服务」。consumer 怎么引用见 [`reference-config.md`](./reference-config.md)；接口/DTO 放哪见 [`api-module-design.md`](./api-module-design.md)。

## 规则

| 项 | 约定 |
|----|------|
| 暴露注解 | 实现类标 `@DubboService`（3.x 注解，替代旧 `@Service`） |
| 接口与实现 | 接口放 api jar，实现类放 provider 模块，禁止 consumer 依赖实现 |
| 多版本 | 不兼容升级用 `version`；同接口多实现/灰度用 `group` 区分 |
| 超时 | 在 provider 侧配 `timeout`（毫秒），给出服务端处理上限 |
| 异步耗时方法 | 长耗时方法单独 `timeout`，勿用全局默认 |

## 正例

```java
// 实现类放 provider 模块；接口在 api jar
@DubboService(version = "1.0.0", group = "order", timeout = 3000)
public class OrderServiceImpl implements OrderService {
    @Override
    public OrderDTO getById(Long id) {
        return orderRepository.find(id);
    }
}
```

```java
// 灰度：同接口两个 group，并行暴露
@DubboService(version = "1.0.0", group = "gray", timeout = 3000)
public class OrderServiceGrayImpl implements OrderService { /* ... */ }
```

## 反例

```java
// ❌ 不写 version：后续不兼容升级时无法与老版本并存，consumer 全量受影响
@DubboService(timeout = 3000)
public class OrderServiceImpl implements OrderService { /* ... */ }
```

❌ 把实现类（`OrderServiceImpl`）放进 api jar 让 consumer 依赖 —— api 模块只该有接口与 DTO（见 api-module-design）。

❌ 完全不配 `timeout`，依赖全局默认 1000ms，耗时方法必然超时报错。

## 自检

- [ ] 实现类用 `@DubboService`，不是 Spring 的 `@Service`？
- [ ] 接口在 api jar，实现类只在 provider 模块？
- [ ] 不兼容变更走了新 `version`，灰度/分组走了 `group`？
- [ ] provider 侧配了与方法耗时匹配的 `timeout`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`reference-config.md`](./reference-config.md)（consumer 怎么引用）
- 兄弟：[`api-module-design.md`](./api-module-design.md)（接口/DTO 放哪）
- 兄弟：[`graceful-degradation.md`](./graceful-degradation.md)（优雅停机不丢请求）
