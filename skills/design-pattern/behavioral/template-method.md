---
name: behavioral-template-method
description: 模板方法模式 — 抽象类用 final 方法固定流程骨架，把可变步骤留成抽象/钩子方法由子类实现。Use when 多个流程步骤大体相同只差几步 / 想抽公共骨架防子类改流程顺序时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 模板方法
  - Template Method
  - 抽象骨架
  - 钩子方法
  - 流程固化
effort: medium
context: inline
version: '1.0'
---
# Behavioral · 模板方法

## 何时用

| 信号 | 用模板方法 |
|------|-----------|
| 多个处理流程**步骤顺序一致**，只有个别步骤实现不同 | ✅ |
| 想强制子类不能改流程顺序，只能填空 | ✅（骨架方法 `final`） |
| 流程步骤完全不同 / 需运行时切换整套算法 | ❌ 用策略 |

## 正例：固定骨架 + 抽象步骤 + 钩子

```java
public abstract class ImportTask {
    // 骨架方法 final：子类不能改流程顺序
    public final void run(File file) {
        List<Row> rows = parse(file);   // 可变步骤：子类实现
        validate(rows);                 // 可变步骤
        save(rows);                     // 可变步骤
        afterSave();                    // 钩子：默认空，子类可选覆盖
    }

    protected abstract List<Row> parse(File file);
    protected abstract void validate(List<Row> rows);
    protected abstract void save(List<Row> rows);
    protected void afterSave() { /* 默认不做，钩子 */ }
}

public class UserImportTask extends ImportTask {
    protected List<Row> parse(File f) { /* 解析 CSV */ return ...; }
    protected void validate(List<Row> rows) { /* 校验 */ }
    protected void save(List<Row> rows) { /* 落库 */ }
    @Override protected void afterSave() { /* 发通知 */ }
}
```

## 反例：复制整段流程

```java
// ❌ 每种导入都把「解析-校验-保存-通知」整套复制一遍
public class UserImportTask {
    public void run(File f) { /* 同样 4 步，重复 */ }
}
public class OrderImportTask {
    public void run(File f) { /* 又抄一遍，骨架改了要改 N 处 */ }
}
```

## 自检

- [ ] 骨架方法（定义流程顺序的那个）是 `final`，子类不能篡改顺序？
- [ ] 可变步骤是 `abstract`，可选扩展点用「默认空实现」的钩子方法？
- [ ] 子类只填空、不重复整段流程？
- [ ] 若是「整套算法替换」而非「填空」，改用了策略而非模板方法？

## 相关

- 父：[`./index.md`](./index.md)
- 对比：[`../strategy/index.md`](../strategy/index.md)（替换整套算法 vs 填空骨架）
- 流程编排：[`../../lang/java/pipeline-style/orchestration-method.md`](../../lang/java/pipeline-style/orchestration-method.md)
