---
name: grpc-proto-definition
description: gRPC 的 Protobuf 定义规范 — message/service 写法、字段编号不可复用、向后兼容（不删不改字段编号）。Use when 写 .proto 文件 / 改 message 字段 / 评审 proto 向后兼容时。
parent: ./index.md
paths:
- '*.java'
- '*.proto'
triggers:
  keywords:
  - 字段编号
  - 向后兼容
  - Protobuf
  - proto3
  - message
  - reserved
effort: medium
context: inline
version: '1.0'
---
# gRPC · Protobuf 定义与向后兼容

> 本条只管「.proto 怎么定义、改字段时怎么不破坏兼容」。四种调用方式见 [`four-call-types.md`](./four-call-types.md)；错误与超时见 [`error-and-deadline.md`](./error-and-deadline.md)。

## 规则

| 项 | 约定 |
|----|------|
| 语法版本 | 统一 `syntax = "proto3"`；显式 `package` + Java 用 `option java_package` / `java_multiple_files` |
| 字段编号 | 每个字段的 tag 号（`= N`）一旦发布**永久占用**：不复用、不改号、不挪用到别的字段 |
| 删字段 | 不真删，删字段名后用 `reserved N;` `reserved "name";` 占住编号，防后人复用 |
| 改字段 | 改类型/语义=破坏兼容；要变就**加新字段**用新编号，老字段标 deprecated 保留 |
| 加字段 | 加可选字段（新编号）是兼容的；老 client 忽略未知字段，缺失字段取默认值 |
| 命名 | message/enum 用 PascalCase，字段 snake_case，service 方法 PascalCase |

## 正例

```proto
syntax = "proto3";
package order.v1;
option java_package = "com.x.order.grpc";
option java_multiple_files = true;

message OrderDTO {
  int64 id = 1;
  string status = 2;
  reserved 3;                 // 旧 amount_cents 已废弃，编号永久占住
  reserved "amount_cents";
  int64 amount_minor = 4;     // 替代字段：用新编号，不改 3
}

service OrderService {
  rpc GetById(GetByIdRequest) returns (OrderDTO);
}
```

## 反例

```proto
// ❌ 把已发布的字段编号 1 改给了新字段：
// 老 client 按编号 1 反序列化会把 user_name 当成 id 读，数据错乱
message OrderDTO {
  string user_name = 1;       // 原本 id = 1
}
```

❌ 直接删掉字段又不写 `reserved`：后人新增字段时复用了同一编号，与历史数据/老节点冲突。

❌ 改字段类型（`int32 id` 改成 `string id`）当兼容升级：wire 格式不同，跨版本反序列化失败。

## 自检

- [ ] 用 `proto3` 且配了 `java_package` / `java_multiple_files`？
- [ ] 删字段时写了 `reserved` 占住编号与字段名？
- [ ] 语义变更走了「加新字段 + 新编号」，没有改动已发布字段的编号或类型？
- [ ] 新增字段用的是从未用过的编号？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`four-call-types.md`](./four-call-types.md)（一元/流式调用怎么定义）
- 兄弟：[`error-and-deadline.md`](./error-and-deadline.md)（错误码与超时）
- 兄弟：[`grpc-vs-rest-dubbo.md`](./grpc-vs-rest-dubbo.md)（要不要用 gRPC）
