---
name: lang-java-pipeline-style-index
description: Java 业务方法的「注释驱动流水线编排」风格 — 方法即编排器 / 逻辑下沉 Converter-Validator-Utils。Use when 写 Service 业务方法 / 重构臃肿方法 / 评审方法结构时。
parent: ../index.md
children:
  - { name: orchestration-method, path: orchestration-method.md, tag: skill, note: 方法体=顺序步骤注释+每步一调用+final 中间变量+早返回 }
  - { name: extract-converter-validator, path: extract-converter-validator.md, tag: skill, note: "转换抽 Converter / 校验抽 Validator / 结果校验下沉，ServiceImpl 不膨胀" }
when_to_descend: 写或重构 Service/业务编排方法、评审方法结构是否符合团队流水线风格
---

# Pipeline Style · 注释驱动流水线编排

> 这是团队**编码风格基准**：业务方法写成"流水线编排器"，每步一注释一调用，具体逻辑下沉。
> 本仓所有 Java **Service/业务方法**的代码例子都应遵循此风格。

按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 写一个 Service 业务方法，想知道方法体怎么组织 | [orchestration-method](orchestration-method.md) |
| ServiceImpl 里堆了大段转换 / 校验代码，想抽出去 | [extract-converter-validator](extract-converter-validator.md) |

## 相关

- 父：[`../index.md`](../index.md)
- 分层职责（Controller 薄 / Service 编排 / Mapper 纯）：[`../layering/index.md`](../layering/index.md)
- 同思想的设计模式：[`../../../design-pattern/pipeline/index.md`](../../../design-pattern/pipeline/index.md)（注释驱动的 Step 编排）
- 编排里用到的工具：[`../collections/stream-api.md`](../collections/stream-api.md)（集合用 Stream）· [`../../../framework/mapstruct/index.md`](../../../framework/mapstruct/index.md)（转换用 MapStruct）· [`../utils/utility-class-design.md`](../utils/utility-class-design.md)（逻辑下沉 Utils）
