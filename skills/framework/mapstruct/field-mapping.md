---
name: mapstruct-field-mapping
description: 用 @Mapping 处理字段名不一致、嵌套属性、多源参数、表达式与日期格式的映射。Use when 字段名对不上 / 映射嵌套属性 / 多个入参映射到一个目标 / 格式化日期时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 字段映射
  - 嵌套属性
  - '@Mapping'
  - 多源参数
  - expression
  - dateFormat
effort: medium
context: inline
version: '1.0'
---
# MapStruct · 字段映射

> 本条只管「字段怎么对上」。Mapper 接口定义见 [`mapper-definition.md`](./mapper-definition.md)；空值/全局策略/自定义类型转换见 [`mapping-strategy.md`](./mapping-strategy.md)。

## 规则

| 场景 | 写法 |
|------|------|
| 字段名不一致 | `@Mapping(source = "userName", target = "name")` |
| 嵌套属性 | `@Mapping(source = "user.address.city", target = "city")` |
| 跳过某字段 | `@Mapping(target = "password", ignore = true)` |
| 多个入参 | 多个方法参数 + `source = "参数名.字段"` |
| 计算/拼接值 | `@Mapping(target = "x", expression = "java(...)")` |
| 日期↔字符串 | `@Mapping(target = "d", dateFormat = "yyyy-MM-dd")` |

字段名完全一致的字段**不用写** `@Mapping`，MapStruct 自动按名匹配；只为「对不上」的字段写规则。

## 正例

```java
@Mapper(componentModel = "spring")
public interface UserMapper {

    @Mapping(source = "userName", target = "name")             // 改名
    @Mapping(source = "profile.avatarUrl", target = "avatar")  // 嵌套属性
    @Mapping(target = "password", ignore = true)               // 显式跳过敏感字段
    @Mapping(target = "fullName",
             expression = "java(u.getFirstName() + u.getLastName())")  // 表达式
    @Mapping(source = "birthday", target = "birthdayText",
             dateFormat = "yyyy-MM-dd")                        // Date → String 格式化
    UserVO toVO(UserDO u);

    // 多源参数：两个入参合并成一个目标
    @Mapping(source = "user.id", target = "userId")
    @Mapping(source = "order.amount", target = "amount")
    OrderDetailVO toDetail(UserDO user, OrderDO order);
}
```

## 反例

```java
// ❌ 字段名一致还逐个写 @Mapping，纯噪声；MapStruct 本就自动按名匹配
@Mapping(source = "id", target = "id")
@Mapping(source = "name", target = "name")
UserVO toVO(UserDO u);
```

## 自检

- [ ] 只为「字段名对不上 / 嵌套 / 需跳过 / 需计算」的字段写 `@Mapping`？
- [ ] 敏感字段（密码等）用 `ignore = true` 显式跳过，而非靠名字碰巧不匹配？
- [ ] 日期与字符串互转用 `dateFormat`，而非 expression 里手写 SimpleDateFormat？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mapper-definition.md`](./mapper-definition.md)（Mapper 接口怎么定义）
- 兄弟：[`mapping-strategy.md`](./mapping-strategy.md)（漏字段报错 / 空值 / 自定义类型转换）
- 兄弟：[`anti-patterns.md`](./anti-patterns.md)（枚举映射用 @ValueMapping）
