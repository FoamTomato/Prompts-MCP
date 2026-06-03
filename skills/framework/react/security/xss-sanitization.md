---
name: react-xss-sanitization
description: React XSS 防护：默认转义安全，dangerouslySetInnerHTML 与 href 用户输入是唯一缺口。Use when 渲染用户 HTML / 富文本 / Markdown / 拼 href 跳转链接时
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - dangerouslySetInnerHTML
  - DOMPurify
  - sanitize
  - XSS 防护
  - 富文本消毒
  - Markdown 渲染
  - href 注入
  - 协议白名单
effort: high
context: inline
version: '1.0'
---
# React · XSS 防护

## 规则

决策点：内容怎么进 DOM 决定要不要消毒。

| 写法 | 是否转义 | 处置 |
|------|---------|------|
| `{userInput}` 文本插值 | React 默认转义，安全 | 直接用 |
| `dangerouslySetInnerHTML` | 绕过转义 | 插入前必经 `DOMPurify.sanitize` |
| 富文本 / Markdown 渲染 | 输出 HTML | 白名单消毒后再 `dangerouslySetInnerHTML` |
| `href={userInput}` | 可被 `javascript:` 注入 | 校验协议白名单，非白名单降级 `#` |

消毒与协议校验下沉到纯函数，组件体只编排。

```ts
// frontend/src/utils/sanitize.ts
import DOMPurify from "dompurify";

// 富文本白名单消毒：仅放行排版标签与安全属性
export const sanitizeRichHtml = (raw: string): string =>
  DOMPurify.sanitize(raw, {
    ALLOWED_TAGS: ["p", "br", "strong", "em", "ul", "ol", "li", "a", "h1", "h2", "code"],
    ALLOWED_ATTR: ["href", "title"],
  });

// 链接协议白名单:只允许 http/https/mailto,否则降级为锚点
const SAFE_PROTOCOLS = ["http:", "https:", "mailto:"];
export const safeHref = (raw: string | null | undefined): string => {
  if (!raw) return "#";
  try {
    const url = new URL(raw, window.location.origin);
    return SAFE_PROTOCOLS.includes(url.protocol) ? raw : "#";
  } catch {
    return "#";
  }
};
```

## 反例·正例

```tsx
// 反例：用户 HTML 直接塞进 DOM，<script>/onerror 可执行
const ArticleBad = ({ userHtml }: { userHtml: string }) => (
  <div dangerouslySetInnerHTML={{ __html: userHtml }} />
);

// 反例：href 直接放用户输入，javascript:alert(1) 可注入
const LinkBad = ({ rawUrl }: { rawUrl: string }) => <a href={rawUrl}>详情</a>;
```

```tsx
import { sanitizeRichHtml, safeHref } from "@/utils/sanitize";

// 正例：富文本先消毒再渲染
const Article = ({ userHtml }: { userHtml: string }) => {
  // 步骤 1：白名单消毒,剥离脚本与危险属性
  const clean = sanitizeRichHtml(userHtml);
  // 步骤 2:消毒后内容才允许进入 DOM
  return <div dangerouslySetInnerHTML={{ __html: clean }} />;
};

// 正例：href 先过协议白名单
const Link = ({ rawUrl }: { rawUrl: string }) => {
  // 步骤 1:校验协议,非白名单降级为 #
  const href = safeHref(rawUrl);
  // 步骤 2:渲染受信链接
  return <a href={href} rel="noopener noreferrer">详情</a>;
};
```

## 自检

- [ ] 纯文本走 `{}` 插值，没有为省事改用 `dangerouslySetInnerHTML`？
- [ ] 每个 `dangerouslySetInnerHTML` 的 `__html` 都来自 `DOMPurify.sanitize` 输出？
- [ ] 富文本 / Markdown 消毒配了 `ALLOWED_TAGS` / `ALLOWED_ATTR` 白名单？
- [ ] 用户可控的 `href` / `src` 过了协议白名单，非白名单降级 `#`？
- [ ] 外链补 `rel="noopener noreferrer"`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`token-storage-redirect.md`](./token-storage-redirect.md)
- 跨引：[`../../antd/form/validator-pattern.md`](../../antd/form/validator-pattern.md)（输入侧校验）
- 跨引：[`../../../lang/typescript/null-safety/optional-chaining-nullish.md`](../../../lang/typescript/null-safety/optional-chaining-nullish.md)（空值兜底）
