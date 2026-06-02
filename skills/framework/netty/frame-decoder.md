---
name: netty-frame-decoder
description: Netty 粘包拆包解决 — TCP 是字节流无消息边界，按协议选 LengthFieldBasedFrameDecoder（长度字段）/ 分隔符 / 定长解码器，禁自己在业务里拼包。Use when 处理粘包拆包 / 选帧解码器 / 设计应用层协议时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 粘包拆包
  - LengthFieldBasedFrameDecoder
  - 分隔符解码
  - 定长解码
  - 半包
effort: high
context: inline
version: '1.0'
---
# Netty · 粘包拆包与帧解码器选型

> 本条只管「怎么切出完整一帧」。Handler 链顺序见 [`pipeline-handler.md`](./pipeline-handler.md)；ByteBuf 引用见 [`heartbeat-and-bytebuf.md`](./heartbeat-and-bytebuf.md)。

## 为什么

TCP 是**字节流**没有消息边界：发两条可能粘成一坨（粘包），一条可能被切两段（半包/拆包）。必须在解码器层切出完整帧，**禁止**在业务 Handler 里自己缓存拼包。

## 规则：按协议选解码器

| 协议形态 | 选哪个 | 说明 |
|---------|-------|------|
| 头部带长度字段（主流自定义协议） | `LengthFieldBasedFrameDecoder` | 最通用，读长度字段切帧 |
| 以特殊分隔符结尾（如 `\n`） | `LineBasedFrameDecoder` / `DelimiterBasedFrameDecoder` | 文本协议常用 |
| 每条消息固定长度 | `FixedLengthFrameDecoder` | 定长报文，简单 |
| 直接用现成协议 | `HttpServerCodec` / 自带 protobuf 解码器 | 别重复造轮子 |

## 正例：长度字段解码器（最常用）

```java
// 协议：[4字节长度][变长 body]
// 参数：maxFrameLength, lengthFieldOffset, lengthFieldLength,
//       lengthAdjustment, initialBytesToStrip
ch.pipeline().addLast(new LengthFieldBasedFrameDecoder(
        1024 * 1024, // 最大帧长，防超大包打爆内存
        0,           // 长度字段偏移：从第 0 字节开始
        4,           // 长度字段占 4 字节
        0,           // 长度调整：长度字段值即 body 长
        4));         // 剥掉前 4 字节长度头，下游只拿 body
// 编码端配套加 LengthFieldPrepender(4) 自动写长度头
ch.pipeline().addLast(new LengthFieldPrepender(4));
```

## 正例：分隔符 / 定长

```java
// 以换行分隔（文本协议）
ch.pipeline().addLast(new LineBasedFrameDecoder(8192));

// 自定义分隔符
ByteBuf delim = Unpooled.copiedBuffer("$$".getBytes());
ch.pipeline().addLast(new DelimiterBasedFrameDecoder(8192, delim));

// 定长报文
ch.pipeline().addLast(new FixedLengthFrameDecoder(128));
```

## 反例

```java
// ❌ 在业务 Handler 里自己 if 判断长度拼包：半包/粘包处理不全，必出 bug
protected void channelRead0(ChannelHandlerContext ctx, ByteBuf buf) {
    if (buf.readableBytes() >= expectLen) { ... }  // 漏处理半包累积
}

// ❌ LengthFieldBasedFrameDecoder 不设 maxFrameLength（或设极大）：
//    伪造超长长度字段 → 一次性分配巨量内存，OOM 攻击
new LengthFieldBasedFrameDecoder(Integer.MAX_VALUE, 0, 4, 0, 4);
```

## 自检

- [ ] 切帧交给现成 FrameDecoder，没在业务 Handler 里自己拼包？
- [ ] 按协议选对解码器（长度字段 / 分隔符 / 定长）？
- [ ] `LengthFieldBasedFrameDecoder` 设了合理 `maxFrameLength` 防超大包 OOM？
- [ ] 长度字段协议在编码端配了 `LengthFieldPrepender` 写头？
- [ ] 解码器是有状态的，每个连接 new 一个（没误加 `@Sharable`）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`pipeline-handler.md`](./pipeline-handler.md)（解码器放在 pipeline 链首）
- 兄弟：[`heartbeat-and-bytebuf.md`](./heartbeat-and-bytebuf.md)（解码出的 ByteBuf 谁来 release）
