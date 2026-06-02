---
name: spring-boot-controller-design
description: Spring Boot 控制器设计 — @RestController + RESTful 路由 + 统一返回体 Result<T>（code/msg/data）。Use when 写 REST 接口 / 定接口返回结构 / 评审 Controller 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 统一返回体
  - RESTful 接口
  - Result
  - '@RestController'
  - 控制器设计
  - ResponseEntity
effort: medium
context: inline
version: '1.0'
---
# Spring Boot · 控制器设计与统一返回体

> 本条只管「接口怎么定 + 返回什么结构」。异常转返回体见 [`global-exception-handler.md`](./global-exception-handler.md)；入参校验见 [`param-validation.md`](./param-validation.md)。

## 规则

| 维度 | 约定 |
|------|------|
| 注解 | `@RestController`（= `@Controller` + `@ResponseBody`），不手写返回 JSON |
| 路由 | 资源名用复数名词、动词靠 HTTP method：`GET /users/{id}`、`POST /users` |
| 返回体 | 业务接口统一包 `Result<T>`，含 `code` / `msg` / `data` 三字段 |
| 职责 | Controller 只做参数绑定 + 调 service + 包返回体，**不写业务逻辑** |
| HTTP 状态码 | 走通的请求统一 200，业务结果靠 `Result.code` 表达 |

## 正例

```java
@Data
@AllArgsConstructor
public class Result<T> {
    private int code;       // 0 成功，非 0 业务错误码
    private String msg;
    private T data;

    public static <T> Result<T> ok(T data) {
        return new Result<>(0, "ok", data);
    }
    public static <T> Result<T> fail(int code, String msg) {
        return new Result<>(code, msg, null);
    }
}

@RestController
@RequestMapping("/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    @GetMapping("/{id}")
    public Result<UserVO> get(@PathVariable Long id) {
        return Result.ok(userService.getById(id));
    }
}
```

## 反例

```java
// ❌ 每个接口各定一套 Map 返回，前端无法统一解析
@GetMapping("/{id}")
public Map<String, Object> get(@PathVariable Long id) {
    Map<String, Object> m = new HashMap<>();
    m.put("user", userService.getById(id));
    return m;
}
```

❌ Controller 里写 if/else 业务判断、拼 SQL、catch 异常返回 null —— 业务逻辑下沉到 service，异常交给全局处理器。

## 自检

- [ ] 用 `@RestController`，没手写 JSON 序列化？
- [ ] 业务接口返回 `Result<T>`，三字段齐全（code/msg/data）？
- [ ] 路由是资源名词，动作靠 HTTP method 区分？
- [ ] Controller 不含业务逻辑，只编排 service 调用？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`global-exception-handler.md`](./global-exception-handler.md)（异常统一转 Result）
- 兄弟：[`param-validation.md`](./param-validation.md)（入参校验）
