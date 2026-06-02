---
name: framework-netty-index
description: Netty 网络编程约定 — Reactor 线程模型/ChannelPipeline 处理器链/粘包拆包解码器/心跳与 ByteBuf 引用计数四个独立决策点。Use when 写 Netty 服务端 / 配 EventLoopGroup / 编解码 / 处理粘包或内存泄漏时。
parent: ../index.md
children:
  - { name: netty-reactor-thread-model, path: reactor-thread-model.md, tag: skill, note: boss/worker EventLoopGroup 主从 Reactor 模型 }
  - { name: netty-pipeline-handler, path: pipeline-handler.md, tag: skill, note: ChannelPipeline + Handler 链编解码与业务分离 }
  - { name: netty-frame-decoder, path: frame-decoder.md, tag: skill, note: 粘包拆包：长度字段/分隔符/定长解码器选型 }
  - { name: netty-heartbeat-and-bytebuf, path: heartbeat-and-bytebuf.md, tag: skill, note: IdleStateHandler 心跳 + ByteBuf 引用计数防泄漏 }
when_to_descend: 写 / 改 Java 里的 Netty 代码：配线程组、组装 pipeline、解决粘包拆包、做心跳或排查 ByteBuf 内存泄漏。
---

# Netty · 网络编程约定索引

四个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 配 boss/worker 线程组、决定业务逻辑放哪 | [reactor-thread-model](reactor-thread-model.md) |
| 组装 ChannelPipeline、写 Handler 链 | [pipeline-handler](pipeline-handler.md) |
| 解决 TCP 粘包/拆包、选解码器 | [frame-decoder](frame-decoder.md) |
| 做连接保活心跳 / 排查 ByteBuf 内存泄漏 | [heartbeat-and-bytebuf](heartbeat-and-bytebuf.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../redis/index.md`](../redis/index.md) · [`../file-storage/index.md`](../file-storage/index.md)
