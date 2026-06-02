---
name: behavioral-adapter
description: 适配器模式 — 把已有类的接口包一层转换成调用方期望的接口，对接第三方/旧代码而不改其源码。Use when 已有类接口与所需不一致 / 对接多家第三方想统一接口 / 包装遗留代码时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 适配器
  - Adapter
  - 接口适配
  - 第三方对接
  - 统一接口
effort: medium
context: inline
version: '1.0'
---
# Behavioral · 适配器

> 适配器属于结构型模式，因常与行为型一起用而归在本模块；它只管「接口转换」。

## 何时用

| 信号 | 用适配器 |
|------|---------|
| 已有类功能合用，但**接口签名**和你需要的不一致 | ✅ |
| 对接多家第三方（多家短信/支付），想对上层暴露**统一接口** | ✅ |
| 包装无法修改源码的旧代码/SDK | ✅ |
| 能直接改目标类的接口 | ❌ 直接改，别套适配器 |

## 正例：统一第三方接口

```java
// 上层期望的统一接口
public interface SmsSender { void send(String phone, String content); }

// 第三方 SDK 接口长这样（不能改）
class AliyunSdk { void dispatch(String mobile, String text, String sign) { } }

// 适配器：把 AliyunSdk 适配成 SmsSender
public class AliyunSmsAdapter implements SmsSender {
    private final AliyunSdk sdk = new AliyunSdk();
    @Override
    public void send(String phone, String content) {
        sdk.dispatch(phone, content, "【签名】");   // 转换参数/补默认值
    }
}
// 换腾讯云只加 TencentSmsAdapter，上层只依赖 SmsSender 不变
```

## 反例：上层直接耦合第三方

```java
// ❌ 业务代码直接调第三方 SDK，换供应商要改所有调用处
public void notifyUser(String phone) {
    AliyunSdk sdk = new AliyunSdk();
    sdk.dispatch(phone, "...", "【签名】");   // 全项目散落这种调用
}
```

## 自检

- [ ] 适配器实现的是**调用方期望的接口**，内部委托给被适配对象？
- [ ] 上层只依赖统一接口，不直接 import 第三方 SDK 类？
- [ ] 多家第三方各自一个适配器，新增供应商不改上层？
- [ ] 接口本就能改时没有多此一举套适配器？

## 相关

- 父：[`./index.md`](./index.md)
- 选实现：[`../strategy/index.md`](../strategy/index.md) · [`../factory/index.md`](../factory/index.md)（适配后用工厂/策略选具体适配器）
