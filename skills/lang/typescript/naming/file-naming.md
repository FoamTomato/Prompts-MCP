---
name: typescript-file-naming
description: 组件 PascalCase.tsx / hook camelCase.ts / 工具 kebab-case.ts。Use when 写 TS
  业务代码 / 评审涉及 `file-naming` 的 PR。
parent: ./index.md
paths:
- frontend/**/*.ts
- frontend/**/*.tsx
triggers:
  keywords:
  - 文件命名
  - PascalCase
  - kebab-case
  - camelCase
effort: medium
context: inline
version: '1.0'
---
# TypeScript · 文件命名

## 规则

| 类别 | 命名 | 例 |
|------|------|------|
| React 组件 `.tsx` | `PascalCase` | `ArticleCard.tsx` / `GenerateButton.tsx` |
| 页面（路由组件） | `PascalCase` | `HomePage.tsx` / `EditorPage.tsx` |
| 自定义 hook | `camelCase`（`useXxx`） | `useSSE.ts` / `useArticleHistory.ts` |
| Zustand store | `camelCase`（`use...Store`） | `editorStore.ts` / `useTenantStore.ts` |
| 工具函数 | `kebab-case` 或 `camelCase` | `format-date.ts` / `formatDate.ts`（项目统一一种） |
| 类型定义 | `kebab-case` | `article.ts` / `document-element.ts` |
| API 模块 | 复数名词 `kebab-case` | `articles.ts` / `documents.ts` |
| 样式文件 | 与组件同名 `.module.css` | `ArticleCard.module.css` |

## 项目实际规范示例

```
frontend/src/
├── components/
│   ├── Button.tsx                 # ✅ PascalCase
│   └── Button.module.css
├── features/home/
│   ├── ContentTypeSelector.tsx
│   └── GenerateButton.tsx
├── pages/
│   └── HomePage.tsx
├── hooks/
│   ├── useSSE.ts                  # ✅ useXxx
│   └── useArticleHistory.ts
├── stores/
│   └── editor.ts                  # 内部 export `useEditorStore`
├── api/
│   └── articles.ts                # ✅ 复数 kebab
├── types/
│   └── article.ts                 # ✅ kebab 单数
└── utils/
    └── format-date.ts             # ✅ kebab
```

## 反例

```
❌ articleCard.tsx           # 组件不是 camelCase
❌ Article-card.tsx          # 混合
❌ btn.tsx                   # 缩写
❌ Header.module.tsx         # 样式不是 tsx
❌ useSSE.tsx                # hook 是 ts 不是 tsx
```

## 一个文件一个组件

每个 `.tsx` 文件只导出一个主组件（同文件内的小辅助组件不算）。

```tsx
// ✅ ArticleCard.tsx
export interface ArticleCardProps { ... }
export function ArticleCard(props: ArticleCardProps) { ... }

// 同文件内的小辅助 — 允许但不 export
function CardCover({ url }: { url: string }) { ... }
```

## 自检

- [ ] 组件 PascalCase 且 `.tsx`？
- [ ] hook `useXxx` 且 `.ts`？
- [ ] 一文件一主组件？
- [ ] kebab / camel / Pascal 在项目里保持一致？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`interface-type-alias.md`](./interface-type-alias.md)

