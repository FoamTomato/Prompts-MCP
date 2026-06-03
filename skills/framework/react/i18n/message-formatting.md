---
name: react-i18n-message-formatting
description: React 文案国际化:禁字符串拼接整句、复数走 ICU、数字日期交给 Intl、抽 key 禁硬编码、RTL 用逻辑属性。Use when 拼接含变量的多语言句子 / 写复数分支 / 按 locale 格式化数字日期货币 / 支持阿拉伯语希伯来语 RTL。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - i18next
  - FormatJS
  - ICU plural
  - 占位符模板
  - 复数形式
  - message key
  - RTL 布局
  - margin-inline-start
  - 文案硬编码
effort: medium
context: inline
version: '1.0'
---
# React · 国际化文案格式化

## 规则

决策点:文案怎么组合决定能否被翻译。

| 场景 | 反模式 | 正解 |
|------|--------|------|
| 含变量的句子 | `t('hi') + name + t('welcome')` 拼接 | 整句一个 key,变量用占位符 `{name}` |
| 单复数 | `count > 1 ? t('items') : t('item')` | ICU plural,交给 i18next/FormatJS 选形 |
| 数字 / 货币 / 百分比 | 手写正则加逗号、手拼 `¥` | `Intl.NumberFormat`,见 number/format.md |
| 日期 / 时间 | 手拼 `YYYY-MM-DD` 字符串 | `Intl.DateTimeFormat` / dayjs locale |
| 散落字面量 | 组件里写死中文 | 抽 message key 进资源文件 |

语序按语言变,拼接必错;复数形随语言不同(英 2 形 one/other、波兰 3 形 one/few/many、阿拉伯 6 形 zero/one/two/few/many/other),只能由 ICU 引擎按 locale 选形。数字日期一律交给 `Intl`,别手拼分隔符与符号。

```json
// locales/zh-CN.json — 整句模板 + ICU plural,语序与复数都由翻译承载
{
  "cart.welcome": "{name},欢迎回来",
  "cart.count": "{count, plural, other {购物车有 # 件商品}}"
}
// locales/en-US.json
{
  "cart.welcome": "Welcome back, {name}",
  "cart.count": "{count, plural, one {# item in cart} other {# items in cart}}"
}
```

## 反例·正例

```tsx
// 反例:拼接整句,英文 "Welcome back, X" 与中文 "X,欢迎回来" 语序相反,翻译无从下手
const HeaderBad = ({ name }: { name: string }) => (
  <h2>{t("hi") + name + t("welcome")}</h2>
);
// 反例:手判复数 + 手拼金额,波兰/阿拉伯多复数形全错,千分位与货币符号写死
const SummaryBad = ({ count, total }: { count: number; total: number }) => (
  <p>{count > 1 ? t("items") : t("item")},共 ¥{total.toFixed(2)}</p>
);
```

```tsx
import { useTranslation } from "react-i18next";
import { formatCurrency } from "@/utils/format"; // 内部用 Intl.NumberFormat

// 正例:整句模板 + ICU 复数 + Intl 货币,组件只编排
const Summary = ({ name, count, total, locale }: SummaryProps) => {
  const { t } = useTranslation();
  // 步骤 1:含变量句子走占位符整句翻译,语序交给资源文件
  const greeting = t("cart.welcome", { name });
  // 步骤 2:复数走 ICU,各语言复数形由 i18next 按 locale 选
  const countText = t("cart.count", { count });
  // 步骤 3:货币交给 Intl,千分位与符号按 locale 生成
  const totalText = formatCurrency(total, locale);
  // 步骤 4:平铺渲染,无字符串拼接
  return (
    <section>
      <h2>{greeting}</h2>
      <p>{countText} · {totalText}</p>
    </section>
  );
};
```

```tsx
// 正例:文本膨胀(德/俄常长 30%)与 RTL — dir 由 locale 推导,间距用逻辑属性
const Page = ({ locale, children }: PageProps) => {
  // 步骤 1:RTL 语言集合判定方向,阿拉伯/希伯来语走 rtl
  const dir = ["ar", "he", "fa"].includes(locale) ? "rtl" : "ltr";
  // 步骤 2:dir 落到容器,内部用 margin-inline-start 自动随方向翻转
  return (
    <div dir={dir} style={{ marginInlineStart: 16 }}>
      {children}
    </div>
  );
};
```

## 自检

- [ ] 含变量的句子是整句一个 key + `{占位符}`,没有 `t() + 变量 + t()` 拼接?
- [ ] 单复数走 ICU `{count, plural, ...}`,而非 `count > 1 ? : ` 手判?
- [ ] ICU 复数列了目标语言所需形(英 one/other、波兰 one/few/many、阿拉伯 6 形)?
- [ ] 数字 / 货币 / 百分比走 `Intl.NumberFormat`,日期走 `Intl.DateTimeFormat` / dayjs locale?
- [ ] 组件里没有硬编码中文 / 英文字面量,全部抽成 message key?
- [ ] RTL:容器设了 `dir`,间距用 `margin-inline-start` 等逻辑属性替代 `margin-left`?

## 相关

- 父:[`./index.md`](./index.md)
- 跨引:[`../../../lang/typescript/number/format.md`](../../../lang/typescript/number/format.md)(数字货币格式化)
- 跨引:[`../../../lang/typescript/datetime/pitfalls.md`](../../../lang/typescript/datetime/pitfalls.md)(日期格式化陷阱)
- 跨引:[`../../antd/setup/install-and-locale.md`](../../antd/setup/install-and-locale.md)(antd ConfigProvider locale)
