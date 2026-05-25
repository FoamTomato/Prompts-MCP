---
name: lang-python-naming-index
description: Python 命名规范
parent: ../index.md
children:
  - { name: function-naming, path: function-naming.md, tag: skill, note: 函数 snake_case 动词开头 }
  - { name: variable-naming, path: variable-naming.md, tag: skill, note: 变量 snake_case 名词性 }
  - { name: module-naming, path: module-naming.md, tag: skill, note: 模块/包小写 + 单数 }
when_to_descend: 命名任何 Python 函数 / 变量 / 模块前。
---

# Python · 命名

| 子项 | 一句话 |
|------|-------|
| function-naming | 函数 snake_case 动词开头（fetch_xxx / get_or_raise / build_xxx） |
| variable-naming | 变量 snake_case 名词性 / 布尔加 is_/has_/should_ 前缀 |
| module-naming | 模块小写单数（service.py / repository.py），文件即模块 |
