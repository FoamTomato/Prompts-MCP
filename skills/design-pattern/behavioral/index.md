---
name: design-pattern-behavioral-index
description: 常用行为型模式 — 模板方法 / 责任链 / 观察者 / 适配器。Use when 抽公共流程骨架 / 串过滤器拦截链 / 发布订阅事件 / 适配不兼容接口时。
parent: ../index.md
children:
  - { name: behavioral-template-method, path: template-method.md, tag: skill, note: 抽象骨架固定流程+钩子留扩展 }
  - { name: behavioral-chain-of-responsibility, path: chain-of-responsibility.md, tag: skill, note: 过滤器/拦截器链逐节点处理 }
  - { name: behavioral-observer, path: observer.md, tag: skill, note: 事件发布订阅解耦 ApplicationEvent }
  - { name: behavioral-adapter, path: adapter.md, tag: skill, note: 把不兼容接口适配成期望接口 }
when_to_descend: 抽公共流程骨架、串拦截链、发布事件、适配接口时
---

# Behavioral · 常用行为型模式索引

按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 多个流程步骤大体相同、只有几步不同，想抽公共骨架 | [template-method](template-method.md) |
| 一个请求要经过一串处理者（过滤/校验/拦截），可增删节点 | [chain-of-responsibility](chain-of-responsibility.md) |
| 某动作发生后要通知多个不相关的下游，想解耦发布与订阅 | [observer](observer.md) |
| 已有类的接口和你需要的不一致，想包一层转换 | [adapter](adapter.md) |
