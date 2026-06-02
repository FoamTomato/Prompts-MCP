---
name: websocket-spring-websocket
description: Spring WebSocket 接入选型 — JSR-356 '@ServerEndpoint' vs Spring 原生 WebSocketHandler/握手拦截器/WebSocketSession 会话操作。Use when 接入 WebSocket / 选端点写法 / 写握手拦截器时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 握手拦截器
  - WebSocket 端点
  - '@ServerEndpoint'
  - WebSocketHandler
  - HandshakeInterceptor
effort: medium
context: inline
version: '1.0'
---
# Spring WebSocket · 端点选型与握手

> 本条只管「裸 WebSocket 怎么接入、握手怎么拦」。子协议消息路由见 [`stomp-messaging.md`](./stomp-messaging.md)；session 与用户映射见 [`session-and-heartbeat.md`](./session-and-heartbeat.md)。

## 规则

| 项 | 约定 |
|----|------|
| 端点选型 | Spring 项目优先 `WebSocketHandler`（接入 Spring 生命周期/拦截器/容器）；`@ServerEndpoint` 仅在脱离 Spring 的纯 JSR-356 容器下用 |
| 注册方式 | 实现 `WebSocketConfigurer`，在 `registerWebSocketHandlers` 注册 handler + 路径 + 拦截器 |
| 处理器基类 | 文本消息继承 `TextWebSocketHandler`，二进制继承 `BinaryWebSocketHandler`，别直接裸实现接口 |
| 握手鉴权 | 用 `HandshakeInterceptor.beforeHandshake` 校验 token，把 userId 放进 `attributes`（后续 session 可取） |
| 跨域 | `setAllowedOrigins` 显式列白名单，**禁止** `"*"` 上生产 |
| @ServerEndpoint 注入 | `@ServerEndpoint` 默认非 Spring Bean，注入 Service 需 `SpringConfigurator` 或静态持有 |

## 正例

```java
@Configuration
@EnableWebSocket
@RequiredArgsConstructor
public class WsConfig implements WebSocketConfigurer {
    private final ChatHandler chatHandler;
    private final AuthHandshakeInterceptor authInterceptor;

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(chatHandler, "/ws/chat")
                .addInterceptors(authInterceptor)
                .setAllowedOrigins("https://app.example.com");  // 不写 "*"
    }
}

@Component
public class ChatHandler extends TextWebSocketHandler {
    @Override
    public void afterConnectionEstablished(WebSocketSession session) {
        Object uid = session.getAttributes().get("userId");   // 握手时塞入
        // 注册到用户↔session 映射，见 session-and-heartbeat
    }
    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage msg) throws Exception {
        session.sendMessage(new TextMessage("echo:" + msg.getPayload()));
    }
}
```

```java
// 握手拦截器：鉴权 + 把用户身份带进 session.attributes
@Component
public class AuthHandshakeInterceptor implements HandshakeInterceptor {
    @Override
    public boolean beforeHandshake(ServerHttpRequest req, ServerHttpResponse resp,
                                   WebSocketHandler h, Map<String, Object> attributes) {
        String token = UriComponentsBuilder.fromUri(req.getURI()).build()
                .getQueryParams().getFirst("token");
        Long uid = tokenService.parse(token);  // 失败返回 false → 拒绝握手
        if (uid == null) { resp.setStatusCode(HttpStatus.UNAUTHORIZED); return false; }
        attributes.put("userId", uid);
        return true;
    }
    @Override public void afterHandshake(ServerHttpRequest r, ServerHttpResponse s,
                                         WebSocketHandler h, Exception e) {}
}
```

## 反例

```java
// ❌ setAllowedOrigins("*")：任意站点可发起跨域 WS 连接，CSRF 风险
registry.addHandler(handler, "/ws").setAllowedOrigins("*");

// ❌ 把鉴权放进 handleTextMessage：连接已建立才验，资源已占且可绕过
@Override protected void handleTextMessage(WebSocketSession s, TextMessage m) {
    if (!auth(m.getPayload())) s.close();   // 鉴权应在握手期做
}
```

## 自检

- [ ] Spring 项目用 `WebSocketHandler` 体系而非 `@ServerEndpoint`？
- [ ] 鉴权在 `HandshakeInterceptor.beforeHandshake` 完成、失败即拒握手？
- [ ] 用户身份握手时放进 `attributes`，而非连接后再传？
- [ ] `setAllowedOrigins` 列了白名单、没用 `"*"`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`stomp-messaging.md`](./stomp-messaging.md)（要消息路由/广播时改用 STOMP）
- 兄弟：[`session-and-heartbeat.md`](./session-and-heartbeat.md)（连上后的 session 管理）
