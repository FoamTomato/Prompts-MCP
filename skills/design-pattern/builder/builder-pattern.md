---
name: builder-pattern
description: 建造者模式 — 多参对象用链式 Builder 替代望远镜构造器/裸 setter，优先 Lombok @Builder 生成。Use when 构造参数过多或可选 / 需要不可变对象 / 纠结何时上 Builder 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 建造者
  - Builder
  - 链式构造
  - 不可变对象
  - 望远镜构造器
effort: medium
context: inline
version: '1.0'
---
# Builder · 建造者模式

## 何时用 Builder

| 信号 | 用 Builder |
|------|-----------|
| 构造参数 ≥4 个，或可选参数多 | ✅ 避免望远镜构造器 |
| 需要不可变对象（字段 final） | ✅ 构造后不可变 |
| 多个 `String` 参数顺序易写错 | ✅ 链式 + 命名清晰 |
| 参数 1-2 个、全必填 | ❌ 直接构造器即可 |

## 正例：Lombok @Builder（首选）

```java
@Builder
@Getter
public class HttpRequest {
    private final String url;            // 必填
    private final String method;
    @Builder.Default
    private final int timeoutMs = 3000;  // 给默认值
    private final Map<String, String> headers;
}

// 调用：可读、顺序无关、可省略可选项
HttpRequest req = HttpRequest.builder()
        .url("https://api.example.com")
        .method("POST")
        .timeoutMs(5000)
        .build();
```

## 正例：手写 Builder（需在 build() 做校验时）

```java
public static class Builder {
    private String url;
    private int timeoutMs = 3000;
    public Builder url(String url) { this.url = url; return this; }
    public Builder timeoutMs(int t) { this.timeoutMs = t; return this; }
    public HttpRequest build() {
        Objects.requireNonNull(url, "url required");   // 集中校验
        return new HttpRequest(this);
    }
}
```

## 反例：望远镜构造器 / 裸 setter

```java
// ❌ 望远镜构造器：参数顺序难记，可选项要写一堆重载
new HttpRequest("url", "POST", 3000, null, null, false);

// ❌ 全 setter：构造期间是半成品状态，无法做成不可变
HttpRequest r = new HttpRequest();
r.setUrl("url"); r.setMethod("POST");  // 忘了 setUrl 也能编译通过
```

## 自检

- [ ] 参数多/可选多时用了 Builder，而不是望远镜构造器？
- [ ] 优先 `@Builder` 生成，仅在需要 build() 校验时才手写？
- [ ] 不可变需求下字段 `final`、无 setter？
- [ ] 必填项在 build() 或构造器里做了非空校验？
- [ ] 参数仅 1-2 个全必填时没有过度套 Builder？

## 相关

- 父：[`./index.md`](./index.md)
- 对象创建相关：[`../factory/index.md`](../factory/index.md)（选哪个对象 vs 怎么装配对象）
