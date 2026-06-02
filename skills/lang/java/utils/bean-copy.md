---
name: java-bean-copy
description: 对象属性拷贝（DO/DTO/VO 转换）优先用 MapStruct 编译期生成，禁用反射式 BeanUtils。Use when 写对象属性拷贝 / DO 转 DTO / 纠结用哪个 BeanUtils 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - Bean 拷贝
  - 属性拷贝
  - bean copy
  - MapStruct
  - BeanUtils
  - copyProperties
  - DO DTO 转换
effort: medium
context: inline
version: '1.0'
---
# Java · Bean 拷贝

> 本条只管「对象属性拷贝用什么」。工具类结构见 [`utility-class-design.md`](./utility-class-design.md)；通用判空选库见 [`prefer-common-libs.md`](./prefer-common-libs.md)。

## 规则

| 方式 | 用不用 | 原因 |
|------|--------|------|
| MapStruct | ✅ 首选 | 编译期生成 get/set 代码，零反射、有类型检查，字段不匹配编译期报错 |
| Apache `BeanUtils.copyProperties` | ❌ 禁用 | 反射 + 类型自动转换，最慢；参数顺序 `(dest, orig)` 与 Spring 相反，极易拷反 |
| Spring `BeanUtils.copyProperties` | ⚠️ 仅简单场景 | 反射，性能差于 MapStruct；**类型不匹配静默跳过**，字段拷不过去也不报错 |

核心理由：反射式拷贝（两个 `BeanUtils`）的失败是**静默**的 —— 字段名拼错、类型对不上时不抛异常，只是悄悄不拷，线上才发现值是 null。MapStruct 把这些问题提前到**编译期**。

> MapStruct 的 Mapper 接口写法、`@Mapping` 字段映射、与 Spring 集成详见 framework/mapstruct（该模块规约另行维护）。

## 反例

```java
// ❌ Spring 版：source/target 类型不一致时静默跳过，amount 拷不过去也不报错
BeanUtils.copyProperties(orderDO, orderVO);   // org.springframework.beans

// ❌ Apache 版：参数顺序是 (dest, orig)，与 Spring 相反，很容易拷反方向
org.apache.commons.beanutils.BeanUtils.copyProperties(orderVO, orderDO);
```

## 正例

```java
// ✅ MapStruct：接口定义映射，编译期生成实现，字段对不上直接编译失败
@Mapper(componentModel = "spring")
public interface OrderMapper {
    OrderVO toVO(OrderDO source);
}

// 调用处：拿到的是生成的实现，纯 get/set，无反射
OrderVO vo = orderMapper.toVO(orderDO);
```

## 自检

- [ ] 新拷贝逻辑用 MapStruct，而非任何 `BeanUtils.copyProperties`？
- [ ] 没有引入 Apache `commons-beanutils`（参数顺序反 + 性能差）？
- [ ] 残留的 Spring `BeanUtils` 仅用于字段完全同名同类型的简单场景，且知道它静默失败的坑？
- [ ] DO/DTO/VO 之间的转换走统一的 Mapper，而非各处手写散落？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`utility-class-design.md`](./utility-class-design.md)（别自己写一个反射拷贝工具类）
- 兄弟：[`prefer-common-libs.md`](./prefer-common-libs.md)（同样是"别造轮子"原则的应用）
