---
name: typescript-form-error-handling
description: antd Form 提交局部 catch ApiError + 字段映射 — 比 ErrorBoundary 更细，比 Form rules 更全。Use when 写表单 onSubmit / 后端业务断言失败要回填字段 / 评审表单错误兜底 / 调试用户提交后无反馈。
parent: ./index.md
paths:
  - "frontend/app/**/*.tsx"
  - "frontend/app/views/**/*.tsx"
triggers:
  keywords:
    - Form
    - setError
    - onSubmit
    - ApiError
    - instanceof
    - 表单校验
    - 字段错误
    - antd Form
    - form.setFields
effort: medium
version: "1.0"
---

# Form · 局部错误处理

## 场景分类（哪一种用什么）

| 错误类型 | 处理位置 |
|---------|---------|
| 路由级未捕获错误 | `app/error.tsx` ErrorBoundary（[`error-boundary.md`](./error-boundary.md)） |
| 表单提交业务失败 | **表单组件内 try/catch + setFields**（**本叶子**） |
| 表单字段实时校验 | antd `Form.Item rules`（不要走 ApiError） |
| 全局 toast 错误 | `App.message.error`（API 兜底） |

## 规则

1. **try/catch 包住整个 onSubmit**（含客户端预校验 + 后端调用）。
2. **catch 用 `e instanceof ApiError` 守卫**，未知错误 `throw e` 透传给 ErrorBoundary。
3. **字段级错误**用 `form.setFields([{ name: field, errors: [...] }])` 高亮对应输入框；**业务级错误**绑到 `_root` 或顶部 alert。
4. **`FIELD_BY_CODE` 映射独立维护**，不在组件里硬编码 —— 每个业务模块自己的 `_internals/error-mapping.ts`。
5. **客户端预校验和后端断言共享错误码**（如 D003 客户端和后端用同一个，fetcher 把后端响应转 ApiError）。
6. **`setSubmitting(false)` 必在 `finally`**，不在 catch 里。
7. **简单 required/maxLength** 用 `Form.Item rules`，不走 try/catch。

## 自检

- [ ] try/catch 包住 `await` + 客户端预校验？
- [ ] catch 用 `e instanceof ApiError` 守卫？
- [ ] 字段相关错误用 `form.setFields` 绑定到具体 input？
- [ ] 业务级错误绑到 `_root` 或 toast？
- [ ] 未知错误 `throw e` 透传？
- [ ] `FIELD_BY_CODE` 独立维护？
- [ ] `setSubmitting(false)` 在 `finally`？

## 详细参考

- 完整 OutlineFormView 实现 + FIELD_BY_CODE 字典 + 反例集：[`./form-error-handling.examples.md`](./form-error-handling.examples.md)

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`assert-helpers.md`](./assert-helpers.md) · [`error-boundary.md`](./error-boundary.md) · [`api-error-class.md`](./api-error-class.md)
- 配套：[`../../../framework/antd/form/index.md`](../../../framework/antd/form/index.md)
- 错误码字典：`.ai/skills/core/error_code_dict.md`
