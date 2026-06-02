---
name: solid-liskov-substitution
description: 里氏替换原则 LSP — 子类必须能无声替换父类而不破坏调用方预期，不可收窄入参/放宽异常/抛 UnsupportedOperation。Use when 设计继承体系 / 子类重写后行为不一致 / 评审 instanceof 判类型时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 里氏替换
  - LSP
  - 继承替换
  - 契约不变
  - Liskov Substitution
effort: medium
context: inline
version: '1.0'
---
# SOLID · 里氏替换 LSP

> 本条只管「子类能否替换父类」。接口太大导致被迫空实现见 [`interface-segregation.md`](./interface-segregation.md)。

## 规则

| 约束 | 子类不可 |
|------|---------|
| 前置条件不可收窄 | 重写方法要求比父类更严的入参 |
| 后置条件不可放宽 | 返回比父类契约更弱的结果 |
| 异常不可加码 | 抛父类契约外的异常（含 `UnsupportedOperationException`） |
| 不变式要保持 | 破坏父类承诺的状态约束 |
| 信号 | 调用方要 `instanceof` 判类型才能正确用 → 已违反 LSP |

## 正例：替换后行为一致

```java
public abstract class Shape {
    public abstract int area();   // 契约：返回非负面积
}

public class Rectangle extends Shape {
    protected int w, h;
    public int area() { return w * h; }
}

// 任何用 Shape 的地方换成 Square 都不出错
public class Square extends Shape {
    private int side;
    public int area() { return side * side; }
}
```

## 反例：子类破坏父类契约

```java
// ❌ Square 继承 Rectangle 却让 setWidth 偷偷改了 height
public class Square extends Rectangle {
    @Override public void setWidth(int w)  { this.w = w; this.h = w; }
    @Override public void setHeight(int h) { this.w = h; this.h = h; }
}
// 调用方按 Rectangle 预期 setWidth(3)+setHeight(4) 期望 area=12，实际得 16 → 替换失败

// ❌ 子类抛父类契约外的异常
public class ReadOnlyList<E> extends ArrayList<E> {
    @Override public boolean add(E e) { throw new UnsupportedOperationException(); }
}
```

## 自检

- [ ] 任何用父类的地方换成子类，调用方代码无需改、行为不破？
- [ ] 子类没有收窄入参、放宽返回、新增父类外异常？
- [ ] 没有出现 `instanceof` 判子类型才能正确工作的调用方？
- [ ] 「is-a 但行为不兼容」的关系改用组合而非继承？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`interface-segregation.md`](./interface-segregation.md)（被迫空实现也是替换坏味道）
- 兄弟：[`open-closed.md`](./open-closed.md)（多态扩展依赖可靠的替换）
