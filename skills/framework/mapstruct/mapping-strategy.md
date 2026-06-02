---
name: mapstruct-mapping-strategy
description: 用 unmappedTargetPolicy=ERROR 强制显式映射防漏字段，配空值策略与 @Named 自定义类型转换。Use when 配置 MapStruct 全局策略 / 防止漏映射字段 / 处理 null / 写自定义类型转换时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 映射策略
  - 漏字段
  - unmappedTargetPolicy
  - nullValueMappingStrategy
  - '@Named'
  - 自定义转换
effort: medium
context: inline
version: '1.0'
---
# MapStruct · 映射策略

> 本条只管「全局策略与自定义类型转换」。字段级 `@Mapping` 写法见 [`field-mapping.md`](./field-mapping.md)；Mapper 接口定义见 [`mapper-definition.md`](./mapper-definition.md)。

## 规则

| 目的 | 配置 |
|------|------|
| 目标有字段没被映射就**编译报错**（防漏字段） | `@Mapper(unmappedTargetPolicy = ReportingPolicy.ERROR)` |
| 入参为 null 时返回空对象而非 null | `nullValueMappingStrategy = RETURN_DEFAULT` |
| 自定义某类型的转换逻辑 | 写带 `@Named` 的方法，字段上 `qualifiedByName` 引用 |

`unmappedTargetPolicy = ERROR` 是最值钱的一条：新增了目标字段却忘了映射，编译期直接红，而不是线上拿到一个 null。建议设为团队默认。

## 正例

```java
@Mapper(
    componentModel = "spring",
    unmappedTargetPolicy = ReportingPolicy.ERROR,            // 漏映射 → 编译失败
    nullValueMappingStrategy = NullValueMappingStrategy.RETURN_DEFAULT
)
public interface AccountMapper {

    @Mapping(source = "status", target = "statusText", qualifiedByName = "statusToText")
    AccountVO toVO(AccountDO source);

    // 自定义类型转换：状态码 → 文案，多个 Mapper 可复用
    @Named("statusToText")
    default String statusToText(Integer status) {
        return status != null && status == 1 ? "启用" : "停用";
    }
}
```

## 反例

```java
// ❌ 用默认 IGNORE 策略：新增 target 字段忘了映射，编译照过，线上才发现是 null
@Mapper(componentModel = "spring")  // 没设 unmappedTargetPolicy
public interface AccountMapper {
    AccountVO toVO(AccountDO source);
}
```

## 自检

- [ ] Mapper 设了 `unmappedTargetPolicy = ReportingPolicy.ERROR`，漏字段会编译失败？
- [ ] null 入参的行为是有意选择（默认 null / 还是 `RETURN_DEFAULT`），不是放任默认？
- [ ] 自定义类型转换用 `@Named` + `qualifiedByName`，而非塞进 expression？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`field-mapping.md`](./field-mapping.md)（字段级 @Mapping 写法）
- 兄弟：[`mapper-definition.md`](./mapper-definition.md)（Mapper 接口定义）
- 兄弟：[`anti-patterns.md`](./anti-patterns.md)（枚举映射与反模式）
