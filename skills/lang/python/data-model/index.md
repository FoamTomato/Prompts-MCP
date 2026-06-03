---
name: lang-python-data-model-index
description: Python 语言核心/数据模型规则索引（可变默认参数 / is vs == / 拷贝语义 / dunder 协议 / 闭包延迟绑定 / GIL 与 free-threading）。Use when 排查共享状态 bug / 设计值对象 / 选并发模型。
parent: ../index.md
children:
  - { name: py-mutable-default-arg, path: mutable-default-arg.md, tag: skill, note: "def f(x=[]) 陷阱，用 None 哨兵" }
  - { name: py-is-vs-equals, path: is-vs-equals.md, tag: skill, note: "is 比身份 / == 比相等，None 用 is" }
  - { name: py-copy-semantics, path: copy-semantics.md, tag: skill, note: 引用语义 / 浅拷贝 vs deepcopy }
  - { name: py-dunder-protocol, path: dunder-protocol.md, tag: skill, note: "__eq__/__hash__ 成对 / __repr__ / 真值协议" }
  - { name: py-closure-late-binding, path: closure-late-binding.md, tag: skill, note: 闭包延迟绑定 / LEGB / nonlocal }
  - { name: py-gil-and-free-threading, path: gil-and-free-threading.md, tag: skill, note: "GIL 语义 / 3.13/3.14 free-threading" }
when_to_descend: 出现意外共享状态 / 对象相等性 / 循环里建闭包 / CPU 密集多线程不提速。
---

# Python · 数据模型 / 语言核心 子项索引

| 你在做什么 | 进哪个 |
|-----------|-------|
| 函数默认值是 list/dict/set，多次调用结果串了 | mutable-default-arg |
| 不确定该写 `is` 还是 `==`，或判 None / 缓存小整数踩坑 | is-vs-equals |
| 赋值后改一个对象，另一个跟着变；要复制嵌套结构 | copy-semantics |
| 给类加相等性 / 哈希 / 打印 / 真值判断 | dunder-protocol |
| for 循环里建的 lambda 全引用了同一个变量 | closure-late-binding |
| 多线程跑 CPU 密集不提速，或在评估 3.13/3.14 no-GIL | gil-and-free-threading |
