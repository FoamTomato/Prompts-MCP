---
name: mapstruct-mapper-definition
description: 用 @Mapper(componentModel="spring") 把 Mapper 定义成可注入接口，编译期生成实现替代手写转换/BeanUtils。Use when 新建 MapStruct Mapper / 注入 Mapper / 纠结 MapStruct 还是手写转换时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 映射器接口
  - 对象映射
  - '@Mapper'
  - componentModel
  - MapStruct
  - mapper 注入
effort: medium
context: inline
version: '1.0'
---
# MapStruct · Mapper 接口定义

> 本条只管「Mapper 接口怎么定义、怎么被注入」。字段名对不上见 [`field-mapping.md`](./field-mapping.md)；映射策略见 [`mapping-strategy.md`](./mapping-strategy.md)。

## 规则

| 要点 | 做法 |
|------|------|
| 让 Mapper 能被 Spring 注入 | `@Mapper(componentModel = "spring")`，生成的实现自动注册为 Bean |
| Mapper 是接口 | 只写方法签名，实现由 MapStruct 注解处理器编译期生成 |
| 反向映射 | 在同一接口加一条反向方法即可，无需额外配置 |
| 集合映射 | 声明 `List<VO> toVOList(List<DO>)`，复用单对象方法 |

不写 `componentModel` 时默认生成的实现不是 Bean，只能用 `Mappers.getMapper(...)` 手动取，无法 `@Autowired`。Spring 项目一律用 `"spring"`。

## 正例

```java
// ✅ componentModel = "spring" → 生成实现带 @Component，可直接注入
@Mapper(componentModel = "spring")
public interface OrderMapper {

    OrderVO toVO(OrderDO source);          // 正向
    OrderDO toDO(OrderVO source);          // 反向，再加一条方法即可
    List<OrderVO> toVOList(List<OrderDO> list);  // 集合复用单对象映射
}

// 注入处：拿到的是编译期生成的纯 get/set 实现
@Service
public class OrderService {
    private final OrderMapper orderMapper;  // 构造器注入

    public OrderService(OrderMapper orderMapper) {
        this.orderMapper = orderMapper;
    }
}
```

## 为什么用 MapStruct 而非手写/BeanUtils

- **编译期生成**：实现是编译时生成的纯 `getter/setter` 代码，零反射，性能等同手写。
- **类型安全**：字段类型对不上、目标字段没映射，**编译期**就报错，不会拖到线上。
- **可读可调试**：生成的实现是普通 `.java`，能点进去看、能打断点。

## 自检

- [ ] Spring 项目的 Mapper 都加了 `componentModel = "spring"`？
- [ ] Mapper 是 interface，没有手写实现类？
- [ ] 通过 `@Autowired` / 构造器注入使用，而非 `Mappers.getMapper`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`field-mapping.md`](./field-mapping.md)（字段名/类型对不上怎么映射）
- 兄弟：[`mapping-strategy.md`](./mapping-strategy.md)（映射策略与自定义转换）
- 兄弟：[`anti-patterns.md`](./anti-patterns.md)（别再用 BeanUtils）
- 拷贝选型：[`../../lang/java/utils/bean-copy.md`](../../lang/java/utils/bean-copy.md)
