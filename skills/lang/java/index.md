---
name: lang-java-index
description: Java 语言级规则索引（命名 / 异常处理 / 集合 / 并发 / 泛型 / IO / 日期时间 / 编码规范 / utils / 分层）
parent: ../index.md
children:
  - { name: naming, path: naming/index.md, tag: folder, note: 类 / 方法 / 包命名规约 }
  - { name: error-handling, path: error-handling/index.md, tag: folder, note: 异常选型 / catch 处理 / 资源释放 }
  - { name: collections, path: collections/index.md, tag: folder, note: 集合选型 / Stream / 不可变 / 并发集合 }
  - { name: concurrency, path: concurrency/index.md, tag: folder, note: 线程池 / Executors 禁用 / CompletableFuture / 锁选型 / ThreadLocal }
  - { name: generics, path: generics/index.md, tag: folder, note: 泛型通配符 PECS / 类型擦除的坑 }
  - { name: io, path: io/index.md, tag: folder, note: NIO Files/Paths / 缓冲流与大文件 }
  - { name: datetime, path: datetime/index.md, tag: folder, note: java.time 取代旧 Date / 时区处理 }
  - { name: coding-style, path: coding-style/index.md, tag: folder, note: 禁魔法值 / Optional / 防 NPE / equals-hashCode / 字符串 / Lombok }
  - { name: utils, path: utils/index.md, tag: folder, note: 工具类设计 / 用成熟库 / Bean 拷贝 }
  - { name: layering, path: layering/index.md, tag: folder, note: Controller / Service / Repository 分层 }
  - { name: pipeline-style, path: pipeline-style/index.md, tag: folder, note: 注释驱动流水线编排 / 抽 Converter-Validator（团队风格基准） }
when_to_descend: |
  写 / 改任何 `.java` 文件、Spring / Spring Boot 项目代码。
---

# Java · 语言级规则

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| naming | 文件夹 | 类 / 方法 / 包命名 |
| error-handling | 文件夹 | 异常选型 / catch 处理 / 资源释放（3 子项） |
| collections | 文件夹 | 集合选型 / Stream / 不可变集合 / 并发集合（4 子项） |
| concurrency | 文件夹 | 线程池 / Executors 禁用 / CompletableFuture / 锁 / ThreadLocal（5 子项） |
| generics | 文件夹 | 泛型通配符 PECS / 类型擦除的坑（2 子项） |
| io | 文件夹 | NIO Files/Paths / 缓冲流与大文件（2 子项） |
| datetime | 文件夹 | java.time 取代旧 Date / 时区处理（2 子项） |
| coding-style | 文件夹 | 禁魔法值 / Optional / 防 NPE / equals-hashCode / 字符串 / Lombok（6 子项） |
| utils | 文件夹 | 工具类设计 / 用成熟库 / Bean 拷贝（3 子项） |
| layering | 文件夹 | Controller / Service / Repository |
| pipeline-style | 文件夹 | 注释驱动流水线编排 / 抽 Converter-Validator（团队风格基准，2 子项） |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../python/index.md`](../python/index.md) · [`../typescript/index.md`](../typescript/index.md)
