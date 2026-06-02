---
name: jvm-oom-troubleshooting
description: 线上 OutOfMemoryError 排查决策树 — 按 OOM 类型分流：堆→jmap+MAT、元空间→类加载泄漏、栈→递归/线程数、直接内存→Netty/NIO。Use when 排查 OOM / 分析堆 dump / 定位内存泄漏时。
parent: ./index.md
paths:
- '*.java'
- '*.yml'
triggers:
  keywords:
  - OOM 排查
  - OutOfMemoryError
  - 内存泄漏
  - jmap
  - MAT
  - 堆 dump
effort: high
context: inline
version: '1.0'
---
# JVM · OOM 排查决策树

> 本条只管「OOM 了怎么定位」。排查的前提是已加 `-XX:+HeapDumpOnOutOfMemoryError`（见 [`heap-params.md`](./heap-params.md)）。GC 频繁但未 OOM 见 [`gc-selection.md`](./gc-selection.md)；元空间泄漏的根因分析见 [`class-loading.md`](./class-loading.md)。

## 第一步：看报错后半句，分流到对应分支

`OutOfMemoryError` 后面那句话直接指明类型，别盲查：

| 报错关键字 | 是哪种 OOM | 查什么 |
|-----------|-----------|--------|
| `Java heap space` | 堆 OOM | 堆里谁占着不放 |
| `Metaspace` | 元空间 OOM | 类加载泄漏 |
| `unable to create new native thread` | 线程/栈 | 线程数爆 / 栈太深 |
| `Direct buffer memory` | 直接内存 | 堆外 ByteBuffer 没释放 |
| `GC overhead limit exceeded` | 堆濒满 | 当堆 OOM 查 |

## 各分支怎么查

```text
堆 OOM (Java heap space)
  → 拿 OOM 自动 dump（或 jmap -dump:live,format=b,file=h.hprof <pid>）
  → 用 MAT 打开，看 Leak Suspects / 支配树（Dominator Tree）找最大对象
  → 常见根因：大集合/缓存无上限、ThreadLocal 未 remove、监听器未注销

元空间 OOM (Metaspace)
  → 看类加载数：jstat -class <pid>，类数只增不降 = 类加载泄漏
  → 常见根因：CGLIB/动态代理反复生成类、热部署反复加载、ClassLoader 泄漏
  → 根因机制见 class-loading.md

线程/栈 (unable to create new native thread)
  → 先 jstack <pid> 数线程数：是不是线程池没设上限/没复用
  → 真栈溢出(StackOverflowError)：查递归无出口；深递归可调 -Xss

直接内存 (Direct buffer memory)
  → Netty/NIO 的 DirectByteBuffer 未释放：查 ByteBuf 引用计数(leak)
  → -XX:MaxDirectMemorySize 限制堆外，配合 Netty leak detector 定位
```

## 反例

```text
❌ 一看到 OOM 就无脑 jmap dump：元空间/直接内存 OOM 在堆 dump 里根本看不出根因
❌ 直接内存 OOM 去加 -Xmx：堆外内存和 -Xmx 无关，越加越快被 OOMKilled
❌ 重启了事不留 dump：偶发 OOM 下次还来，且现场永久丢失
```

## 自检

- [ ] 先读了 `OutOfMemoryError` 后半句、确认是哪种 OOM 再动手？
- [ ] 堆 OOM 用 MAT 看了支配树/Leak Suspects，而非凭猜？
- [ ] 元空间 OOM 用 `jstat -class` 确认了类数只增不降？
- [ ] 直接内存 OOM 没去调 `-Xmx`，而是查堆外释放？
- [ ] 重启前保留了 dump / jstack 现场？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`heap-params.md`](./heap-params.md)（提前配好 dump 参数）
- 兄弟：[`class-loading.md`](./class-loading.md)（元空间泄漏的类加载根因）
- 跨模块：[`../troubleshooting/memory-leak.md`](../troubleshooting/memory-leak.md)（堆 OOM 分支：MAT 支配树沿 GC Roots 找住对象的根因）
