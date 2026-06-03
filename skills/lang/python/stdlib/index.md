---
name: lang-python-stdlib-index
description: Python 标准库重点用法（collections / itertools / functools / pathlib / dataclasses / enum）。Use when 选数据结构 / 写迭代管道 / 缓存装饰器 / 处理文件路径 / 建数据模型。
parent: ../index.md
children:
  - { name: py-stdlib-collections-toolkit, path: collections-toolkit.md, tag: skill, note: defaultdict / Counter / deque / namedtuple / ChainMap }
  - { name: py-stdlib-itertools-pipeline, path: itertools-pipeline.md, tag: skill, note: chain / groupby / islice / accumulate 惰性管道 }
  - { name: py-stdlib-functools-toolkit, path: functools-toolkit.md, tag: skill, note: lru_cache / partial / wraps / singledispatch / cached_property }
  - { name: py-stdlib-pathlib-over-ospath, path: pathlib-over-ospath.md, tag: skill, note: Path 面向对象路径取代 os.path }
  - { name: py-stdlib-dataclasses-usage, path: dataclasses-usage.md, tag: skill, note: "@dataclass / field / frozen / slots / __post_init__" }
  - { name: py-stdlib-enum-usage, path: enum-usage.md, tag: skill, note: "Enum / IntEnum / StrEnum / Flag + auto()" }
when_to_descend: 选用标准库容器 / 迭代器组合 / 缓存与高阶函数 / 路径处理 / 数据建模 / 枚举常量。
---

# Python · 标准库重点 · 子项索引

| 你在做什么 | 进哪个 |
|------|-------|
| 计数 / 分组累加 / 双端队列 / 轻量记录 | collections-toolkit |
| 拼接、分组、切片、累计等惰性迭代管道 | itertools-pipeline |
| 函数缓存、固定参数、装饰器、单分派 | functools-toolkit |
| 拼接路径、读写文件、glob 通配 | pathlib-over-ospath |
| 定义纯数据载体（字段、不可变、省内存） | dataclasses-usage |
| 定义一组命名常量 / 位标志 | enum-usage |
