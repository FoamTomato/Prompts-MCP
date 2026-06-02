---
name: lang-java-io-index
description: Java IO 两件事 — 文件读写用 NIO Files/Paths（显式 UTF-8）/ 流必须 buffered 包装且别一次性读大文件进内存。Use when 写 Java 文件读写 / 包装 InputStream / 处理大文件或乱码问题时。
parent: ../index.md
children:
  - { name: nio-files, path: nio-files.md, tag: skill, note: Files/Paths 优先于老 File，readAllLines/walk，字符集显式 UTF_8 }
  - { name: buffered-stream, path: buffered-stream.md, tag: skill, note: 流必须 buffered 包装 + try-with-resources，大文件流式处理别全读内存 }
when_to_descend: 写 / 评审 Java 文件读写、流处理、大文件场景
---

# IO · 子项索引

IO 拆成两个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 读写文件路径 / 遍历目录 / 担心默认字符集乱码 | [nio-files](nio-files.md) |
| 包装字节或字符流 / 担心性能 / 处理可能很大的文件 | [buffered-stream](buffered-stream.md) |
