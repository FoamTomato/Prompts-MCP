---
name: lang-python-oop-index
description: Python 面向对象与数据类规则索引（方法类型与 property / MRO 与 super / 建模选型 / 描述符协议 / 子类钩子与元类）。Use when 设计类层次 / 选数据建模方案 / 排查多继承或属性访问问题。
parent: ../index.md
children:
  - { name: py-oop-method-types-property, path: method-types-property.md, tag: skill, note: "实例/类/静态方法 + @property" }
  - { name: py-oop-mro-super, path: mro-super.md, tag: skill, note: "MRO / super() / 组合优于继承" }
  - { name: py-oop-dataclass-vs-pydantic, path: dataclass-vs-pydantic.md, tag: skill, note: "dataclass / pydantic / attrs 建模选型" }
  - { name: py-oop-descriptor-protocol, path: descriptor-protocol.md, tag: skill, note: "__get__/__set__/__set_name__ 描述符" }
  - { name: py-oop-init-subclass-metaclass, path: init-subclass-metaclass.md, tag: skill, note: "__init_subclass__ 优先于元类 / ABC" }
when_to_descend: 设计类时纠结方法该是哪种 / 多继承调用顺序 / 该用 dataclass 还是 pydantic / 写可复用的字段对象 / 想在子类定义时做校验。
---

# Python · 面向对象与数据类 子项索引

| 你在做什么 | 进哪个 |
|-----------|-------|
| 纠结某方法该是实例 / 类 / 静态方法，或想把计算字段暴露成属性 | method-types-property |
| 多继承调用顺序不符预期，或 super() 不知怎么写、该不该继承 | mro-super |
| 新建一个数据载体，不知道选 dataclass、pydantic v2 还是 attrs | dataclass-vs-pydantic |
| 多个字段要复用同一套校验 / 惰性计算逻辑（property 背后机制） | descriptor-protocol |
| 想在子类定义那一刻做注册或校验，或在评估元类 / ABC | init-subclass-metaclass |
