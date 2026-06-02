---
name: framework-testing-index
description: Java 测试约定 — JUnit5 写法 / Mockito 隔离依赖 / Spring Boot 测试分层 / 测试金字塔四个独立决策点。Use when 写单元测试 / mock 外部依赖 / 选 @SpringBootTest 还是 @WebMvcTest / 定测试分层策略时。
parent: ../index.md
children:
  - { name: testing-junit5-basics, path: junit5-basics.md, tag: skill, note: "JUnit5 写法：@Test / @BeforeEach / @ParameterizedTest / assertThrows / assertAll" }
  - { name: testing-mockito-stubbing, path: mockito-stubbing.md, tag: skill, note: "Mockito：@Mock / @InjectMocks / when-thenReturn / verify 隔离外部依赖" }
  - { name: testing-spring-boot-test, path: spring-boot-test.md, tag: skill, note: "@SpringBootTest 集成 vs @WebMvcTest controller 层 vs 纯单测，何时用哪个" }
  - { name: testing-test-pyramid, path: test-pyramid.md, tag: skill, note: 测试金字塔分层比例与反模式（依赖外部资源、mock 一切） }
when_to_descend: 写 / 改 *.java 的测试代码：写 JUnit5 用例、用 Mockito mock 依赖、选 Spring 测试切片、规划测试分层比例时。
---

# Testing · Java 测试约定索引

四个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 写测试方法、断言、参数化、断言异常 | [junit5-basics](junit5-basics.md) |
| mock 掉 service/dao 等外部依赖做隔离单测 | [mockito-stubbing](mockito-stubbing.md) |
| 纠结起不起 Spring 容器、用哪个测试注解 | [spring-boot-test](spring-boot-test.md) |
| 规划单测/集成/E2E 的比例、避免测试反模式 | [test-pyramid](test-pyramid.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../spring-boot/index.md`](../spring-boot/index.md)
- 相关：[`../../lang/java/error-handling/index.md`](../../lang/java/error-handling/index.md)
