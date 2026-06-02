---
name: grpc-four-call-types
description: gRPC 四种调用方式 — 一元 / 服务端流 / 客户端流 / 双向流，及各自适用场景与选型。Use when 定义 rpc 方法 / 选一元还是流式 / 设计推送或上传接口时。
parent: ./index.md
paths:
- '*.java'
- '*.proto'
triggers:
  keywords:
  - 流式调用
  - 服务端流
  - 双向流
  - stream
  - StreamObserver
  - unary
effort: medium
context: inline
version: '1.0'
---
# gRPC · 四种调用方式与选型

> 本条只管「选哪种调用方式」。message/字段怎么定义见 [`proto-definition.md`](./proto-definition.md)；超时与错误见 [`error-and-deadline.md`](./error-and-deadline.md)。

## 规则

| 调用方式 | proto 写法 | 适用场景 |
|---------|-----------|---------|
| 一元 unary | `rpc M(Req) returns (Resp)` | 普通请求-响应：查询、单次写。默认首选 |
| 服务端流 server-streaming | `rpc M(Req) returns (stream Resp)` | 一次请求、多条结果陆续返回：大结果集分批、订阅推送、进度上报 |
| 客户端流 client-streaming | `rpc M(stream Req) returns (Resp)` | 多条上行、单次汇总返回：批量/分片上传、客户端聚合后服务端算一次 |
| 双向流 bidirectional | `rpc M(stream Req) returns (stream Resp)` | 长连接双向实时交互：聊天、协同、实时行情、心跳 |

> 选型口诀：**默认用一元**；只在「结果太大/要持续推/要长连双向」时才上流式 —— 流式更复杂（背压、半关闭、错误中途）。

## 正例

```proto
service OrderService {
  rpc GetById(GetByIdReq) returns (OrderDTO);              // 一元
  rpc ListByDay(ListReq) returns (stream OrderDTO);        // 服务端流：大结果集分批
  rpc Import(stream OrderDTO) returns (ImportResult);      // 客户端流：批量上传
  rpc Sync(stream Event) returns (stream Event);           // 双向流：实时同步
}
```

```java
// 服务端流：逐条 onNext，结束 onCompleted
@Override
public void listByDay(ListReq req, StreamObserver<OrderDTO> obs) {
    orderRepo.streamByDay(req.getDay()).forEach(o -> obs.onNext(toDTO(o)));
    obs.onCompleted();
}
```

## 反例

❌ 用一元接口返回十万条的大 list：单条响应体过大，反序列化与内存峰值爆炸 → 应改服务端流分批。

❌ 用轮询一元接口模拟实时推送：高频空轮询浪费连接与 CPU → 实时推送用服务端流或双向流。

❌ 简单查询硬上双向流：徒增半关闭/背压/错误处理复杂度，得不偿失。

## 自检

- [ ] 普通请求-响应优先用了一元，没有过度流式化？
- [ ] 大结果集 / 持续推送用了服务端流？
- [ ] 批量上传 / 客户端聚合用了客户端流？
- [ ] 长连双向实时交互才用双向流？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`proto-definition.md`](./proto-definition.md)（message/字段定义）
- 兄弟：[`error-and-deadline.md`](./error-and-deadline.md)（流式中途出错与超时）
- 兄弟：[`grpc-vs-rest-dubbo.md`](./grpc-vs-rest-dubbo.md)（要不要用 gRPC）
