---
name: java-nio-files
description: 文件操作优先 java.nio.file.Files/Paths 而非老 File，字符集必须显式传 StandardCharsets.UTF_8。Use when 读写文件 / 遍历目录 / 排查中文乱码时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - NIO
  - Files
  - Paths
  - readAllLines
  - Files.walk
  - StandardCharsets.UTF_8
  - 字符集
  - 文件读写
  - 默认编码乱码
effort: medium
context: inline
version: '1.0'
---
# Java · NIO Files/Paths 文件操作

> 本条只管「用什么 API 读写文件 + 字符集」。流怎么 buffered 包装、大文件怎么流式处理见 [`buffered-stream.md`](./buffered-stream.md)。

## 规则

| 场景 | 用（NIO） | 别用（老 File） |
|------|----------|----------------|
| 构造路径 | `Path p = Paths.get(dir, name)` | `new File(dir, name)` |
| 读全部行 | `Files.readAllLines(p, UTF_8)` | 手搓 `BufferedReader` 循环 |
| 写文本 | `Files.write(p, bytes)` / `Files.writeString` | `FileWriter`（用平台默认编码） |
| 遍历目录树 | `Files.walk(p)` / `Files.list(p)` | `File.listFiles()` 递归 |
| 判存在 / 删除 / 建目录 | `Files.exists` / `delete` / `createDirectories` | `File.exists()`（出错只返回 boolean，无异常信息） |

**字符集铁律**：任何文本读写**必须显式传** `StandardCharsets.UTF_8`，绝不依赖平台默认编码（`Charset.defaultCharset()` 在不同 OS / locale 不一致，是中文乱码头号原因）。

## 正例

```java
import static java.nio.charset.StandardCharsets.UTF_8;

Path path = Paths.get("/data", "config.txt");

// ✅ 读：显式 UTF-8
List<String> lines = Files.readAllLines(path, UTF_8);

// ✅ 写：显式 UTF-8（Java 11+ writeString）
Files.writeString(path, "内容\n", UTF_8);

// ✅ 遍历目录树，记得关 Stream（见 buffered-stream 的 try-with-resources）
try (Stream<Path> tree = Files.walk(Paths.get("/data"))) {
    tree.filter(Files::isRegularFile)
        .filter(p -> p.toString().endsWith(".java"))
        .forEach(System.out::println);
}
```

## 反例

```java
// ❌ 不传字符集 —— 用平台默认编码，换台机器就乱码
List<String> lines = Files.readAllLines(path);          // 用了默认 UTF-8？不保证旧 JDK / 非 UTF-8 平台
String text = new String(Files.readAllBytes(path));     // new String 不传 charset，用平台默认

// ❌ 老 File API：删除失败只返回 false，丢失原因
File f = new File("/data/x.txt");
f.delete();                                              // 失败了你也不知道为什么

// ❌ FileWriter 永远用平台默认编码，没法显式指定（旧构造器）
new FileWriter("out.txt").write("中文");                 // 乱码风险
```

理由：老 `java.io.File` 的方法失败时多数只返回 `boolean`、不抛带原因的异常，难排查；且文本类 API 默认用平台编码。`Files` 系列失败抛 `IOException`（含路径与原因），并强制你在重载里传 `Charset`，把乱码风险消灭在编译期可见处。

## 自检

- [ ] 用 `Paths.get` / `Path` 而非 `new File(...)`？
- [ ] 所有文本读写都显式传 `StandardCharsets.UTF_8`，没有裸 `new String(bytes)` / `FileWriter`？
- [ ] 目录遍历用 `Files.walk` / `Files.list` 而非手写递归？
- [ ] `Files.walk` / `Files.list` 返回的 `Stream` 放进了 try-with-resources？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`buffered-stream.md`](./buffered-stream.md)（流怎么 buffered 包装、大文件别全读内存）
