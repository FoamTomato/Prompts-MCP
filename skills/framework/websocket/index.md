---
name: framework-websocket-index
description: WebSocket（Java/Spring 视角）使用约定 — 端点接入/STOMP 消息/会话与心跳/集群广播四个独立决策点。Use when 接入 WebSocket / 用 STOMP 推送 / 管在线会话与心跳 / 多实例广播时。
parent: ../index.md
children:
  - { name: websocket-spring-websocket, path: spring-websocket.md, tag: skill, note: "@ServerEndpoint vs WebSocketHandler + 握手拦截鉴权" }
  - { name: websocket-stomp-messaging, path: stomp-messaging.md, tag: skill, note: "@MessageMapping/@SendTo 订阅广播 + SimpMessagingTemplate 主动推" }
  - { name: websocket-session-and-heartbeat, path: session-and-heartbeat.md, tag: skill, note: 用户↔session 映射+心跳保活+断线检测+连接数限制 }
  - { name: websocket-cluster-broadcast, path: cluster-broadcast.md, tag: skill, note: 多实例下 Redis pub/sub 或 MQ 扇出到所有节点 }
when_to_descend: 写 / 改 Java 里的 WebSocket 代码：接入端点、用 STOMP 推送、管在线会话与心跳，或做多实例集群广播。
---

# WebSocket · 框架使用约定索引

四个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 接入 WebSocket、选端点写法、写握手鉴权拦截器 | [spring-websocket](spring-websocket.md) |
| 用 STOMP 做订阅/广播、服务端主动推送 | [stomp-messaging](stomp-messaging.md) |
| 维护在线 session、做心跳保活/断线检测/限连 | [session-and-heartbeat](session-and-heartbeat.md) |
| 多实例部署、推送只有部分用户收到、跨节点广播 | [cluster-broadcast](cluster-broadcast.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../netty/index.md`](../netty/index.md)
- 相关：[`../redis/index.md`](../redis/index.md)
