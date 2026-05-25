---
name: java-checked-vs-runtime
description: Checked vs Runtime 异常使用边界
parent: ./index.md
paths:
  - "*.java"
triggers:
  keywords: [Exception, RuntimeException]
effort: medium
context: inline
version: "1.0"
---

# Java · Checked vs Runtime 异常

## 规则

| 场景 | 用 |
|------|-----|
| 业务异常 | RuntimeException 子类（如 `BusinessException`） |
| 调用方应当处理的失败 | Checked Exception（如 `IOException`） |
| 框架不允许 throws 的位置 | RuntimeException |
| 不可恢复的程序错误 | Error 子类 |

## 业务异常推荐 RuntimeException

```java
public class BusinessException extends RuntimeException {
    private final int code;

    public BusinessException(String msg, int code) {
        super(msg);
        this.code = code;
    }

    public int getCode() { return code; }
}

// 使用
if (user.getBalance() < amount) {
    throw new BusinessException("余额不足", 403);
}
```

理由：业务异常不希望污染所有方法签名。Spring 上层有 `@RestControllerAdvice` 兜底。

## Checked 用于明确合约

```java
// 这个方法可能失败，调用方必须显式处理
public Config loadConfig(Path path) throws IOException {
    return objectMapper.readValue(path.toFile(), Config.class);
}

// 调用方
try {
    Config c = loadConfig(path);
} catch (IOException e) {
    log.error("config load failed", e);
    System.exit(1);
}
```

## 反例

```java
// ❌ 把 IOException 包装成 RuntimeException 后吞掉
try {
    return loadConfig(path);
} catch (IOException e) {
    return null;   // 静默失败，调用方以为成功
}

// ✅ 包装但保留信息
try {
    return loadConfig(path);
} catch (IOException e) {
    throw new ConfigLoadException("无法加载配置: " + path, e);
}
```

## try-with-resources 必用

```java
// ❌ 手动 close 容易遗漏
InputStream in = new FileInputStream(file);
try { ... } finally { in.close(); }

// ✅
try (InputStream in = new FileInputStream(file)) {
    ...
}   // 自动 close
```

## 自检

- [ ] 业务异常用 `RuntimeException` 子类（如 `BusinessException`）？
- [ ] Checked 异常表达调用方必须处理的合约？
- [ ] 不空 catch（必须 log + 重抛或包装）？
- [ ] 资源用 try-with-resources？

## 相关

- 父：[`./index.md`](./index.md)

