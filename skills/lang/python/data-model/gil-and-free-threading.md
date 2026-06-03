---
name: py-gil-and-free-threading
description: GIL 让 CPython 同一时刻只跑一个线程的字节码，故多线程不加速 CPU 密集；3.13/3.14 free-threading(PEP 703/779) 可关 GIL。Use when 多线程跑满 CPU 却不提速 / 选并发模型 / 评估 no-GIL 构建。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - GIL
  - 全局解释器锁
  - free-threading
  - 自由线程
  - PEP 703
effort: high
context: inline
version: '1.0'
---
# Python · GIL 与 free-threading

## 规则

| 工作负载 | 标准 CPython（带 GIL） | 该用什么 |
|---------|----------------------|---------|
| CPU 密集（算数 / 解析 / 压缩） | 多线程**不提速**：GIL 让字节码串行执行 | `multiprocessing` / `ProcessPoolExecutor`，或 free-threading 构建 |
| I/O 密集（网络 / 磁盘 / DB） | 多线程**有效**：阻塞时释放 GIL | `threading` / `asyncio` |
| 调 C 扩展（numpy / 压缩库） | 计算段常释放 GIL，可并行 | 多线程即可 |

核心：**GIL 是 CPython 实现的一把进程级互斥锁，同一时刻只有一个线程执行 Python 字节码。** 它简化了内存管理，但使纯 Python 的 CPU 密集多线程退化为串行 + 切换开销。

## free-threading（PEP 703 / 779，3.13 起）

```text
3.13  引入实验性 free-threaded 构建（python3.13t），可在运行时关闭 GIL
3.14  PEP 779：free-threading 从实验转为“官方支持”阶段（仍非默认）
代价  单线程性能有约 5-10% 损耗；默认解释器仍带 GIL
检测  python -VV 看是否 free-threading；运行期 sys._is_gil_enabled()
```

## 正例

```python
from concurrent.futures import ProcessPoolExecutor

def cpu_heavy(n: int) -> int:
    return sum(i * i for i in range(n))   # 纯 Python CPU 密集

# ✅ 标准 CPython 下，CPU 密集靠多进程绕开 GIL
with ProcessPoolExecutor() as pool:
    results = list(pool.map(cpu_heavy, [10_000_000] * 8))
```

```python
import sys
# 探测当前解释器是否真的关掉了 GIL（free-threaded 构建才有此函数）
if hasattr(sys, "_is_gil_enabled") and not sys._is_gil_enabled():
    from concurrent.futures import ThreadPoolExecutor  # 此时线程可真正并行 CPU
```

## 反例

```python
# ❌ 标准 CPython 下用线程跑 CPU 密集，期望多核加速
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=8) as pool:
    pool.map(cpu_heavy, [10_000_000] * 8)   # 8 核机器上几乎不比单线程快
```

理由：GIL 保证同一时刻仅一个线程跑字节码，纯计算线程拿不到并行，反而多了锁竞争与上下文切换。CPU 密集要么多进程、要么用 free-threading 构建（确认 GIL 已关）。

## 自检

- [ ] CPU 密集用多进程 / free-threading，没指望标准 CPython 的多线程加速？
- [ ] I/O 密集才用 `threading` / `asyncio`？
- [ ] 用 free-threading 前确认了 `python -VV` / `sys._is_gil_enabled()`，并接受单线程 5-10% 损耗？
- [ ] 依赖的 C 扩展声明了 free-threading 兼容，避免在无 GIL 下竞态？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`copy-semantics.md`](./copy-semantics.md)（多进程间对象需序列化拷贝） · [`is-vs-equals.md`](./is-vs-equals.md)
