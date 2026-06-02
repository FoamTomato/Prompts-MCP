---
name: troubleshooting-arthas-online
description: Arthas 免重启在线诊断 — watch 看方法入参/返回/异常，trace 按调用链拆方法耗时定位慢点，profiler 出火焰图找热点，全程不停服不改代码。Use when 线上不能重启又要看方法入参出参 / 定位方法内部耗时 / 抓 CPU 热点火焰图时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - Arthas
  - 在线诊断
  - watch
  - trace
  - 火焰图
  - 免重启
effort: medium
context: inline
version: '1.0'
---
# 线上排查 · Arthas 在线诊断

> 本条只管「不重启、不加日志，动态看运行时行为」。CPU 飙高的 top+jstack 流程见 [`cpu-high.md`](./cpu-high.md)；内存 dump 见 [`memory-leak.md`](./memory-leak.md)；不确定先看 [`diagnosis-decision-tree.md`](./diagnosis-decision-tree.md)。

## 价值：补上静态工具的盲区

jstack/jmap 是**快照**，看不到"某次调用的入参是什么""慢在哪个子方法"。Arthas attach 到运行进程，**免重启、免改代码**动态观测。

## 命令速查

| 你要看什么 | 命令 | 说明 |
|-----------|------|------|
| 某方法的入参/返回/异常 | `watch 类 方法 '{params,returnObj,throwExp}' -x 2` | 线上少日志时神器 |
| 方法内部哪步慢 | `trace 类 方法 '#cost > 50'` | 按调用链拆耗时，过滤 >50ms |
| 谁调用了这个方法 | `stack 类 方法` | 反向调用栈 |
| CPU 热点 | `profiler start` → `profiler stop --format html` | 输出火焰图 |
| 哪个线程忙/死锁 | `thread -n 3` / `thread -b` | top 线程 / 检测死锁 |

`watch`/`trace` 靠**字节码增强**实现：诊断完务必关掉或 `stop`，避免增强残留影响性能。

## 正例

```bash
# 线上某接口偶发返回 null，又没打入参日志——直接 watch
watch com.x.OrderService createOrder '{params,returnObj}' -x 3

# 接口 P99 高，trace 出耗时大头（只看超过 50ms 的调用）
trace com.x.OrderService createOrder '#cost > 50'

# 抓 CPU 热点，生成火焰图给团队看
profiler start; sleep 30; profiler stop --format html
```

## 反例

```text
❌ 为查一个偶发问题改代码加日志 → 重新发版 → 等复现：Arthas watch 一行搞定，无需发版
❌ trace 不加 '#cost > Nms' 过滤：海量正常调用刷屏，淹没慢点
❌ 诊断完不 stop / 不 shutdown：字节码增强 + watch 表达式持续开销留在生产
❌ 生产无差别 profiler 长时间跑：本身有采样开销，限定时长（如 30s）
```

## 自检

- [ ] 是「不能重启又要看运行时入参/耗时」才用 Arthas（快照需求用 jstack/jmap）？
- [ ] `trace`/`watch` 加了 `#cost`/条件过滤，没刷屏？
- [ ] 诊断结束 `stop` profiler 并 `shutdown`/`stop` Arthas，没留增强残留？
- [ ] profiler 限定了采样时长，没在生产长时间裸跑？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`cpu-high.md`](./cpu-high.md)（jstack 快照版定位）
- 兄弟：[`memory-leak.md`](./memory-leak.md)（堆 dump 分析）
- 兄弟：[`diagnosis-decision-tree.md`](./diagnosis-decision-tree.md)（按症状选手段）
