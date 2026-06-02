---
name: java-buffered-stream
description: 原始字节/字符流必须用 Buffered 包装减少系统调用，配合 try-with-resources 自动关闭，大文件按行/按块流式处理别一次性读进内存。Use when 包装 Java InputStream/Reader / 写文件复制循环 / 处理可能很大的文件时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - BufferedInputStream
  - BufferedReader
  - 缓冲流
  - buffered stream
  - 大文件
  - 流式处理
  - streaming
  - OutOfMemoryError
effort: medium
context: inline
version: '1.0'
---
# Java · 缓冲流与大文件

> 本条只管「流怎么包装 + 大文件怎么处理」。读写文件该用哪个 API、字符集见 [`nio-files.md`](./nio-files.md)；资源关闭的通用规则见 [`../error-handling/resource-management.md`](../error-handling/resource-management.md)。

## 规则

| 要求 | 怎么做 |
|------|--------|
| 减少系统调用 | 原始流外**必套** `BufferedInputStream` / `BufferedReader` / `BufferedWriter` |
| 自动关闭 | 流一律放进 **try-with-resources**（详见 resource-management） |
| 大文件读 | **按行 / 按块**处理，绝不 `readAllBytes` / `readAllLines` 整个吃进内存 |
| 大文件遍历 | 用 `Files.lines`（惰性、按行）而非 `Files.readAllLines`（全加载） |

判据：文件大小不可控（用户上传 / 日志 / 导出）→ 必须流式，避免 `OutOfMemoryError`。

## 正例

```java
import static java.nio.charset.StandardCharsets.UTF_8;

// ✅ 缓冲 + try-with-resources + 按行流式，文件多大都不爆内存
try (Stream<String> lines = Files.lines(Paths.get("/logs/huge.log"), UTF_8)) {
    long errors = lines.filter(l -> l.contains("ERROR")).count();
}

// ✅ 字节复制：缓冲包装 + 固定大小缓冲区，逐块搬
try (InputStream in = new BufferedInputStream(Files.newInputStream(src));
     OutputStream out = new BufferedOutputStream(Files.newOutputStream(dst))) {
    byte[] buf = new byte[8192];
    int n;
    while ((n = in.read(buf)) != -1) {
        out.write(buf, 0, n);
    }
}
```

## 反例

```java
// ❌ 裸流不缓冲：每个字节一次系统调用，慢几个数量级
InputStream in = Files.newInputStream(src);
int b;
while ((b = in.read()) != -1) { ... }       // 无 Buffered 包装

// ❌ 大文件一次性读进内存：文件几 GB 直接 OutOfMemoryError
byte[] all = Files.readAllBytes(Paths.get("/logs/huge.log"));
List<String> lines = Files.readAllLines(path);   // 同理，全量加载

// ❌ 流没关：用了缓冲但没 try-with-resources，句柄泄漏
BufferedReader r = new BufferedReader(new FileReader(file));
r.readLine();                                 // 漏 close
```

理由：每次 `read()` 直达底层是一次系统调用，`Buffered*` 用内存缓冲区批量读写、把系统调用次数降几个数量级。文件大小不可控时整体加载会 OOM，必须 `Files.lines` / 固定缓冲区逐块处理。

## 自检

- [ ] 原始 `InputStream` / `Reader` / `OutputStream` / `Writer` 都套了 `Buffered*`？
- [ ] 所有流都在 try-with-resources 里（见 [`resource-management.md`](../error-handling/resource-management.md)）？
- [ ] 大小不可控的文件用 `Files.lines` / 逐块读，而非 `readAllBytes` / `readAllLines`？
- [ ] 复制循环用固定大小 `byte[]` 缓冲区，没把整文件读成一个数组？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`nio-files.md`](./nio-files.md)（用哪个 API 读写 + 字符集）
- 跨模块：[`../error-handling/resource-management.md`](../error-handling/resource-management.md)（try-with-resources 通用规则）
