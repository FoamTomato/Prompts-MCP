---
name: testing-junit5-basics
description: JUnit5 测试写法 — @Test / @BeforeEach 生命周期、@ParameterizedTest 参数化、assertThrows / assertAll 断言。Use when 写 JUnit5 测试方法 / 做参数化用例 / 断言抛异常或批量断言时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 单元测试
  - JUnit5
  - '@Test'
  - '@ParameterizedTest'
  - assertThrows
  - assertAll
effort: medium
context: inline
version: '1.0'
---
# JUnit5 · 测试方法与断言写法

> 本条只管「一个用例怎么写、怎么断言」。mock 依赖见 [`mockito-stubbing.md`](./mockito-stubbing.md)；起不起 Spring 见 [`spring-boot-test.md`](./spring-boot-test.md)。

## 规则

| 维度 | 约定 |
|------|------|
| 包名 | 断言/注解一律用 `org.junit.jupiter.api.*`，**不要**混入 JUnit4 的 `org.junit.*` |
| 测试方法 | `@Test` 标注，方法 **无需 public**（JUnit5 允许 package-private），命名清晰描述场景 |
| 生命周期 | `@BeforeEach`/`@AfterEach` 每个用例前后跑；`@BeforeAll`/`@AfterAll` 全类一次（须 static） |
| 参数化 | 多组输入用 `@ParameterizedTest` + `@ValueSource`/`@CsvSource`/`@MethodSource`，不复制粘贴用例 |
| 断异常 | 用 `assertThrows(X.class, () -> ...)` 拿到异常对象再断言 message，**不要** try-catch+fail |
| 批量断言 | 多个相关断言用 `assertAll`，一次跑完全部、汇总失败，不在第一个失败处中断 |

## 正例

```java
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {

    Calculator calc;

    @BeforeEach
    void setUp() {           // 每个用例前重置，隔离状态
        calc = new Calculator();
    }

    @Test
    void divide_shouldThrow_whenDivisorIsZero() {
        ArithmeticException ex = assertThrows(
            ArithmeticException.class,
            () -> calc.divide(1, 0));
        assertTrue(ex.getMessage().contains("zero"));
    }

    @ParameterizedTest
    @CsvSource({"2,3,5", "0,0,0", "-1,1,0"})
    void add_shouldSum(int a, int b, int expected) {
        assertEquals(expected, calc.add(a, b));
    }

    @Test
    void user_fieldsShouldMatch() {
        User u = calc.buildUser();
        assertAll("user",                 // 一次性断完，汇总失败
            () -> assertEquals("Tom", u.getName()),
            () -> assertEquals(18, u.getAge()));
    }
}
```

## 反例

```java
// ❌ 用 try-catch + fail 断异常：冗长，还易漏掉「没抛也算过」的 bug
@Test
void divideZero() {
    try {
        calc.divide(1, 0);
        fail("should throw");
    } catch (ArithmeticException ignored) { }
}
```

❌ 三个几乎一样的用例只换输入值 —— 该用 `@ParameterizedTest`。
❌ 误 import `org.junit.Test`（JUnit4）导致 JUnit5 不识别、用例静默不跑。

## 自检

- [ ] 注解/断言都来自 `org.junit.jupiter`，没混 JUnit4？
- [ ] 多组输入用了 `@ParameterizedTest` 而非复制用例？
- [ ] 断异常用 `assertThrows` 而非 try-catch+fail？
- [ ] 同一对象的多个字段断言用 `assertAll` 汇总？
- [ ] `@BeforeEach` 里重置了共享状态，用例间互不污染？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mockito-stubbing.md`](./mockito-stubbing.md)（mock 外部依赖做隔离）
- 兄弟：[`spring-boot-test.md`](./spring-boot-test.md)（要不要起 Spring 容器）
