---
name: troubleshooting-diagnosis-decision-tree
description: 线上排查总决策树 — 先按症状分流：CPU 高走 top+jstack，内存涨/OOM 走 jmap+MAT，接口变慢走 Arthas trace + GC 日志，偶发抖动走链路追踪。Use when 拿到一个线上故障不知从何下手 / 要先选对排查手段再深入时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 排查决策树
  - 线上排查
  - troubleshooting
  - 故障定位
  - 接口变慢
  - 偶发
  - 链路追踪
effort: medium
context: inline
version: '1.0'
---
# 线上排查 · 总决策树（先分流再深入）

> 本条是**入口分流**：先按症状选手段，再下钻到对应兄弟叶子的具体步骤。别一上来就乱试工具。

## 按症状分流

| 症状 | 先用 | 下钻 |
|------|------|------|
| CPU 占用打满 | `top -H` 找忙线程 → `jstack` 看栈 | [`cpu-high.md`](./cpu-high.md) |
| 内存持续涨 / 抛 OOM | `jmap` dump → MAT 支配树 | [`memory-leak.md`](./memory-leak.md) |
| 接口/方法变慢（非整体卡） | Arthas `trace` 拆方法耗时 + 看 GC 日志排除停顿 | [`arthas-online.md`](./arthas-online.md) |
| 偶发抖动 / 跨服务慢 | 链路追踪（traceId 贯穿）看是哪一跳 | 见「相关」可观测模块 |
| 整体卡顿 / 周期性停顿 | 先看 **GC 日志**（jstat / GC log）排除 GC | [`../jvm/gc-selection.md`](../jvm/gc-selection.md) |

## 分流原则

```text
1. 先定性是哪一维：CPU / 内存 / 慢 / 偶发 —— 别拿内存工具查 CPU 问题。
2. 变慢先分「整体 vs 单点」：整体周期停顿优先怀疑 GC；单接口慢用 trace 拆。
3. 偶发问题靠链路追踪定位「哪一跳」，再到那台机用上面手段深挖。
4. 任何排查：先留现场（jstack/jmap/日志）再动手，禁直接重启丢现场。
```

## 反例

```text
❌ 不分症状直接重启：可能临时好转，根因没找到必复发，且现场全丢
❌ CPU 问题去翻堆 dump、内存问题去看线程栈：手段和症状错配，白忙
❌ 接口慢不先看 GC 日志，直接归咎业务代码：周期性停顿往往是 Full GC
❌ 偶发问题在单机狂 dump：无链路追踪定位不到是哪台/哪一跳，碰运气
```

## 自检

- [ ] 先把症状归到 CPU / 内存 / 慢 / 偶发**某一维**，再选手段？
- [ ] 「变慢」已区分整体（先查 GC）还是单点（trace）？
- [ ] 偶发/跨服务问题先用链路追踪定位到具体节点？
- [ ] 动手前先留了现场（栈/dump/日志），没有直接重启？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`cpu-high.md`](./cpu-high.md) · [`memory-leak.md`](./memory-leak.md) · [`arthas-online.md`](./arthas-online.md)
- GC 停顿与选型：[`../jvm/gc-selection.md`](../jvm/gc-selection.md)
- 链路追踪 / 可观测（traceId 贯穿）：[`../../framework/observability/index.md`](../../framework/observability/index.md)
