---
name: mapstruct-anti-patterns
description: 对象转换的反模式 — 别用反射 BeanUtils.copyProperties、别手写 getter/setter 搬运，枚举映射用 @ValueMapping。Use when 评审对象转换代码 / 看到 BeanUtils 或手写搬运 / 映射枚举时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 转换反模式
  - 枚举映射
  - BeanUtils
  - copyProperties
  - '@ValueMapping'
  - getter setter 搬运
effort: medium
context: inline
version: '1.0'
---
# MapStruct · 转换反模式

> 本条只管「别这么干」。Mapper 接口定义见 [`mapper-definition.md`](./mapper-definition.md)；字段映射见 [`field-mapping.md`](./field-mapping.md)。

## 规则

| 反模式 | 问题 | 改用 |
|--------|------|------|
| `BeanUtils.copyProperties` | 反射慢；类型/字段对不上**静默漏拷**，线上才发现是 null | MapStruct Mapper |
| 手写 `vo.setX(do.getX())` 逐行搬运 | 字段一多就漏、改字段两头维护、纯样板 | MapStruct 自动生成 |
| 枚举 `switch`/`if` 手写转换 | 漏枚举值无提示，新增值忘改 | `@ValueMapping` |

核心：这些写法的失败都是**静默或滞后**的（运行时才暴露），MapStruct 把它们提前到**编译期**。

## 反例

```java
// ❌ 反射拷贝：amount 类型不一致时静默跳过，不报错
BeanUtils.copyProperties(orderDO, orderVO);

// ❌ 手写搬运：字段一多必漏，新增字段两头改
orderVO.setId(orderDO.getId());
orderVO.setName(orderDO.getName());
// ... 漏了 orderVO.setAmount(...)，编译照过

// ❌ 手写枚举 switch：新增 PAID 枚举值忘了加分支，落到 default
String text = switch (status) {
    case CREATED -> "已创建";
    default -> "未知";
};
```

## 正例

```java
@Mapper(componentModel = "spring", unmappedTargetPolicy = ReportingPolicy.ERROR)
public interface OrderMapper {

    OrderVO toVO(OrderDO source);   // ✅ 自动生成，漏字段编译失败

    // ✅ 枚举映射：@ValueMapping 处理特殊值，其余按名匹配；漏值编译期可控
    @ValueMapping(source = "UNKNOWN", target = MappingConstants.NULL)
    OrderStatusVO toVO(OrderStatusDO status);
}
```

## 自检

- [ ] 没有新增 `BeanUtils.copyProperties`（Spring 或 Apache 版均不用）？
- [ ] 没有逐行手写 `set/get` 搬运对象，而是走 Mapper？
- [ ] 枚举映射用 `@ValueMapping`，而非手写 switch/if？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mapper-definition.md`](./mapper-definition.md)（为什么 MapStruct 优于反射）
- 兄弟：[`field-mapping.md`](./field-mapping.md)（字段映射写法）
- 兄弟：[`mapping-strategy.md`](./mapping-strategy.md)（unmappedTargetPolicy 防漏字段）
- 拷贝选型详解：[`../../lang/java/utils/bean-copy.md`](../../lang/java/utils/bean-copy.md)
