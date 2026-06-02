---
name: netty-reactor-thread-model
description: Netty 主从 Reactor 线程模型 — boss EventLoopGroup 只 accept，worker 处理 IO 读写，耗时业务必须丢业务线程池不能阻塞 EventLoop。Use when 配 EventLoopGroup / 设线程数 / 业务耗时阻塞 IO 线程时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - Reactor 线程模型
  - EventLoopGroup
  - boss worker
  - IO 线程阻塞
  - 业务线程池
effort: high
context: inline
version: '1.0'
---
# Netty · 主从 Reactor 线程模型

> 本条只管「线程组怎么配、业务放哪」。Handler 链怎么组见 [`pipeline-handler.md`](./pipeline-handler.md)；心跳见 [`heartbeat-and-bytebuf.md`](./heartbeat-and-bytebuf.md)。

## 规则

| 项 | 约定 |
|----|------|
| boss 组 | 只负责 `accept` 新连接，线程数 1 即可（单端口监听） |
| worker 组 | 负责已建连接的 IO 读写，默认线程数 = CPU 核数 × 2 |
| 铁律 | EventLoop 线程**绝不能**执行耗时操作（DB/RPC/锁/大计算），否则阻塞该线程上所有连接 |
| 耗时业务 | 丢自定义业务线程池（`DefaultEventExecutorGroup` 或普通线程池），IO 线程立即返回 |
| 单线程归属 | 一个 Channel 全生命周期固定绑一个 EventLoop，Handler 内无需加锁（无并发） |
| 优雅关闭 | `shutdownGracefully()` 关两个组，不要 `System.exit` 硬关 |

## 正例：主从 Reactor 启动 + 业务丢线程池

```java
EventLoopGroup boss = new NioEventLoopGroup(1);          // 只 accept
EventLoopGroup worker = new NioEventLoopGroup();         // 默认 核数×2，处理 IO
EventExecutorGroup biz = new DefaultEventExecutorGroup(16); // 业务线程池
try {
    ServerBootstrap b = new ServerBootstrap();
    b.group(boss, worker).channel(NioServerSocketChannel.class)
     .childHandler(new ChannelInitializer<SocketChannel>() {
        protected void initChannel(SocketChannel ch) {
            ch.pipeline()
              .addLast(new MyDecoder())
              // 耗时业务 Handler 绑到业务线程池，不占 worker
              .addLast(biz, new BizHandler());
        }
     });
    b.bind(8080).sync().channel().closeFuture().sync();
} finally {
    boss.shutdownGracefully();
    worker.shutdownGracefully();
}
```

## 反例

```java
// ❌ 在 worker(IO) 线程里直接做耗时操作：阻塞该 EventLoop 上所有连接
protected void channelRead0(ChannelHandlerContext ctx, Msg msg) {
    Order o = orderMapper.selectById(msg.getId());  // 同步 DB，阻塞 IO 线程
    Thread.sleep(2000);                               // 更致命
    ctx.writeAndFlush(o);
}

// ❌ boss 组配几十个线程：accept 用不上，纯浪费
EventLoopGroup boss = new NioEventLoopGroup(32);
```

## 自检

- [ ] boss 组线程数为 1（单端口），worker 用默认（核数×2）？
- [ ] EventLoop 线程内没有任何 DB/RPC/sleep/重计算等阻塞操作？
- [ ] 耗时业务 Handler 绑到了独立业务线程池（addLast 传 EventExecutorGroup）？
- [ ] 关闭用 `shutdownGracefully()` 关两个组？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`pipeline-handler.md`](./pipeline-handler.md)（Handler 绑哪个线程池在 pipeline 里指定）
- 兄弟：[`heartbeat-and-bytebuf.md`](./heartbeat-and-bytebuf.md)（心跳 Handler 同样在 EventLoop 上跑）
