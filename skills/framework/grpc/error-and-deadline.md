---
name: grpc-error-and-deadline
description: gRPC 错误处理与超时 — 用 Status code 表达错误、deadline 超时传播、每次调用必设 deadline。Use when 处理 gRPC 错误 / 设超时 / 排查 DEADLINE_EXCEEDED 时。
parent: ./index.md
paths:
- '*.java'
- '*.proto'
triggers:
  keywords:
  - 超时传播
  - 错误码
  - deadline
  - Status
  - DEADLINE_EXCEEDED
  - StatusRuntimeException
effort: medium
context: inline
version: '1.0'
---
# gRPC · 错误处理与 deadline

> 本条只管「错误怎么表达、超时怎么设与传播」。调用方式见 [`four-call-types.md`](./four-call-types.md)；message 定义见 [`proto-definition.md`](./proto-definition.md)。

## 规则

| 项 | 约定 |
|----|------|
| 错误表达 | server 端抛 `StatusRuntimeException`，用标准 `Status.Code`，**不要靠返回体里塞 errorCode** |
| 选码 | 参数错=`INVALID_ARGUMENT`、找不到=`NOT_FOUND`、无权=`PERMISSION_DENIED`、未认证=`UNAUTHENTICATED`、内部异常=`INTERNAL`、超时=`DEADLINE_EXCEEDED` |
| 错误详情 | 业务细节用 `Status.withDescription(...)`，结构化详情走 `com.google.rpc.Status` + details |
| 必设 deadline | **每次调用都必须设 deadline**（`withDeadlineAfter`），禁止无超时调用，否则线程/连接被无限占用 |
| 超时传播 | deadline 随调用链向下游透传：A→B→C 共用同一截止时刻，A 超时后 B/C 自动取消，不做无用功 |
| 取消 | 上游超时/取消会通过 `Context` 传到下游，server 端应检查 `Context.isCancelled()` 提前中止 |

## 正例

```java
// client：必设 deadline；剩余时间会随链路传播给下游
OrderDTO o = stub
    .withDeadlineAfter(2, TimeUnit.SECONDS)
    .getById(req);
```

```java
// server：用标准 Status code 表达错误，而非塞进返回体
@Override
public void getById(GetByIdReq req, StreamObserver<OrderDTO> obs) {
    Order o = repo.find(req.getId());
    if (o == null) {
        obs.onError(Status.NOT_FOUND
            .withDescription("order not found: " + req.getId())
            .asRuntimeException());
        return;
    }
    obs.onNext(toDTO(o));
    obs.onCompleted();
}
```

## 反例

```java
// ❌ 无 deadline 调用：下游卡住时本端线程被永久占用，连锁拖垮
OrderDTO o = stub.getById(req);
```

❌ 用 `Status.OK` 返回，再在 response body 里塞 `code=404`：丢失 gRPC 原生错误语义，拦截器/监控无法识别失败。

❌ server 把所有异常都包成 `INTERNAL`：client 无法区分「参数错（不该重试）」与「内部错（可重试）」。

## 自检

- [ ] 每次调用都 `withDeadlineAfter` 设了 deadline？
- [ ] 错误用标准 `Status.Code` 表达，未塞进返回体？
- [ ] 选码区分了 INVALID_ARGUMENT / NOT_FOUND / INTERNAL 等语义？
- [ ] 依赖 deadline 随链路传播，上游超时下游能被取消？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`four-call-types.md`](./four-call-types.md)（流式调用中途出错）
- 兄弟：[`proto-definition.md`](./proto-definition.md)（message 定义）
- 兄弟：[`grpc-vs-rest-dubbo.md`](./grpc-vs-rest-dubbo.md)（要不要用 gRPC）
