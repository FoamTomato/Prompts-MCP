---
name: netty-pipeline-handler
description: Netty ChannelPipeline 处理器链 — Inbound/Outbound 顺序、解码→业务→编码分层、无状态 Handler 加 @Sharable。Use when 组装 pipeline / 写 ChannelHandler / 排查 Handler 顺序时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 处理器链
  - ChannelPipeline
  - ChannelHandler
  - Inbound Outbound
  - SimpleChannelInboundHandler
effort: high
context: inline
version: '1.0'
---
# Netty · ChannelPipeline 处理器链

> 本条只管「Handler 怎么排、职责怎么分」。线程模型见 [`reactor-thread-model.md`](./reactor-thread-model.md)；解码器选型见 [`frame-decoder.md`](./frame-decoder.md)。

## 规则

| 项 | 约定 |
|----|------|
| 链顺序 | 入站读：解码器 → 业务 Handler；出站写：编码器（Outbound 逆序执行） |
| 职责分层 | 一个 Handler 只干一件事：拆包 / 解码 / 业务 / 编码分开，禁一个 Handler 全包 |
| Inbound | `channelRead` 处理读，必须 `ctx.fireChannelRead(msg)` 或交给下一个，否则链断 |
| Outbound | `write` 处理写，沿链反向传递到 head 真正发出 |
| 业务基类 | 用 `SimpleChannelInboundHandler<T>`，它读完**自动 release** ByteBuf，免手动管引用 |
| 共享实例 | 无状态 Handler 加 `@Sharable` 可复用单实例；有状态的每连接 new（如解码器） |
| 异常 | 重写 `exceptionCaught` 统一处理，记日志 + `ctx.close()`，别让异常静默 |

## 正例：分层 pipeline + 自动释放的业务 Handler

```java
protected void initChannel(SocketChannel ch) {
    ch.pipeline()
      .addLast(new LengthFieldBasedFrameDecoder(1024, 0, 4, 0, 4)) // 1 拆包
      .addLast(new ProtoDecoder())     // 2 解码 byte->对象（Inbound）
      .addLast(new ProtoEncoder())     // 3 编码 对象->byte（Outbound）
      .addLast(new BizHandler());      // 4 业务
}

// 业务 Handler：SimpleChannelInboundHandler 读完自动 release 消息
public class BizHandler extends SimpleChannelInboundHandler<Request> {
    @Override
    protected void channelRead0(ChannelHandlerContext ctx, Request req) {
        Response resp = service.handle(req);
        ctx.writeAndFlush(resp);   // 触发 Outbound 编码器
    }
    @Override
    public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause) {
        log.error("channel error", cause);
        ctx.close();               // 统一兜底，避免异常静默
    }
}
```

## 反例

```java
// ❌ 一个 Handler 同时拆包+解码+业务：职责混乱，无法复用与排查
public class GodHandler extends ChannelInboundHandlerAdapter {
    public void channelRead(ChannelHandlerContext ctx, Object msg) {
        ByteBuf buf = (ByteBuf) msg;
        // 这里又拆包又解码又写业务又编码…… 几百行
    }
}

// ❌ 用 ChannelInboundHandlerAdapter 处理 ByteBuf 却不 release：内存泄漏
public void channelRead(ChannelHandlerContext ctx, Object msg) {
    process((ByteBuf) msg);   // 没 ReferenceCountUtil.release(msg)
}
```

## 自检

- [ ] 链顺序正确：入站解码器在前、业务在后，出站编码器逆序生效？
- [ ] 每个 Handler 只干一件事（拆包/解码/业务/编码分开）？
- [ ] 业务 Handler 用 `SimpleChannelInboundHandler` 自动 release，或手动 release 了？
- [ ] 无状态 Handler 才加 `@Sharable`，有状态的每连接 new？
- [ ] 重写了 `exceptionCaught` 统一处理 + close，没让异常静默？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`frame-decoder.md`](./frame-decoder.md)（拆包解码器放在链首）
- 兄弟：[`heartbeat-and-bytebuf.md`](./heartbeat-and-bytebuf.md)（ByteBuf release 与心跳 Handler 的位置）
