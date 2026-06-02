---
name: api-doc-springdoc-openapi
description: Spring Boot 3 用 springdoc-openapi 替代过时的 springfox，靠 @Operation/@Schema/@Parameter 生成 OpenAPI 3 文档。Use when 选文档 starter / 给接口加注解 / 从 springfox 迁移时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 接口文档注解
  - springdoc-openapi
  - springfox 迁移
  - '@Operation'
  - '@Schema'
  - OpenAPI 3
effort: medium
context: inline
version: '1.0'
---
# API 文档 · springdoc-openapi 注解

> 本条只管「Spring Boot 3 选哪个库 + 怎么写文档注解」。文档 UI 见 [`knife4j.md`](./knife4j.md)；防漂移与生产安全见 [`doc-as-contract.md`](./doc-as-contract.md)。

## 规则

| 维度 | 约定 |
|------|------|
| 选型 | Spring Boot 3 用 `springdoc-openapi-starter-webmvc-ui`；**禁用 springfox**（停更、不兼容 Boot 3 / Jakarta） |
| 接口描述 | 方法上 `@Operation(summary, description)`，类上 `@Tag` 分组 |
| 参数描述 | `@Parameter` 标注单个入参；路径/查询参数说明含义与是否必填 |
| 模型字段 | DTO 字段用 `@Schema(description, example)`，**不要**靠字段名让前端猜 |
| 不侵入校验 | 必填/格式仍由 JSR-303（`@NotBlank` 等）表达，文档只描述不替代校验 |

## 正例

```java
@Tag(name = "用户", description = "用户增删改查")
@RestController
@RequestMapping("/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    @Operation(summary = "按 ID 查用户", description = "不存在时返回业务码 404")
    @GetMapping("/{id}")
    public Result<UserVO> get(
            @Parameter(description = "用户主键", required = true) @PathVariable Long id) {
        return Result.ok(userService.getById(id));
    }
}

@Data
public class UserVO {
    @Schema(description = "用户 ID", example = "1001")
    private Long id;

    @Schema(description = "昵称", example = "张三")
    private String name;
}
```

依赖（Maven）：

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.x</version>  <!-- 以官网最新 2.x 为准 -->
</dependency>
```

## 反例

```java
// ❌ Boot 3 仍引 springfox：启动报 NoSuchMethodError / 与 Jakarta 命名空间冲突
// io.springfox:springfox-boot-starter  —— 已停更，不要再用

// ❌ 字段无 @Schema，前端只能靠字段名猜含义和示例值
public class UserVO {
    private Long id;     // 是自增？雪花？前端无从得知
    private String name; // 昵称还是真名？
}
```

## 自检

- [ ] Spring Boot 3 用 `springdoc-openapi-starter-webmvc-ui`，没有残留 springfox 依赖？
- [ ] 每个接口有 `@Operation` 摘要，分组有 `@Tag`？
- [ ] DTO 字段有 `@Schema(description, example)`，不靠字段名猜？
- [ ] 必填/格式仍由 JSR-303 校验注解保证，没把 `@Parameter` 当校验用？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`knife4j.md`](./knife4j.md)（基于本注解的增强文档 UI）
- 兄弟：[`doc-as-contract.md`](./doc-as-contract.md)（注解与代码同源防漂移、生产关端点）
- 跨模块：[`../spring-boot/param-validation.md`](../spring-boot/param-validation.md)（JSR-303 校验）
