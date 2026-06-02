---
name: spring-boot-param-validation
description: Spring Boot 参数校验 — @Valid/@Validated + JSR-303 注解 + 分组校验 + 自定义校验器。Use when 校验请求入参 / 复用 DTO 做新增与更新校验 / 写自定义约束注解时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 参数校验
  - 分组校验
  - '@Valid'
  - '@Validated'
  - 自定义校验器
  - JSR-303
effort: medium
context: inline
version: '1.0'
---
# Spring Boot · 参数校验

> 本条只管「入参怎么校验」。校验失败异常如何转返回体见 [`global-exception-handler.md`](./global-exception-handler.md)。

## 规则

| 场景 | 用法 |
|------|------|
| 校验请求体对象 | 参数前加 `@Valid`（或 `@Validated`），约束注解写在 DTO 字段上 |
| 校验单个方法参数 | 类上 `@Validated`，参数上直接 `@NotNull` / `@Min` 等 |
| 一个 DTO 复用于新增/更新 | **分组校验**：定义分组接口，注解写 `groups`，入口用 `@Validated(组.class)` |
| 内置注解覆盖不了 | 自定义约束注解 + 实现 `ConstraintValidator` |
| 嵌套对象 | 字段上加 `@Valid` 才会级联校验 |

## 正例

```java
public interface Create {}
public interface Update {}

@Data
public class UserDTO {
    @NotNull(groups = Update.class, message = "更新必须带 id")
    private Long id;

    @NotBlank(message = "用户名必填")
    @Size(min = 2, max = 20)
    private String name;

    @Email(message = "邮箱格式不正确")
    private String email;
}

@PostMapping
public Result<Void> create(@Validated(Create.class) @RequestBody UserDTO dto) {
    userService.create(dto);
    return Result.ok(null);
}
```

```java
// 自定义校验器：手机号
@Documented
@Constraint(validatedBy = PhoneValidator.class)
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
public @interface Phone {
    String message() default "手机号格式不正确";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}

public class PhoneValidator implements ConstraintValidator<Phone, String> {
    @Override
    public boolean isValid(String value, ConstraintValidatorContext ctx) {
        return value != null && value.matches("^1[3-9]\\d{9}$");
    }
}
```

## 反例

```java
// ❌ 在 Controller 里手写 if 校验，规则散落、无法复用、错误信息不统一
@PostMapping
public Result<Void> create(@RequestBody UserDTO dto) {
    if (dto.getName() == null || dto.getName().isEmpty()) {
        return Result.fail(400, "用户名必填");
    }
    // ... 一堆 if
}
```

❌ 忘了加 `@Valid`/`@Validated` —— 注解形同虚设，校验根本不触发。

## 自检

- [ ] 校验入口加了 `@Valid` 或 `@Validated`，否则约束不生效？
- [ ] 校验规则在 DTO 字段上，没散落在 Controller 的 if 里？
- [ ] 新增/更新共用 DTO 时用 `groups` 分组，没建两个雷同 DTO？
- [ ] 内置注解不够时自定义 `ConstraintValidator`，没绕回手写 if？
- [ ] 校验失败异常交给全局处理器，没在本地 catch？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`global-exception-handler.md`](./global-exception-handler.md)（校验失败异常转返回体）
- 兄弟：[`controller-design.md`](./controller-design.md)（接口入参绑定）
