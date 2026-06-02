---
name: testing-test-pyramid
description: 测试金字塔分层比例 — 单元测试最多、集成测试居中、E2E 最少，及常见反模式（测试依赖外部 DB/网络、mock 一切测了个寂寞）。Use when 规划测试比例 / 评审测试质量 / 纠结某逻辑该写哪层测试时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 测试金字塔
  - 测试分层
  - test pyramid
  - 测试反模式
  - E2E 测试
  - 测试覆盖率
effort: medium
context: inline
version: '1.0'
---
# 测试金字塔 · 分层比例与反模式

> 本条只管「哪类测试该占多少、哪些是反模式」。具体注解选型见 [`spring-boot-test.md`](./spring-boot-test.md)；mock 语法见 [`mockito-stubbing.md`](./mockito-stubbing.md)。

## 三层比例（自下而上，数量递减）

| 层 | 占比 | 特征 | 本库对应 |
|----|------|------|---------|
| 单元测试 | **最多（底座）** | 快、稳、隔离，覆盖分支与边界 | JUnit5 + Mockito 纯单测 |
| 集成测试 | 居中 | 验组件协作（DB/MQ/Web 切片），慢一些 | `@WebMvcTest`/`@DataJpaTest`/`@SpringBootTest` |
| E2E 测试 | **最少（塔尖）** | 真实环境跑完整业务流，最慢最脆 | 仅核心链路冒烟 |

核心原则：**越往上越慢越脆，数量越少**；能用下层覆盖的逻辑就别往上推。

## 反模式

| 反模式 | 为什么坏 | 改法 |
|--------|----------|------|
| 单测依赖真实 DB/网络/时钟 | 慢、不稳、CI 受环境牵连，本质是集成测试伪装成单测 | 外部依赖用 Mockito mock；持久层用内存库切片 |
| mock 一切（连被测对象都桩死） | 测的全是 mock 行为，逻辑改了测试照样绿，「测了个寂寞」 | 只 mock 外部依赖，被测对象真实运行 |
| 倒金字塔 / 冰淇淋（E2E 巨多、单测寥寥） | 跑得慢、定位难、动一行挂一片 | 把校验下沉到单测，E2E 只留关键流 |
| 唯覆盖率论（堆无断言用例刷百分比） | 覆盖率高但没真正断言，假安全感 | 关注分支/边界与有效断言，而非数字 |

## 正例（分层归位）

```text
金额计算、状态机流转、参数校验分支  → 单元测试（多，Mockito 隔离）
Controller 路由 + service + DAO 串通  → 切片集成（@WebMvcTest / @DataJpaTest，少）
"下单→支付→发货"完整业务流            → E2E 冒烟（极少，核心链路）
```

## 反例

```java
// ❌ 名为单测，实则连真实 MySQL —— 没数据库就挂，慢且不稳
@Test
void findUser() {
    UserDao dao = new UserDaoImpl(realDataSource); // 连真库
    assertNotNull(dao.findById(1L));
}
```

❌ 写了 100 个用例全是 `assertNotNull(obj)`，覆盖率好看但没断言真正行为。

## 自检

- [ ] 单测占大头，且不碰真实 DB/网络/时钟？
- [ ] 集成测试只在「验组件协作」时用，数量克制？
- [ ] E2E 只覆盖少量核心业务流？
- [ ] 没有「mock 一切」导致用例永远绿的假测试？
- [ ] 不靠堆无断言用例刷覆盖率？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`spring-boot-test.md`](./spring-boot-test.md)（各层用哪个注解）
- 兄弟：[`mockito-stubbing.md`](./mockito-stubbing.md)（mock 外部依赖而非一切）
