---
name: framework-index
description: 框架/库使用约定索引 — 前端(React/antd/Vue3/Element Plus/GSAP) / Python(FastAPI/Tortoise) / Java(Spring 全家桶/MyBatis(-Plus)/MySQL/Redis/MQ/Security/调度/测试等)。Use when 写具体框架代码 / 用第三方库 / 评审框架用法时。
parent: ../index.md
children:
  - { name: react, path: react/index.md, tag: folder, note: 组件 / hook / state / 布局 / 性能 / 安全 / React19 }
  - { name: antd, path: antd/index.md, tag: folder, note: Form / Modal / Table / 组件选型 }
  - { name: vue, path: vue/index.md, tag: folder, note: Vue3 组合式 API / 响应式 / SFC / Pinia / Router }
  - { name: element-plus, path: element-plus/index.md, tag: folder, note: ElForm / ElTable / 主题 / 消息反馈 }
  - { name: fastapi, path: fastapi/index.md, tag: folder, note: router / schema / middleware }
  - { name: tortoise, path: tortoise/index.md, tag: folder, note: model 类模板 / 事务上下文 }
  - { name: gsap, path: gsap/index.md, tag: folder, note: FLIP / Draggable 动画 }
  - { name: spring-boot, path: spring-boot/index.md, tag: folder, note: "Controller / 全局异常 / 校验 / 配置 / 注入 / @Transactional" }
  - { name: mybatis, path: mybatis/index.md, tag: folder, note: "Mapper / XML 设计 / 动态 SQL / 防注入 / 分页 / N+1" }
  - { name: mybatis-plus, path: mybatis-plus/index.md, tag: folder, note: "Wrapper / 分页插件 / 逻辑删除 / 乐观锁 / 自动填充 / 与 XML 共存" }
  - { name: mysql, path: mysql/index.md, tag: folder, note: "索引 / 事务与锁 / Schema 字段 / EXPLAIN 慢查询 / Online DDL 分库分表" }
  - { name: connection-pool, path: connection-pool/index.md, tag: folder, note: "HikariCP 参数 / Druid 监控 / 池大小与泄漏检测" }
  - { name: sharding-sphere, path: sharding-sphere/index.md, tag: folder, note: "分片策略 / 分片键 / 读写分离 / 广播绑定表 / 分布式限制" }
  - { name: mapstruct, path: mapstruct/index.md, tag: folder, note: "@Mapper 定义 / 字段映射 / 映射策略 / 反模式" }
  - { name: redis, path: redis/index.md, tag: folder, note: "RedisTemplate / Key 设计 / 缓存三问题 / 分布式锁 / @Cacheable" }
  - { name: redisson, path: redisson/index.md, tag: folder, note: "分布式锁(看门狗) / 锁 vs SETNX / 限流 / 延迟队列" }
  - { name: elasticsearch, path: elasticsearch/index.md, tag: folder, note: "Mapping / IK 分词 / DSL / 聚合 / 同步 MySQL / 深分页" }
  - { name: dubbo, path: dubbo/index.md, tag: folder, note: "@DubboService 暴露 / 引用配置 / API 模块 / 优雅降级" }
  - { name: spring-cloud, path: spring-cloud/index.md, tag: folder, note: "OpenFeign / 网关 / 配置中心 / 服务发现 / 熔断限流" }
  - { name: grpc, path: grpc/index.md, tag: folder, note: "Protobuf 定义 / 四种调用 / deadline / vs REST-Dubbo 选型" }
  - { name: webflux, path: webflux/index.md, tag: folder, note: "Mono/Flux / 何时响应式 / 阻塞陷阱 / 背压 / WebClient" }
  - { name: websocket, path: websocket/index.md, tag: folder, note: "Spring WebSocket / STOMP / 会话心跳 / 集群广播" }
  - { name: kafka, path: kafka/index.md, tag: folder, note: "生产者可靠投递 / 消费者手动 ack / 消费幂等 / 死信队列" }
  - { name: rocketmq, path: rocketmq/index.md, tag: folder, note: "发送方式 / 顺序-事务-延迟消息 / 消费模式 / 幂等去重" }
  - { name: spring-security, path: spring-security/index.md, tag: folder, note: "FilterChain / JWT 无状态 / 授权注解 / 密码加密 / OAuth2" }
  - { name: scheduling, path: scheduling/index.md, tag: folder, note: "@Scheduled / @Async / XXL-Job / Quartz 选型" }
  - { name: testing, path: testing/index.md, tag: folder, note: "JUnit5 / Mockito / @SpringBootTest / 测试金字塔" }
  - { name: api-doc, path: api-doc/index.md, tag: folder, note: "springdoc-openapi / Knife4j / 文档即契约" }
  - { name: seata, path: seata/index.md, tag: folder, note: "AT / TCC / Saga / @GlobalTransactional 选型" }
  - { name: observability, path: observability/index.md, tag: folder, note: "Micrometer / SkyWalking / 结构化日志 / 黄金指标" }
  - { name: file-storage, path: file-storage/index.md, tag: folder, note: "存储抽象 / 预签名 URL / 分片上传" }
  - { name: netty, path: netty/index.md, tag: folder, note: "Reactor 线程模型 / Pipeline / 粘包拆包 / 心跳" }
