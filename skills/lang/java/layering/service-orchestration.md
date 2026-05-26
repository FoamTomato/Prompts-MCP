---
name: java-service-orchestration
description: '语言规则 · java: Spring Service 编排层'
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - '@Service'
  - Service
  - 编排层
effort: medium
context: inline
version: '1.0'
---
# Java · Service 编排

## 规则

Service 负责**业务流程编排**：参数校验 → 加载领域对象 → 调用领域方法 → 持久化。**不直接处理 HTTP / 不写 SQL**。

## 模板

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class OrderService {

    private final OrderRepository orderRepository;
    private final UserRepository userRepository;
    private final PaymentService paymentService;

    @Transactional
    public OrderVo create(CreateOrderDto dto, Long userId) {
        // 校验
        OrderValidator.validateCreate(dto);

        // 加载领域对象
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new BusinessException("用户不存在", 404));

        // 领域规则
        if (!user.canPlaceOrder(dto.getAmount())) {
            throw new BusinessException("余额不足", 400);
        }

        // 编排
        Order order = Order.from(dto, user);
        orderRepository.save(order);

        // 后置操作
        paymentService.deduct(user.getId(), dto.getAmount());

        log.info("create order id={} userId={} amount={}", order.getId(), userId, dto.getAmount());

        // 规整输出
        return OrderConverter.toVo(order);
    }
}
```

## 注释驱动

每个步骤前一行中文注释，读注释即懂全流程：

```java
public OrderVo submit(SubmitDto dto) {
    // 1. 参数与权限校验
    OrderValidator.validateSubmit(dto);

    // 2. 加载购物车并校验库存
    Cart cart = loadCartWithStockCheck(dto.getCartId());

    // 3. 计算最终价格（含优惠、积分）
    Price price = priceCalculator.calculate(cart, dto.getCoupon(), dto.getPoints());

    // 4. 扣库存
    inventoryService.deduct(cart.getItems());

    // 5. 生成订单
    Order order = orderFactory.create(cart, price, dto);
    orderRepository.save(order);

    // 6. 触发支付
    paymentService.charge(order);

    return OrderConverter.toVo(order);
}
```

## 反例

```java
// ❌ Service 写 SQL
@Service
public class OrderService {
    @PersistenceContext EntityManager em;

    public List<Order> getActiveOrders(Long userId) {
        return em.createQuery("SELECT o FROM Order o WHERE ...")
                 .getResultList();
    }
}

// ✅ 通过 Repository
return orderRepository.findActiveByUserId(userId);
```

## @Transactional 边界

```java
// ✅ 跨多表写
@Transactional
public OrderVo create(...) { ... }

// ❌ 只读不要事务（性能损耗）
@Transactional(readOnly = true)
public OrderVo findById(Long id) {
    return orderRepository.findById(id)
        .map(OrderConverter::toVo)
        .orElseThrow();
}
```

## 自检

- [ ] Service 不直接写 SQL（通过 Repository）？
- [ ] 步骤间有中文注释？
- [ ] 复杂转换抽到 `*Converter`？
- [ ] 复杂校验抽到 `*Validator`？
- [ ] `@Transactional` 边界合理？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`controller-thin.md`](./controller-thin.md)
- 配套：[`../../../design-pattern/ddd-layering/service-orchestration.md`](../../../design-pattern/ddd-layering/service-orchestration.md)

