---
name: java-checked-vs-runtime
description: 该抛 Checked 还是 Runtime 异常的选型边界 — 业务异常用 RuntimeException 子类，调用方必须处理的失败用 Checked。Use when 设计 Java 异常类型 / 写 throws 签名 / 评审异常分类时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - Checked Exception
  - RuntimeException
  - 异常使用边界
  - 异常选型
  - BusinessException
  - throws
effort: medium
context: inline
version: '1.0'
---
# Java · Checked vs Runtime 异常

> 本条只管「该抛哪一类异常」。catch 到之后怎么处理见 [`catch-block-rules.md`](./catch-block-rules.md)；资源释放见 [`resource-management.md`](./resource-management.md)。

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
```

`throws IOException` 把「这里会失败」写进方法签名，编译器强制调用方决定怎么处理（catch 的写法见 [`catch-block-rules.md`](./catch-block-rules.md)）。

## 自检

- [ ] 业务异常用 `RuntimeException` 子类（如 `BusinessException`）？
- [ ] Checked 异常表达调用方必须处理的合约？
- [ ] 框架不允许 throws 的位置改用 RuntimeException？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`catch-block-rules.md`](./catch-block-rules.md)（catch 到之后怎么办）
- 兄弟：[`resource-management.md`](./resource-management.md)（资源怎么释放）