when_to_descend: |
  任务涉及具体框架的使用：写 React/antd 组件 / 写 FastAPI router / 操作 Tortoise ORM / 写 Spring Boot Controller / 写 MyBatis Mapper / 用 MapStruct 转换 / 操作 Redis / 调 MySQL 索引事务与慢查询 / Dubbo RPC / Spring Cloud 微服务 / Kafka 或 RocketMQ 消息。
---

# Framework · 框架使用约定

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| react | 文件夹 | 组件 / hook / state / 布局 / 性能 / 安全 / React19 |
| antd | 文件夹 | Form / Modal / Table / 组件选型 |
| vue | 文件夹 | Vue3 组合式 API / 响应式 / SFC / Pinia / Router（6 子项） |
| element-plus | 文件夹 | ElForm / ElTable / 主题配置 / 消息反馈（4 子项） |
| fastapi | 文件夹 | router / schema / middleware 3 类 |
| tortoise | 文件夹 | model 模板 / 事务 |
| gsap | 文件夹 | FLIP / Draggable |
| spring-boot | 文件夹 | Controller / 全局异常 / 校验 / 配置 / 注入 / 事务（6 子项） |
| mybatis | 文件夹 | Mapper / XML 设计 / 动态 SQL / 防注入 / 分页 / N+1（6 子项） |
| mybatis-plus | 文件夹 | Wrapper / 分页 / 逻辑删除 / 乐观锁 / 自动填充 / 与 XML 共存（6 子项） |
| mysql | 文件夹 | 索引 / 事务与锁 / Schema 字段 / EXPLAIN 慢查询 / Online DDL 分库分表（5 子目录 19 子项） |
| connection-pool | 文件夹 | HikariCP 参数 / Druid 监控 / 池大小与泄漏（3 子项） |
| sharding-sphere | 文件夹 | 分片策略 / 分片键 / 读写分离 / 广播绑定表 / 分布式限制（5 子项） |
| mapstruct | 文件夹 | Mapper 定义 / 字段映射 / 映射策略 / 反模式（4 子项） |
| redis | 文件夹 | RedisTemplate / Key 设计 / 缓存三问题 / 分布式锁 / 注解（5 子项） |
| redisson | 文件夹 | 分布式锁(看门狗) / 锁 vs SETNX / 限流 / 延迟队列（4 子项） |
| elasticsearch | 文件夹 | Mapping / IK 分词 / DSL / 聚合 / 同步 / 深分页（6 子项） |
| dubbo | 文件夹 | 服务暴露 / 引用配置 / API 模块 / 优雅降级（4 子项） |
| spring-cloud | 文件夹 | OpenFeign / 网关 / 配置中心 / 服务发现 / 熔断限流（5 子项） |
| grpc | 文件夹 | Protobuf / 四种调用 / deadline / vs REST-Dubbo（4 子项） |
| webflux | 文件夹 | Mono-Flux / 何时响应式 / 阻塞陷阱 / 背压 / WebClient（5 子项） |
| websocket | 文件夹 | Spring WebSocket / STOMP / 会话心跳 / 集群广播（4 子项） |
| kafka | 文件夹 | 生产可靠 / 消费 ack / 消费幂等 / 死信队列（4 子项） |
| rocketmq | 文件夹 | 发送方式 / 消息类型 / 消费模式 / 幂等去重（4 子项） |
| spring-security | 文件夹 | FilterChain / JWT / 授权注解 / 密码加密 / OAuth2（5 子项） |
| scheduling | 文件夹 | @Scheduled / @Async / XXL-Job / Quartz（4 子项） |
| testing | 文件夹 | JUnit5 / Mockito / @SpringBootTest / 测试金字塔（4 子项） |
| api-doc | 文件夹 | springdoc-openapi / Knife4j / 文档即契约（3 子项） |
| seata | 文件夹 | AT / TCC / Saga / 选型（4 子项） |
| observability | 文件夹 | Micrometer / SkyWalking / 结构化日志 / 黄金指标（4 子项） |
| file-storage | 文件夹 | 存储抽象 / 预签名 URL / 分片上传（3 子项） |
| netty | 文件夹 | Reactor 模型 / Pipeline / 粘包拆包 / 心跳（4 子项） |

## 何时下钻

- 新增 / 修改 `frontend/src/**/*.tsx` → `react/` + 视具体 UI 决定要不要进 `antd/`
- 新增 / 修改 `frontend/src/**/*.vue` → `vue/` + 视具体 UI 决定要不要进 `element-plus/`
- 新增 / 修改 `backend/routers/*.py` 或 `backend/schemas/*.py` → `fastapi/`
- 操作 ORM Model 或写 migration → `tortoise/`
- 写动画相关代码（`*.animations.ts` / `useGSAP` 等）→ `gsap/`

## 下钻决策表

| 任务 | 选哪个子项 |
|------|----------|
| D6 PresentationCard 卡片 | react/component + antd/table（如有）|
| H2 ContentTypeSelector | react/component + react/state |
| 写 referral 充值返现 API | fastapi/router + fastapi/schema |
| DB10 referral 三表迁移 | tortoise/model-class-pattern |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行维度：[`../lang/index.md`](../lang/index.md) · [`../design-pattern/index.md`](../design-pattern/index.md) · [`../habit/index.md`](../habit/index.md) · [`../tech-selection/index.md`](../tech-selection/index.md) · [`../ai/index.md`](../ai/index.md) · [`../fundamentals/index.md`](../fundamentals/index.md)
- antd MCP（写 antd 组件前查）：`antd_info` / `antd_demo` / `antd_token`
