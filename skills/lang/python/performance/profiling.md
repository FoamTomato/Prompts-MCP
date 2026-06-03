---
name: py-perf-profiling
description: Python 性能剖析工具选型 — cProfile/timeit/line_profiler/py-spy/memray。Use when 定位热点 / 测微基准 / 采样生产进程 / 排查内存。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 性能剖析
  - 热点定位
  - cProfile
  - py-spy
  - timeit
  - memray
effort: medium
context: inline
version: '1.0'
---
# Python · 性能剖析工具选型

先测后优：没有 profile 数据就改代码 = 猜。先定位真正热点，再动手。

## 规则

| 你要做的事 | 用什么 | 说明 |
|-----------|-------|------|
| 找整段代码的耗时热点 | `cProfile` + `pstats` | 标准库确定性剖析，看函数级累计耗时 |
| 比较两段小代码哪个快 | `timeit` | 微基准，多次运行取最小值，避免噪声 |
| 看某函数内逐行耗时 | `line_profiler`（`@profile`） | 第三方，热点函数内部下钻 |
| 采样线上/生产进程 | `py-spy` | 无需改代码、无需重启，低开销采样 |
| 排查内存峰值/泄漏 | `memray` / `tracemalloc` | 内存分配剖析，`tracemalloc` 为标准库 |

## 正例

```python
import cProfile
import pstats

with cProfile.Profile() as pr:
    result = build_report(dataset)

stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.CUMULATIVE).print_stats(10)  # 前 10 热点
```

```python
import timeit

# 比较 list 推导 vs map，各跑 100k 次取最小
t = timeit.repeat("[x * 2 for x in r]", setup="r = range(1000)",
                  number=100_000, repeat=5)
print(min(t))
```

```bash
# 生产进程：拿 PID 直接采样，不改代码不重启
py-spy record -o profile.svg --pid 12345
py-spy top --pid 12345          # 实时火焰图 top 视图
```

```python
import tracemalloc

tracemalloc.start()
load_large_cache()
snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics("lineno")[:10]:
    print(stat)  # 按行号列出分配最多的位置
```

## 反例

```python
# ❌ 凭直觉优化：把可读的循环改成晦涩的一行，却没测过它是否是热点
total = sum(map(lambda r: r.amount * fx[r.ccy], records))  # 真瓶颈其实在 DB 查询

# ❌ 用 time.time() 手测微基准 —— 单次运行受 GC/调度噪声主导，不可信
start = time.time(); f(); print(time.time() - start)
```

理由：90% 的耗时通常集中在 10% 的代码。不先 profile 就优化，往往优化了非热点，白费功夫还降低可读性。微基准必须多次重复取最小值（`timeit`），单次 `time.time()` 噪声太大。

## 自检

- [ ] 动手优化前，先用 cProfile / py-spy 拿到了热点数据？
- [ ] 微基准用 `timeit` 多次取最小，而不是单次 `time.time()`？
- [ ] 生产进程排查用 py-spy 采样，没去改线上代码加埋点？
- [ ] 内存问题用 memray / tracemalloc，而不是肉眼猜？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`caching-strategy.md`](./caching-strategy.md) · [`process-vs-thread-vs-async.md`](./process-vs-thread-vs-async.md)
