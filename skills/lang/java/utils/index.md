---
name: lang-java-utils-index
description: Java 工具类用法三件事 — 自己写的工具类怎么设计 / 别造的轮子优先用哪个库 / Bean 拷贝用什么。Use when 新建 *Utils 类 / 纠结自己写还是用库 / 写对象属性拷贝代码时。
parent: ../index.md
children:
  - { name: utility-class-design, path: utility-class-design.md, tag: skill, note: 自己写工具类：final + 私有构造 + 全 static + 无状态 }
  - { name: prefer-common-libs, path: prefer-common-libs.md, tag: skill, note: 别造轮子：Hutool / Guava / Commons Lang3 常用方法对照 }
  - { name: bean-copy, path: bean-copy.md, tag: skill, note: Bean 拷贝优先 MapStruct，禁反射 BeanUtils }
when_to_descend: 写 / 评审工具类、判空判集合、对象属性拷贝相关代码时
---

# Utils · 子项索引

工具类相关拆成三个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 自己写一个 `XxxUtils` 工具类，纠结类结构怎么定 | [utility-class-design](utility-class-design.md) |
| 要判空 / 判集合空 / null 处理，纠结自己写还是用现成库 | [prefer-common-libs](prefer-common-libs.md) |
| 把一个对象的属性拷到另一个对象（DO→DTO / VO） | [bean-copy](bean-copy.md) |
