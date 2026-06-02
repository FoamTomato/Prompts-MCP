---
name: testing-mockito-stubbing
description: Mockito 隔离依赖 — @Mock 造替身、@InjectMocks 注入被测类、when-thenReturn 打桩、verify 校验交互。Use when 单测要 mock service/dao 等外部依赖 / 打桩返回值 / 验证方法被调用时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 模拟对象
  - Mockito
  - '@Mock'
  - '@InjectMocks'
  - when().thenReturn()
  - verify
effort: medium
context: inline
version: '1.0'
---
# Mockito · 打桩与依赖隔离

> 本条只管「怎么造替身、打桩、验交互」。测试方法/断言本身见 [`junit5-basics.md`](./junit5-basics.md)；该不该起 Spring 见 [`spring-boot-test.md`](./spring-boot-test.md)。

## 规则

| 维度 | 约定 |
|------|------|
| 开启扩展 | 类上加 `@ExtendWith(MockitoExtension.class)`，让 `@Mock`/`@InjectMocks` 生效 |
| 造替身 | 被测类**依赖的协作者**用 `@Mock`（DAO、远程 client、第三方 service） |
| 注入 | 被测类本身用 `@InjectMocks`，Mockito 自动把上面的 `@Mock` 注进去 |
| 打桩 | `when(mock.方法(参数)).thenReturn(值)`；抛异常用 `thenThrow`；参数不确定用 `any()` |
| 验交互 | `verify(mock).方法(...)` 校验被调；次数用 `times(n)`/`never()` |
| 边界 | 只 mock **外部依赖**，被测对象本身**真实运行**，否则等于没测 |

## 正例

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock UserDao userDao;            // 外部依赖：造替身
    @InjectMocks OrderService service; // 被测类：真实运行，注入上面的 mock

    @Test
    void placeOrder_shouldFail_whenUserMissing() {
        // 打桩：约定 mock 的返回
        when(userDao.findById(1L)).thenReturn(null);

        assertThrows(BizException.class,
            () -> service.placeOrder(1L));

        // 验交互：确认查过库、且没继续往下扣款
        verify(userDao).findById(1L);
        verify(userDao, never()).deductBalance(anyLong(), any());
    }
}
```

## 反例

```java
// ❌ 把被测对象自己也 mock 了，when 直接桩死返回值 —— 测的是 mock，不是真实逻辑
@Mock OrderService service;          // 错！被测类不该 mock
@Test
void bad() {
    when(service.placeOrder(1L)).thenReturn("ok");
    assertEquals("ok", service.placeOrder(1L)); // 永远过，毫无意义
}
```

❌ 用 `@Spy` 包真实对象又到处打桩，搞不清哪是真哪是假。
❌ 对没打桩的 mock 方法依赖其默认返回（对象返 null、int 返 0）却不自知，引发 NPE。

## 自检

- [ ] 类上有 `@ExtendWith(MockitoExtension.class)`？
- [ ] 只 mock 外部协作者，被测类用 `@InjectMocks` 真实跑？
- [ ] 打桩覆盖了用例会走到的所有 mock 调用，没漏导致返默认值？
- [ ] 需要确认副作用的地方用 `verify` 校验交互（含 `never()`）？
- [ ] 没有「mock 被测类自身」这种自欺用例？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`junit5-basics.md`](./junit5-basics.md)（测试方法与断言）
- 兄弟：[`spring-boot-test.md`](./spring-boot-test.md)（纯单测 vs 起 Spring 切片）
