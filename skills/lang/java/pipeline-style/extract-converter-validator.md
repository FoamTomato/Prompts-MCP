---
name: java-extract-converter-validator
description: 防 ServiceImpl 膨胀 — 数据转换抽 Converter、参数校验抽 Validator、外部调用返回值校验下沉，编排方法每类只留一行调用。Use when ServiceImpl 堆转换/校验代码 / 拆臃肿 Service / 评审职责分层时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - Converter 转换类
  - Validator 校验类
  - 结果校验
  - ServiceImpl 膨胀
  - 职责抽取
  - assembler
  - 业务校验下沉
effort: medium
context: inline
version: '1.0'
---
# Java · 抽 Converter / Validator

> 本条只管「臃肿逻辑抽到哪个专属类」。编排方法本身怎么写见 [`orchestration-method.md`](./orchestration-method.md)。

## 规则

ServiceImpl 只做**编排**，以下三类逻辑必须抽到专属类，让编排层每类只留一行调用：

| 逻辑 | 抽到 | 编排层留 |
|------|------|---------|
| DO→DTO/VO、多源聚合转换 | `XxxConverter`/`XxxConvert`（MapStruct） | 一行 `convert(...)` |
| 入参合法性校验（格式/范围/依赖） | `XxxValidator`（@Component） | 一行 `validator.validateXxx(req)` |
| 外部调用返回值校验（空判/状态断言/错误码） | `XxxValidator` 静态方法 | 一行 `XxxValidator.assertExists(...)` |

## 正例

```java
// ✅ 参数校验抽到 Validator
@Component
public class ArticleValidator {
    public void validateCreate(ArticleCreateReq req) {
        Assert.notBlank(req.getTitle(), "标题不能为空");
        Assert.isTrue(req.getWordCount() > 0, "字数必须大于 0");
    }
    // ✅ 结果校验：静态断言
    public static void assertExists(ArticleDO article, Long id) {
        if (article == null) {
            throw new BizException("文章不存在: " + id);
        }
    }
}

// 编排方法里各留一行
articleValidator.validateCreate(req);
ArticleValidator.assertExists(article, id);
```

## 反例

```java
// ❌ 转换 + 校验全堆在 ServiceImpl
public ArticleVO getArticle(Long id) {
    ArticleDO article = mapper.selectById(id);
    if (article == null) {                       // 结果校验该下沉
        throw new BizException("文章不存在: " + id);
    }
    ArticleVO vo = new ArticleVO();
    vo.setTitle(article.getTitle());             // 20 行转换该交 Converter
    // ...
}
```

## 自检

- [ ] ServiceImpl 没有 5 行以上的转换逻辑（应在 `XxxConverter`）？
- [ ] 参数校验集中在 `XxxValidator`，没散落在 ServiceImpl？
- [ ] 外部调用返回值校验（null/状态/错误码）用 Validator 静态方法，编排层只一行？
- [ ] Converter 是无状态 @Component / MapStruct 接口，不掺业务判断？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`orchestration-method.md`](./orchestration-method.md)（抽完后编排方法怎么写）
- 分层职责边界：[`../layering/index.md`](../layering/index.md)
- 转换实现：[`../../../framework/mapstruct/index.md`](../../../framework/mapstruct/index.md)
