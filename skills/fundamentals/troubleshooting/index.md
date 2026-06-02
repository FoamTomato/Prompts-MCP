---
name: fundamentals-troubleshooting-index
description: Java 线上故障排查四件事 — CPU 飙高 / 内存泄漏 OOM / Arthas 在线诊断 / 按症状分流的决策树。Use when 线上 CPU 打满 / 内存涨爆 / 接口变慢 / 选排查手段时。
parent: ../index.md
children:
  - { name: troubleshooting-cpu-high, path: cpu-high.md, tag: skill, note: "CPU 飙高：top -H 找线程 → jstack 定位 RUNNABLE 栈" }
  - { name: troubleshooting-memory-leak, path: memory-leak.md, tag: skill, note: "内存泄漏/OOM：jmap dump → MAT 支配树/最大对象" }
  - { name: troubleshooting-arthas-online, path: arthas-online.md, tag: skill, note: "Arthas 免重启在线诊断：watch / trace / 火焰图" }
  - { name: troubleshooting-diagnosis-decision-tree, path: diagnosis-decision-tree.md, tag: skill, note: 先按症状选手段的排查总决策树 }
when_to_descend: 线上 CPU 打满、内存涨爆、接口变慢、偶发抖动，要选用哪种排查手段时下钻
---

# 线上排查 · 子项索引

线上故障排查拆成四个**独立决策点**：先用决策树按症状分流，再下钻到具体手段。

| 你在做什么 | 进哪个 |
|-----------|-------|
| 不确定该用哪种工具，先按症状（CPU/内存/变慢/偶发）分流 | [diagnosis-decision-tree](diagnosis-decision-tree.md) |
| CPU 占用打满，要定位是哪段代码在烧 CPU | [cpu-high](cpu-high.md) |
| 内存持续上涨 / 抛 `OutOfMemoryError`，要找泄漏的对象 | [memory-leak](memory-leak.md) |
| 想免重启在线看方法入参出参 / 方法耗时 / 火焰图 | [arthas-online](arthas-online.md) |
