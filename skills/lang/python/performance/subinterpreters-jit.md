---
name: py-perf-subinterpreters-jit
description: Python 前沿运行时 — 子解释器(PEP 734)、JIT(PEP 744)、specializing interpreter 定位与取舍。Use when 评估子解释器并行 / JIT 提速 / 决定是否上 3.13+ 新特性。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 子解释器
  - 前沿运行时
  - subinterpreters
  - PEP 734
  - JIT
  - specializing interpreter
effort: high
context: inline
version: '1.0'
---
# Python · 前沿运行时特性

这些是 3.12+ 起逐步落地的实验/新特性。定位：先确认现有手段（多进程/async/缓存）不够用，再评估它们，别盲目尝鲜。

## 规则

| 特性 | 是什么 | 现状与取舍 |
|------|-------|-----------|
| 子解释器 `interpreters`（PEP 734） | 同进程内多个隔离解释器，各自独立 GIL | 3.12 C-API / 3.13+ 渐入；比进程轻、比线程隔离，跨解释器传数据受限 |
| JIT（PEP 744） | CPython 内置即时编译器，运行时编译热路径 | 3.13 起默认关闭、需构建开启；当前提速有限，逐版本演进 |
| Specializing interpreter | 自适应字节码特化（PEP 659） | 3.11+ 默认开启、透明免配置；多数提速来自它，无需改代码 |
| free-threading | 移除 GIL 的构建（PEP 703/779） | 3.13 实验 / 3.14 官方支持；线程真并行，单线程约 5-10% 损耗 |

## 正例

```python
# 子解释器：各解释器独立 GIL，可在同进程内并行跑 CPU 任务（API 仍在演进）
from concurrent import interpreters    # 名称/路径随版本变化，以所用版本文档为准

interp = interpreters.create()
interp.exec("result = sum(range(10_000_000))")
interp.close()
```

```bash
# JIT 与 free-threading 都是构建期选项，先实测再决定是否上生产
python3.13 -c "import sys; print(sys._is_gil_enabled())"   # 探测是否 no-GIL 构建
PYTHON_JIT=1 python3.13 app.py                              # 显式开启实验 JIT
```

## 反例

```python
# ❌ 把子解释器 / JIT 当成「免费提速开关」直接上生产
#    实际：API 未稳定、加速因负载而异、C 扩展未必兼容 —— 必须先压测对比

# ❌ 没量化就为追新而换 free-threading 构建
#    实际：单线程任务反而变慢（约 5-10%），收益只在多核 CPU 密集场景体现
```

理由：specializing interpreter 是唯一「升级解释器即免费得到、无需改代码」的提速来源。子解释器、JIT、free-threading 都仍在演进，加速因负载而异、依赖兼容性需逐一验证。把它们当稳定开关直接上生产，风险远大于收益——务必先在真实负载上压测对比，再决定。

## 自检

- [ ] 确认过常规手段（多进程 / async / 缓存）不足，才评估前沿特性？
- [ ] 升级到 3.11+ 已自动享受 specializing interpreter，无需额外配置？
- [ ] 上 JIT / free-threading / 子解释器前，在真实负载上压测对比过？
- [ ] 验证过所有 C 扩展依赖与目标构建兼容？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`process-vs-thread-vs-async.md`](./process-vs-thread-vs-async.md)（成熟的 GIL 绕行选型） · [`profiling.md`](./profiling.md)
