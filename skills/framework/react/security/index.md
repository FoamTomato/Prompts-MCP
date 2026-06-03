---
name: framework-react-security-index
description: 前端安全两类约定：XSS 与 dangerouslySetInnerHTML 消毒、token 存储与 open redirect 防护。Use when 渲染用户内容 / 存登录态 / 做跳转或回调时下钻
parent: ../index.md
children:
  - { name: xss-sanitization, path: xss-sanitization.md, tag: skill, note: 渲染用户 HTML 前 DOMPurify 消毒 / 禁裸 dangerouslySetInnerHTML }
  - { name: token-storage-redirect, path: token-storage-redirect.md, tag: skill, note: token 存哪里 / 跳转回调白名单防 open redirect }
when_to_descend: 渲染用户内容、存登录态、做跳转 / 回调
---

# Security · 子项索引

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| xss-sanitization | skill | 渲染用户 HTML 前消毒，禁裸 `dangerouslySetInnerHTML` |
| token-storage-redirect | skill | token 存储位置选型 + 跳转白名单防 open redirect |

## 何时下钻

- 把用户输入 / 富文本 / Markdown 渲染成 HTML → `xss-sanitization.md`
- 决定登录态 token 存 localStorage / cookie / 内存 → `token-storage-redirect.md`
- 读 `redirect` / `returnUrl` 查询参数做跳转或 OAuth 回调 → `token-storage-redirect.md`

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../error-handling/index.md`](../error-handling/index.md) · [`../state/index.md`](../state/index.md)
- 同源策略与跨域原理（CORS）：[`../../../fundamentals/frontend/cors-same-origin.md`](../../../fundamentals/frontend/cors-same-origin.md)
