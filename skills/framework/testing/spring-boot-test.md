---
name: testing-spring-boot-test
description: Spring Boot 测试分层选型 — @SpringBootTest 全容器集成 vs @WebMvcTest 切 controller 层 vs 纯单测不起 Spring。Use when 纠结要不要起 Spring 容器 / 选哪个测试注解时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 集成测试
  - 测试切片
  - '@SpringBootTest'
  - '@WebMvcTest'
  - MockMvc
  - '@MockBean'
effort: medium
context: inline
version: '1.0'
---
# Spring Boot · 测试注解选型

> 本条只管「起不起 Spring、起多大、用哪个注解」。Mockito 打桩语法见 [`mockito-stubbing.md`](./mockito-stubbing.md)；分层比例见 [`test-pyramid.md`](./test-pyramid.md)。

## 选型表（从快到慢，能小别大）

| 场景 | 用什么 | 起多少 Spring |
|------|--------|--------------|
| 测 service/util 纯逻辑 | **纯单测**（JUnit5 + Mockito，不加 Spring 注解） | 不起容器，最快 |
| 测 controller 的路由/参数绑定/返回 JSON | `@WebMvcTest(Xxx.class)` + `MockMvc` | 只切 Web 层，service 用 `@MockBean` |
| 测 dao/repository 真实读写 | `@DataJpaTest` / `@MybatisTest` | 只切持久层 + 内存库 |
| 测多层串起来的完整链路 | `@SpringBootTest` | 起全量容器，最慢，量要少 |

## 正例

```java
// ① controller 层切片：只起 Web，service 被 mock
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired MockMvc mockMvc;
    @MockBean UserService userService;   // 切片内 mock 协作 Bean

    @Test
    void get_shouldReturn200() throws Exception {
        when(userService.getById(1L)).thenReturn(new UserVO("Tom"));
        mockMvc.perform(get("/users/1"))
               .andExpect(status().isOk())
               .andExpect(jsonPath("$.data.name").value("Tom"));
    }
}

// ② 完整集成：起整个上下文，少量关键链路才用
@SpringBootTest
@AutoConfigureMockMvc
class OrderFlowIT {
    @Autowired MockMvc mockMvc;
    // ... 跑下单全链路
}
```

> 切片里替换 Bean 用 `@MockBean`（进 Spring 容器），纯单测里用 `@Mock`（不进容器）—— 别混用。

## 反例

```java
// ❌ 只想测 controller 的 JSON 格式，却起全量 @SpringBootTest
@SpringBootTest                 // 连 DB/MQ/缓存全拉起，几秒一个用例，CI 拖垮
class UserControllerTest {
    // 该用 @WebMvcTest
}
```

❌ 测纯工具类还加 `@SpringBootTest` —— 起容器纯属浪费，直接 new 对象单测。

## 自检

- [ ] 纯逻辑用纯单测，没无谓地起 Spring 容器？
- [ ] 测 controller 用 `@WebMvcTest` + `MockMvc`，而非全量集成？
- [ ] 切片内替换 Bean 用 `@MockBean`，纯单测用 `@Mock`，没混？
- [ ] `@SpringBootTest` 只留给少量必须的端到端链路？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mockito-stubbing.md`](./mockito-stubbing.md)（mock 语法）
- 兄弟：[`test-pyramid.md`](./test-pyramid.md)（各类测试该占多少比例）
- 跨模块：[`../spring-boot/controller-design.md`](../spring-boot/controller-design.md)（被测的 Controller 怎么定）
