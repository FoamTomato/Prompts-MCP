---
name: framework-react-hook-index
description: React Hooks 规范
parent: ../index.md
children:
  - { name: order-and-rules, path: order-and-rules.md, tag: skill, note: hooks 顺序：state→ref→derived→effect→anim→callback }
  - { name: custom-hook-naming, path: custom-hook-naming.md, tag: skill, note: 自定义 hook 命名 useXxx }
  - { name: no-fetch-in-use-effect, path: no-fetch-in-use-effect.md, tag: skill, note: 禁在 useEffect 拉数据，用 TanStack Query }
when_to_descend: 写 hook / Review useEffect 用法
---

# Hook · 子项索引

| 子项 | 一句话 |
|------|-------|
| order-and-rules | hooks 顺序：state→ref→derived→effect→anim→callback |
| custom-hook-naming | 自定义 hook 命名 useXxx |
| no-fetch-in-use-effect | 禁在 useEffect 拉数据，用 TanStack Query |
