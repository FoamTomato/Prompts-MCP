---
name: lang-python-import-index
description: Python import 顺序与依赖规范
parent: ../index.md
children:
  - { name: absolute-import-only, path: absolute-import-only.md, tag: skill, note: 禁相对导入 }
  - { name: import-order, path: import-order.md, tag: skill, note: stdlib → third-party → local }
  - { name: no-circular-import, path: no-circular-import.md, tag: skill, note: 禁 Service 互依赖 }
when_to_descend: 组织 import 语句 / 排查循环依赖时
---

# Import · 子项索引

| 子项 | 一句话 |
|------|-------|
| absolute-import-only | 禁相对导入 |
| import-order | stdlib → third-party → local |
| no-circular-import | 禁 Service 互依赖 |
