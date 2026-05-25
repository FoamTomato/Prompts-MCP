---
name: java-controller-thin
description: Spring Controller 薄壳
parent: ./index.md
paths:
  - "*.java"
triggers:
  keywords: ["@RestController", Controller]
effort: medium
context: inline
version: "1.0"
---

# Java · Controller 薄

## 规则

Spring Controller 只做：参数绑定 → 调 Service → 返回响应。**禁业务逻辑、禁直接查 DB**。

## 模板

```java
@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService orderService;

    @PostMapping
    public ResponseEntity<OrderVo> create(@Valid @RequestBody CreateOrderDto dto,
                                          @AuthenticationPrincipal User user) {
        OrderVo result = orderService.create(dto, user.getId());
        return ResponseEntity.ok(result);
    }

    @GetMapping("/{id}")
    public ResponseEntity<OrderVo> get(@PathVariable Long id) {
        return ResponseEntity.ok(orderService.findById(id));
    }
}
```

## 反例

```java
// ❌ Controller 写业务逻辑
@PostMapping
public Order create(@RequestBody CreateOrderDto dto) {
    User user = userRepository.findById(dto.getUserId()).orElseThrow();
    if (user.getBalance() < dto.getAmount()) {
        throw new BusinessException("余额不足");
    }
    Order order = new Order();
    order.setUserId(user.getId());
    order.setAmount(dto.getAmount());
    return orderRepository.save(order);
}

// ✅ 业务下沉到 Service
@PostMapping
public OrderVo create(@RequestBody @Valid CreateOrderDto dto,
                      @AuthenticationPrincipal User user) {
    return orderService.create(dto, user.getId());
}
```

## 异常映射

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorVo> handle(BusinessException e) {
        return ResponseEntity.status(e.getCode())
            .body(new ErrorVo(e.getMessage(), e.getCode()));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorVo> handle(Exception e) {
        log.error("unhandled", e);
        return ResponseEntity.status(500).body(new ErrorVo("服务繁忙", 500));
    }
}
```

## 自检

- [ ] Controller 方法 ≤ 5 行？
- [ ] 无 `@Autowired Repository` 直接注入？
- [ ] `@Valid` 触发参数校验？
- [ ] 异常统一在 `@RestControllerAdvice`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`service-orchestration.md`](./service-orchestration.md)

