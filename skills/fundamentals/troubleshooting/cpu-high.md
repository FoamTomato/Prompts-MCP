---
name: troubleshooting-cpu-high
description: CPU 飙高定位 — top -H -p 找占用最高的线程，把线程 id 转十六进制，在 jstack 输出里匹配 nid 找到 RUNNABLE 线程栈。Use when 线上 CPU 打满 / 某进程 CPU 占用异常高 / 要定位是哪段代码在烧 CPU 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - CPU 飙高
  - CPU 打满
  - top -H
  - jstack
  - 线程栈
  - RUNNABLE
effort: medium
context: inline
version: '1.0'
---
# 线上排查 · CPU 飙高定位

> 本条只管「CPU 占用高怎么定位到代码」。内存问题见 [`memory-leak.md`](./memory-leak.md)；想动态 watch/trace 见 [`arthas-online.md`](./arthas-online.md)；不确定先看 [`diagnosis-decision-tree.md`](./diagnosis-decision-tree.md)。

## 排查步骤（top → 线程 → jstack）

| 步骤 | 命令 | 拿到什么 |
|------|------|---------|
| 1. 找高 CPU 进程 | `top` | 进程 PID |
| 2. 找进程内高 CPU 线程 | `top -H -p <PID>` | 线程的十进制 TID |
| 3. TID 转十六进制 | `printf '%x\n' <TID>` | 小写 hex（jstack 的 nid） |
| 4. dump 线程栈 | `jstack <PID> > stack.txt` | 全部线程快照 |
| 5. 按 nid 匹配 | 在 stack.txt 搜 `nid=0x<hex>` | 该线程当前栈帧 |

关键：top -H 看到的是**线程**级 CPU；jstack 里每个线程头有 `nid=0x...`，把第 3 步的 hex 拿去匹配即可锁定代码位置。

## 正例

```bash
# 进程 PID=12345，发现线程 TID=12360 占 CPU 99%
printf '%x\n' 12360          # -> 3048
jstack 12345 | grep -A 30 'nid=0x3048'
```

```text
"pool-1-thread-3" #28 prio=5 nid=0x3048 runnable [0x...]
   java.lang.Thread.State: RUNNABLE
        at com.x.PriceCalc.loop(PriceCalc.java:88)   # 烧 CPU 的代码在这
```

锁定 **RUNNABLE** 且反复出现在栈顶的线程——通常是死循环 / 正则回溯 / 频繁 GC（GC 线程烧 CPU 时转去查内存，见 memory-leak）。

## 反例

```text
❌ CPU 高直接重启了事 —— 现场丢失，下次照样复发，根因永远找不到
❌ 只 top 看进程不 top -H 看线程 —— 定位不到具体线程，jstack 无从匹配
❌ 忘了 TID 转 hex，拿十进制去 jstack 里搜 —— 永远搜不到
```

## 自检

- [ ] 用 `top -H -p <PID>` 拿到的是**线程级** CPU，不是只看进程？
- [ ] 线程 TID 已用 `printf '%x'` 转成十六进制再去 jstack 匹配 `nid`？
- [ ] 锁定的是 `RUNNABLE` 且反复占栈顶的线程？
- [ ] 留存了 jstack 快照（重启前先 dump），没有直接重启丢现场？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`memory-leak.md`](./memory-leak.md)（GC 线程烧 CPU / 内存问题）
- 兄弟：[`arthas-online.md`](./arthas-online.md)（thread 命令更快定位忙线程）
- 兄弟：[`diagnosis-decision-tree.md`](./diagnosis-decision-tree.md)（按症状分流）
