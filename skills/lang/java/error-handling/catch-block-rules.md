---
name: java-catch-block-rules
description: catch 到异常后怎么处理 — 禁空 catch，必须 log + 重抛或包装，包装时保留原始 cause。Use when 写 Java try/catch / 评审吞异常的代码 / 排查静默失败 bug 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - catch
  - 空 catch
  - 异常吞掉
  - 静默失败
  - swallow exception
  - 保留 cause
  - exception wrapping
effort: medium
context: inline
version: '1.0'
---
# Java · catch 块处理规则

> 本条只管「catch 到之后怎么办」。该抛 checked 还是 runtime 见 [`checked-vs-runtime.md`](./checked-vs-runtime.md)；资源释放见 [`resource-management.md`](./resource-management.md)。

## 规则

catch 到异常后，只有三种合法去向，**禁止第四种(吞掉)**：

| 去向 | 何时 |
|------|------|
| 重抛原异常 | 当前层处理不了，交给上层 |
| 包装成新异常**并带上 cause** | 跨层转译语义（如 IO → 业务异常）|
| log 后按业务降级 | 确实可恢复，且已记录足够排查信息 |

## 反例：吞掉异常

```java
// ❌ 静默 return null —— 调用方以为成功，bug 现场全丢
try {
    return loadConfig(path);
} catch (IOException e) {
    return null;
}

// ❌ 空 catch —— 同样吞掉，连日志都没有
try {
    doSomething();
} catch (Exception e) {
}
```

## 正例：包装时保留 cause

```java
// ✅ 第二个参数传 e，堆栈链不断
try {
    return loadConfig(path);
} catch (IOException e) {
    throw new ConfigLoadException("无法加载配置: " + path, e);
}
```

```java
// ✅ 确需降级也要先 log
try {
    return remoteCache.get(key);
} catch (TimeoutException e) {
    log.warn("cache miss on timeout, fallback to db: {}", key, e);
    return db.load(key);
}
```

## 自检

- [ ] 没有空 catch 块（`catch (X e) {}`）？
- [ ] 没有 catch 后静默 `return null` / `return` 吞掉？
- [ ] 包装新异常时把原异常作为 `cause` 传入（`new XxxException(msg, e)`）？
- [ ] 走降级分支前 log 了足够排查的信息？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`checked-vs-runtime.md`](./checked-vs-runtime.md)（该抛哪一类异常）
- 兄弟：[`resource-management.md`](./resource-management.md)（资源怎么释放）
