---
name: java-resource-management
description: 实现 AutoCloseable 的资源（流 / 连接 / 锁）必须用 try-with-resources 自动关闭，禁手动 finally close。Use when 写 Java IO / 操作 InputStream、Connection、Reader / 评审资源泄漏风险时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - try-with-resources
  - AutoCloseable
  - 资源关闭
  - 资源泄漏
  - InputStream
  - Connection
  - resource leak
effort: low
context: inline
version: '1.0'
---
# Java · 资源管理（try-with-resources）

> 本条只管「资源怎么关」。异常该抛哪类见 [`checked-vs-runtime.md`](./checked-vs-runtime.md)；catch 到怎么处理见 [`catch-block-rules.md`](./catch-block-rules.md)。

## 规则

任何实现 `AutoCloseable` / `Closeable` 的资源（`InputStream` / `Reader` / `Connection` / `Statement` / 自定义锁包装等），**一律 try-with-resources**，禁手动 `finally { close() }`。

## 反例：手动 close

```java
// ❌ 手动 close 容易遗漏；close 本身抛异常还会盖住 try 内的真异常
InputStream in = new FileInputStream(file);
try {
    process(in);
} finally {
    in.close();
}
```

## 正例：try-with-resources

```java
// ✅ 自动 close，且多资源按声明逆序关闭
try (InputStream in = new FileInputStream(file)) {
    process(in);
}   // in 自动 close

// ✅ 多资源
try (Connection conn = dataSource.getConnection();
     PreparedStatement ps = conn.prepareStatement(SQL)) {
    return ps.executeQuery();
}
```

## 自检

- [ ] 所有 `AutoCloseable` 资源都在 try-with-resources 的括号里声明？
- [ ] 没有手写 `finally { x.close() }`？
- [ ] 多资源场景未手动嵌套 try，而是一个 try 里分号分隔？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`catch-block-rules.md`](./catch-block-rules.md)（close 抛异常时怎么处理）
- 兄弟：[`checked-vs-runtime.md`](./checked-vs-runtime.md)
