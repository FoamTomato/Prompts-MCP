---
name: websocket-stomp-messaging
description: STOMP 子协议消息路由 — '@MessageMapping'/'@SendTo' 接收并广播、客户端订阅 topic、SimpMessagingTemplate 服务端主动推送给全体或指定用户。Use when 用 STOMP / 配消息代理 / 服务端主动推送时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - STOMP 子协议
  - 订阅广播
  - '@MessageMapping'
  - SimpMessagingTemplate
  - convertAndSendToUser
effort: medium
context: inline
version: '1.0'
---
# WebSocket · STOMP 子协议消息路由

> 本条只管「用 STOMP 做订阅/广播/主动推送」。裸 WebSocket 接入见 [`spring-websocket.md`](./spring-websocket.md)；多实例下推送跨节点见 [`cluster-broadcast.md`](./cluster-broadcast.md)。

## 规则

| 项 | 约定 |
|----|------|
| 启用 | 配 `@EnableWebSocketMessageBroker`，实现 `WebSocketMessageBrokerConfigurer` |
| 端点 | `registerStompEndpoints` 注册连接端点（可加 `.withSockJS()` 兜底降级） |
| 前缀 | `enableSimpleBroker("/topic","/queue")` 配广播前缀；`setApplicationDestinationPrefixes("/app")` 配入站前缀 |
| 接收 | `@MessageMapping("/x")` 收客户端发到 `/app/x` 的消息 |
| 广播 | 方法加 `@SendTo("/topic/x")`，返回值自动广播给订阅 `/topic/x` 的所有人 |
| 点对点 | `@SendToUser` 或 `convertAndSendToUser(user, "/queue/x", msg)`，按 Principal 路由到该用户 |
| 主动推送 | 非请求驱动的推送注入 `SimpMessagingTemplate.convertAndSend(...)` |
| 用户前缀 | 点对点目标客户端订阅 `/user/queue/x`，服务端写 `/queue/x` 即可 |

## 正例

```java
@Configuration
@EnableWebSocketMessageBroker
public class StompConfig implements WebSocketMessageBrokerConfigurer {
    @Override public void registerStompEndpoints(StompEndpointRegistry r) {
        r.addEndpoint("/ws").setAllowedOriginPatterns("https://app.example.com").withSockJS();
    }
    @Override public void configureMessageBroker(MessageBrokerRegistry r) {
        r.enableSimpleBroker("/topic", "/queue");          // 广播 / 点对点前缀
        r.setApplicationDestinationPrefixes("/app");        // 客户端发往 /app/**
        r.setUserDestinationPrefix("/user");                // 点对点用户前缀
    }
}

@Controller
@RequiredArgsConstructor
public class ChatController {
    // 收 /app/room.send → 广播给 /topic/room
    @MessageMapping("/room.send")
    @SendTo("/topic/room")
    public ChatMsg handle(ChatMsg in) {
        return in.withServerTime(Instant.now());
    }
}
```

```java
// 服务端主动推送（如订单状态变更，非客户端请求触发）
@Service
@RequiredArgsConstructor
public class PushService {
    private final SimpMessagingTemplate template;

    public void broadcastNotice(Notice n) {
        template.convertAndSend("/topic/notice", n);            // 广播全体
    }
    public void pushToUser(String userId, OrderEvent e) {
        template.convertAndSendToUser(userId, "/queue/order", e); // 点对点：客户端订阅 /user/queue/order
    }
}
```

## 反例

```java
// ❌ @MessageMapping 路径里带 /app 前缀：前缀由配置加，重复后路由不到
@MessageMapping("/app/room.send")   // 应写 "/room.send"

// ❌ 用 SimpMessageSendingOperations 给指定用户推却写死 /topic：所有人都收到，泄漏
template.convertAndSend("/topic/order-" + userId, e);  // 应 convertAndSendToUser
```

## 自检

- [ ] `@MessageMapping` 路径不含 `/app` 前缀（前缀由 `setApplicationDestinationPrefixes` 加）？
- [ ] 广播用 `/topic`、点对点用 `/queue` + `convertAndSendToUser`，没拿 topic 假装点对点？
- [ ] 非请求驱动的推送走 `SimpMessagingTemplate`，没在 Controller 里硬等？
- [ ] 端点 origin 用白名单、没开 `"*"`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`spring-websocket.md`](./spring-websocket.md)（不需要订阅语义时用裸 WebSocket）
- 兄弟：[`cluster-broadcast.md`](./cluster-broadcast.md)（多实例下 SimpleBroker 只在本节点广播，需跨节点）
