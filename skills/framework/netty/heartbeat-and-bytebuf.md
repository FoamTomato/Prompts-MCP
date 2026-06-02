---
name: netty-heartbeat-and-bytebuf
description: Netty 连接保活与内存安全 — IdleStateHandler 检测读写空闲做心跳/关死连接，ByteBuf 引用计数 release/retain 配对防池化内存泄漏。Use when 做心跳保活 / 清理死连接 / 排查 ByteBuf 内存泄漏时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 心跳保活
  - IdleStateHandler
  - ByteBuf
  - 引用计数
  - 内存泄漏
effort: high
context: inline
version: '1.0'
---
# Netty · 心跳保活与 ByteBuf 引用计数

> 本条管「连接保活 + ByteBuf 不泄漏」两件强相关、同处一处释放逻辑的事。线程模型见 [`reactor-thread-model.md`](./reactor-thread-model.md)；Handler 链见 [`pipeline-handler.md`](./pipeline-handler.md)。

## 规则

| 项 | 约定 |
|----|------|
| 空闲检测 | 用 `IdleStateHandler` 检测读/写/全空闲，触发 `userEventTriggered` |
| 心跳策略 | 写空闲发心跳包；读空闲（多个周期收不到对端）判定死连接 → `ctx.close()` |
| 服务端阈值 | 读空闲阈值 > 客户端心跳间隔（如客户端 5s 发，服务端 15s 判死），留容错 |
| 引用计数 | `ByteBuf` 引用计数归 0 才回收；谁是**最后使用者**谁负责 `release` |
| 自动释放 | 业务用 `SimpleChannelInboundHandler`，框架读完自动 release，最省心 |
| retain | 把 ByteBuf 传给异步线程/缓存留用，必须先 `retain()`，用完再 release |
| 泄漏检测 | 开发期开 `-Dio.netty.leakDetection.level=PARANOID` 抓泄漏点 |

## 正例：心跳 + 安全释放

```java
// pipeline：读空闲 15s、写空闲 5s 触发事件
ch.pipeline()
  .addLast(new IdleStateHandler(15, 5, 0, TimeUnit.SECONDS))
  .addLast(new HeartbeatHandler());

public class HeartbeatHandler extends ChannelInboundHandlerAdapter {
    private int lostBeats = 0;
    @Override
    public void userEventTriggered(ChannelHandlerContext ctx, Object evt) {
        if (evt instanceof IdleStateEvent e) {
            if (e.state() == IdleState.WRITER_IDLE) {
                ctx.writeAndFlush(Heartbeat.PING);          // 写空闲发心跳
            } else if (e.state() == IdleState.READER_IDLE) {
                if (++lostBeats >= 3) ctx.close();          // 连续丢 → 判死关连接
            }
        }
    }
}
```

```java
// 引用计数：传给异步线程留用 → 先 retain，用完 release
ByteBuf buf = msg.content().retain();        // +1，防被框架提前回收
bizExecutor.execute(() -> {
    try { process(buf); }
    finally { buf.release(); }               // 用完 -1，配对
});
```

## 反例

```java
// ❌ 拿到 ByteBuf 处理完不 release：池化内存只增不还 → LEAK，最终 OOM
public void channelRead(ChannelHandlerContext ctx, Object msg) {
    process((ByteBuf) msg);                  // 缺 ReferenceCountUtil.release(msg)
}

// ❌ retain 后忘 release（或 release 两次）：计数不归 0 泄漏 / 提前回收后用到悬空
ByteBuf b = buf.retain();
asyncSend(b);                                // 异步里没人 release

// ❌ 只靠 TCP keepalive 不做应用层心跳：半开连接长期占着，资源不释放
```

## 自检

- [ ] 用 `IdleStateHandler` + `userEventTriggered` 做应用层心跳，不只靠 TCP keepalive？
- [ ] 服务端读空闲阈值 > 客户端心跳间隔，留了容错周期？
- [ ] 每个 ByteBuf 的 retain 与 release 配对，最后使用者负责 release？
- [ ] 业务尽量用 `SimpleChannelInboundHandler` 让框架自动释放？
- [ ] 开发/测试期开了 leakDetection（至少 ADVANCED）验证无泄漏？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`reactor-thread-model.md`](./reactor-thread-model.md)（心跳 Handler 在 EventLoop 上跑）
- 兄弟：[`pipeline-handler.md`](./pipeline-handler.md)（自动 release 的 SimpleChannelInboundHandler）
