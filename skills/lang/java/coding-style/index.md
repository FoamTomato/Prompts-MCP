---
name: lang-java-coding-style-index
description: Java 编码规范六件事 — 禁魔法值 / Optional 用法 / 防 NPE / equals-hashCode / 字符串处理 / Lombok 约定。Use when 写 Java 业务代码 / 评审编码细节的 PR / 排查 NPE 或哈希失效时。
parent: ../index.md
children:
  - { name: no-magic-value, path: no-magic-value.md, tag: skill, note: 散落字面量抽常量/枚举/配置 }
  - { name: optional-usage, path: optional-usage.md, tag: skill, note: Optional 只用于返回值、禁裸 get、orElse vs orElseGet }
  - { name: null-safety, path: null-safety.md, tag: skill, note: 防 NPE：requireNonNull、返回空集合、@Nullable、Objects.equals }
  - { name: equals-hashcode, path: equals-hashcode.md, tag: skill, note: equals/hashCode 成对重写、Objects.hash、与 compareTo 一致 }
  - { name: string-handling, path: string-handling.md, tag: skill, note: StringBuilder 拼接、equals 比较、isEmpty/isBlank }
  - { name: lombok-usage, path: lombok-usage.md, tag: skill, note: "@Data 慎用，推荐 @Getter/@Builder/@RequiredArgsConstructor" }
when_to_descend: 写 / 评审任意 .java 业务代码的编码细节时
---

# Coding Style · 子项索引

编码规范拆成六个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 代码里出现裸数字 / 字符串字面量，想抽常量 / 枚举 / 配置 | [no-magic-value](no-magic-value.md) |
| 方法返回值可能没有，纠结 Optional 怎么用（get / orElse / ifPresent） | [optional-usage](optional-usage.md) |
| 防 NPE：校验入参、返回集合该不该为 null、可空标注、安全比较 | [null-safety](null-safety.md) |
| 重写 equals / 把对象放进 HashSet / HashMap key | [equals-hashcode](equals-hashcode.md) |
| 拼接、比较字符串，或判断字符串是否为空 | [string-handling](string-handling.md) |
| 给类加 Lombok 注解（@Data / @Builder / @Getter / 构造器注入） | [lombok-usage](lombok-usage.md) |

## 相关

- 父：[`../index.md`](../index.md)
- 平行模块：[`../error-handling/index.md`](../error-handling/index.md) · [`../naming/index.md`](../naming/index.md)
- 跨维度：[`../../../habit/code-quality/index.md`](../../../habit/code-quality/index.md)（跨语言代码质量通则）
