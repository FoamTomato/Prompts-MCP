---
name: troubleshooting-memory-leak
description: 内存泄漏/OOM 定位 — jmap dump 堆快照，用 MAT 看支配树和最大对象，沿 GC Roots 引用链找住对象不放的根因。Use when 内存持续上涨 / 抛 OutOfMemoryError / 分析堆 dump 找泄漏对象时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 内存泄漏
  - OOM
  - jmap
  - 堆 dump
  - MAT
  - 支配树
effort: high
context: inline
version: '1.0'
---
# 线上排查 · 内存泄漏 / OOM 定位

> 本条只管「内存涨/OOM 怎么找泄漏对象」。CPU 高见 [`cpu-high.md`](./cpu-high.md)；OOM 的**类型分流**（堆/元空间/栈/直接内存）见 [`../jvm/oom-troubleshooting.md`](../jvm/oom-troubleshooting.md)；不确定先看 [`diagnosis-decision-tree.md`](./diagnosis-decision-tree.md)。

## 排查步骤（dump → MAT → 引用链）

| 步骤 | 手段 | 拿到什么 |
|------|------|---------|
| 1. 拿堆快照 | `jmap -dump:live,format=b,file=heap.hprof <PID>` | hprof 文件 |
| 1'. OOM 自动落盘 | 启动加 `-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=...` | 崩溃现场 dump |
| 2. 看谁占最多 | MAT → **Histogram / Dominator Tree（支配树）** | 最大对象/类 |
| 3. 找为何不回收 | 选中大对象 → **Path to GC Roots（exclude weak/soft）** | 谁在强引用它 |
| 4. 看泄漏嫌疑 | MAT → **Leak Suspects** 报告 | 自动给出嫌疑点 |

核心思路：**支配树**告诉你"哪个对象撑大了堆"，**Path to GC Roots** 告诉你"它为什么没被回收"——两者结合才是根因。

## 正例

```bash
# live 只 dump 存活对象，会先触发一次 Full GC（生产慎用，会停顿）
jmap -dump:live,format=b,file=/tmp/heap.hprof 12345
```

```text
MAT Dominator Tree 典型泄漏画像：
  HashMap                 1.2 GB   <- 一个 Map 占了大半个堆
   └ 持续 put 不 remove 的本地缓存
  Path to GC Roots: static CacheHolder.MAP  <- 静态字段强引用，永不回收
```

常见根因：无界本地缓存 / static 集合只增不减 / ThreadLocal 未 remove / 监听器未注销。

## 反例

```text
❌ 内存涨就调大 -Xmx 了事 —— 泄漏没解决，只是更晚 OOM，且 dump 更大更难分析
❌ 不加 -XX:+HeapDumpOnOutOfMemoryError —— OOM 崩了没现场，只能干等复现
❌ 生产高峰直接 jmap -dump:live —— live 触发 Full GC + STW，可能压垮服务（低峰或备机做）
❌ 只看 Histogram 不看 Path to GC Roots —— 知道谁大却不知道谁在引用，改不对
```

## 自检

- [ ] 启动参数加了 `-XX:+HeapDumpOnOutOfMemoryError`（OOM 自动留现场）？
- [ ] 用 MAT **支配树**找最大对象，而不是只看类直方图？
- [ ] 对大对象查了 **Path to GC Roots** 找到强引用源？
- [ ] 没有用「调大堆」掩盖泄漏？没在生产高峰用 `-dump:live` 触发 STW？

## 相关

- 父：[`./index.md`](./index.md)
- OOM 类型分流（堆/元空间/栈/直接内存先分哪种）：[`../jvm/oom-troubleshooting.md`](../jvm/oom-troubleshooting.md)
- 兄弟：[`cpu-high.md`](./cpu-high.md)（频繁 GC 也会烧 CPU）
- 兄弟：[`diagnosis-decision-tree.md`](./diagnosis-decision-tree.md)
