---
name: websocket-session-and-heartbeat
description: WebSocket 会话管理 — 用户↔WebSocketSession 映射用并发容器、心跳保活、读空闲断线检测清理、单用户连接数上限。Use when 维护在线会话 / 做心跳保活 / 检测断线 / 限连接数时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 会话管理
  - 心跳保活
  - 断线检测
  - WebSocketSession
  - 连接数限制
effort: high
context: inline
version: '1.0'
---
# WebSocket · 会话管理与心跳保活

> 本条只管「连上之后：session 怎么存、怎么保活、怎么清死连接、怎么限连」。接入握手见 [`spring-websocket.md`](./spring-websocket.md)；多节点广播见 [`cluster-broadcast.md`](./cluster-broadcast.md)。

## 规则

| 项 | 约定 |
|----|------|
| 映射容器 | 用户→session 用 `ConcurrentHashMap`；一个用户可多端，value 用 `Set`（`ConcurrentHashMap.newKeySet`） |
| 注册时机 | `afterConnectionEstablished` 注册，`afterConnectionClosed` 必须移除（否则内存泄漏） |
| 发消息加锁 | `WebSocketSession.sendMessage` **非线程安全**，并发写须 synchronized 或用 `ConcurrentWebSocketSessionDecorator` |
| 心跳 | 应用层 ping/pong：客户端定时发 ping，服务端回 pong；不能只靠 TCP keepalive |
| 断线检测 | 记录 `lastPongTime`，定时任务扫描超时（如 > 2 个心跳周期）→ `session.close()` 并移除 |
| 连接数限制 | 注册前查该用户当前连接数，超上限拒绝或踢最早一条 |
| STOMP 心跳 | 用 STOMP 时优先 `setHeartbeatValue` 由框架管心跳，不自己造轮子 |

## 正例

```java
@Component
public class SessionRegistry {
    // userId -> 多端 session 集合（并发安全）
    private final Map<Long, Set<WebSocketSession>> map = new ConcurrentHashMap<>();
    private static final int MAX_PER_USER = 3;

    public boolean register(Long uid, WebSocketSession s) {
        Set<WebSocketSession> set = map.computeIfAbsent(uid, k -> ConcurrentHashMap.newKeySet());
        if (set.size() >= MAX_PER_USER) return false;   // 连接数上限：拒绝
        set.add(s);
        return true;
    }
    public void remove(Long uid, WebSocketSession s) {
        Optional.ofNullable(map.get(uid)).ifPresent(set -> {
            set.remove(s);
            if (set.isEmpty()) map.remove(uid);          // 空集清理，防泄漏
        });
    }
}
```

```java
// 断线检测：定时扫 lastPong 超时的连接并清理
@Scheduled(fixedDelay = 30_000)
public void evictDead() {
    long now = System.currentTimeMillis();
    registry.all().stream()
        .filter(s -> now - lastPong(s) > 60_000)  // 超 2 个周期未收到 pong
        .forEach(s -> { try { s.close(CloseStatus.SESSION_NOT_RELIABLE); }
                        catch (IOException ignored) {} });
}

// 并发写：包一层装饰器，sendMessage 自动串行
WebSocketSession safe = new ConcurrentWebSocketSessionDecorator(raw, 5000, 64 * 1024);
```

## 反例

```java
// ❌ afterConnectionClosed 不移除映射：死连接长期驻留，内存泄漏 + 推送写废连接
@Override public void afterConnectionClosed(WebSocketSession s, CloseStatus st) {
    // 忘了 registry.remove(...)
}

// ❌ 多线程直接对同一 session.sendMessage：交错写导致帧损坏 / IllegalStateException
executor.execute(() -> session.sendMessage(a));
executor.execute(() -> session.sendMessage(b));   // 未串行化
```

## 自检

- [ ] 用户↔session 用并发容器，且 `afterConnectionClosed` 必移除？
- [ ] 并发写同一 session 用了锁或 `ConcurrentWebSocketSessionDecorator`？
- [ ] 有应用层心跳（ping/pong）而非只靠 TCP keepalive？
- [ ] 有定时断线检测，按 `lastPong` 超时清死连接？
- [ ] 单用户连接数有上限，超限拒绝或踢旧？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`spring-websocket.md`](./spring-websocket.md)（注册时机在 handler 生命周期回调里）
- 兄弟：[`cluster-broadcast.md`](./cluster-broadcast.md)（多节点时本地 map 只存本节点 session）
