---
name: spring-boot-global-exception-handler
description: Spring Boot 全局异常处理 — @RestControllerAdvice 集中兜异常并转成统一 Result。Use when 加全局异常兜底 / 把 BusinessException 转返回体 / 评审散落 try-catch 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 全局异常处理
  - 异常兜底
  - '@RestControllerAdvice'
  - '@ExceptionHandler'
  - BusinessException
  - exception handler
effort: medium
context: inline
version: '1.0'
---
# Spring Boot · 全局异常处理

> 本条只管「异常如何集中转成接口返回体」。该抛哪类异常见 [`checked-vs-runtime.md`](../../lang/java/error-handling/checked-vs-runtime.md)；返回体结构见 [`controller-design.md`](./controller-design.md)。

## 规则

| 维度 | 约定 |
|------|------|
| 入口 | 用 `@RestControllerAdvice` 集中处理，**禁止**每个 Controller 各写 try-catch |
| 业务异常 | 专门 `@ExceptionHandler(BusinessException.class)` 转带业务码的 `Result` |
| 校验异常 | 单独处理 `MethodArgumentNotValidException` 等，提取字段错误信息 |
| 兜底 | 留一个 `@ExceptionHandler(Exception.class)` 防止异常裸奔到前端 |
| 日志 | 业务异常 `warn`，未知异常 `error` 带堆栈，绝不静默吞 |

## 正例

```java
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    // 业务异常：转成带业务码的统一返回体
    @ExceptionHandler(BusinessException.class)
    public Result<Void> handleBusiness(BusinessException e) {
        log.warn("业务异常: {}", e.getMessage());
        return Result.fail(e.getCode(), e.getMessage());
    }

    // 兜底：未预期异常不暴露堆栈给前端
    @ExceptionHandler(Exception.class)
    public Result<Void> handleUnknown(Exception e) {
        log.error("未处理异常", e);
        return Result.fail(500, "服务器内部错误");
    }
}
```

`BusinessException` 是 `RuntimeException` 子类，业务代码直接 `throw`，不污染方法签名（见相关链接）。

## 反例

```java
// ❌ 每个接口各自 try-catch，吞掉异常返回 null，且代码重复
@GetMapping("/{id}")
public Result<UserVO> get(@PathVariable Long id) {
    try {
        return Result.ok(userService.getById(id));
    } catch (Exception e) {
        return null; // 前端拿到 null，错误现场全丢
    }
}
```

❌ 只有兜底 `Exception` 一个 handler —— 业务异常和系统异常用同一个码，前端无法区分。

## 自检

- [ ] 有 `@RestControllerAdvice` 集中处理，Controller 里没有零散 try-catch？
- [ ] `BusinessException` 单独 handler，返回业务码？
- [ ] 有 `Exception.class` 兜底，未知异常不裸奔到前端？
- [ ] 未知异常 `log.error` 带堆栈，没有空 catch？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`controller-design.md`](./controller-design.md)（Result 返回体定义）
- 兄弟：[`param-validation.md`](./param-validation.md)（校验异常处理）
- 跨模块：[`checked-vs-runtime.md`](../../lang/java/error-handling/checked-vs-runtime.md)（该抛哪类异常 / BusinessException 选型）
