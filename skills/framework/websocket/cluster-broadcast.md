---
name: websocket-cluster-broadcast
description: WebSocket 集群广播 — 多实例下本地 session 只在本节点，需用 Redis pub/sub 或 MQ 把消息扇出到所有节点，各节点再推给本地 session。Use when 多实例部署 WebSocket / 推送只有部分用户收到 / 跨节点广播时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 集群广播
  - 多实例推送
  - Redis pub/sub
  - 跨节点
  - 消息扇出
effort: high
context: inline
version: '1.0'
---
# WebSocket · 集群多实例广播

> 本条只管「多节点下消息怎么扇出到所有实例」。单机 session 管理见 [`session-and-heartbeat.md`](./session-and-heartbeat.md)；STOMP 推送 API 见 [`stomp-messaging.md`](./stomp-messaging.md)；Redis 用法见 [`../redis/index.md`](../redis/index.md)。

## 问题与方案

| 项 | 约定 |
|----|------|
| 根因 | 用户 A 连节点 1、用户 B 连节点 2；节点 1 的本地 session map 不含 B → 直接推丢消息 |
| 思路 | 业务推送先发到**广播通道**（Redis pub/sub 或 MQ），每个节点订阅，收到后只推给**本节点**持有的 session |
| Redis 方案 | 轻量：`convertAndSend(channel, msg)` 发布，`MessageListener` 订阅；至多一次、无持久化、节点重启期间消息丢 |
| MQ 方案 | 可靠/可回溯：广播型消费（每节点一个独立消费组），适合不可丢的通知 |
| STOMP 升级 | 用 STOMP 时直接换 `enableStompBrokerRelay` 接外部 broker（RabbitMQ/ActiveMQ），由 broker 统一扇出，免自造 |
| 幂等 | 节点收到广播只查本地 map 推送，对不在本节点的用户**静默跳过**，不再转发，防回环 |
| 序列化 | 广播体带 targetUserId/topic + payload，各节点据此本地路由 |

## 正例（Redis pub/sub）

```java
// 发布端：业务推送不再直接写 session，而是发到 Redis 频道
@Service
@RequiredArgsConstructor
public class ClusterPublisher {
    private final StringRedisTemplate redis;
    private final ObjectMapper mapper;

    @SneakyThrows
    public void broadcast(WsMessage msg) {          // msg 含 targetUserId + payload
        redis.convertAndSend("ws:broadcast", mapper.writeValueAsString(msg));
    }
}

// 订阅端：每个节点都订，收到后只推本地 session
@Component
@RequiredArgsConstructor
public class ClusterSubscriber implements MessageListener {
    private final SessionRegistry registry;   // 本节点的用户↔session 映射
    private final ObjectMapper mapper;

    @Override @SneakyThrows
    public void onMessage(Message message, byte[] pattern) {
        WsMessage msg = mapper.readValue(message.getBody(), WsMessage.class);
        registry.localSessions(msg.getTargetUserId())   // 不在本节点 → 空集，静默跳过
                .forEach(s -> sendSafely(s, msg.getPayload()));
    }
}

@Bean
RedisMessageListenerContainer container(RedisConnectionFactory f, ClusterSubscriber sub) {
    var c = new RedisMessageListenerContainer();
    c.setConnectionFactory(f);
    c.addMessageListener(sub, new ChannelTopic("ws:broadcast"));
    return c;
}
```

## 反例

```java
// ❌ 多实例下仍直接推本地 map：只有连到本节点的用户能收到，其余全丢
public void push(Long uid, Object p) {
    registry.localSessions(uid).forEach(s -> send(s, p));  // 跨节点用户收不到
}

// ❌ 节点收到广播后又转发回 Redis：消息回环，雪崩式放大
@Override public void onMessage(Message m, byte[] p) {
    redis.convertAndSend("ws:broadcast", m.getBody());     // 死循环
}
```

## 自检

- [ ] 多实例部署时，业务推送先经广播通道（Redis pub/sub 或 MQ）再落本地？
- [ ] 各节点订阅后只推**本节点** session，对不在本节点的用户静默跳过？
- [ ] 节点收到广播后没有再转发回通道（无回环）？
- [ ] 不可丢的通知选 MQ 广播消费，可丢的实时态可选 Redis pub/sub？
- [ ] 用 STOMP 的话评估过直接接外部 broker relay 替自造扇出？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`session-and-heartbeat.md`](./session-and-heartbeat.md)（本地 session map 是扇出的落点）
- 兄弟：[`stomp-messaging.md`](./stomp-messaging.md)（SimpleBroker 仅本节点，需替换为 relay 或自扇出）
- 跨模块：[`../redis/index.md`](../redis/index.md)（pub/sub 用的 Redis 连接与序列化约定）
