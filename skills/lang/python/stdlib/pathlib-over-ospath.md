---
name: py-stdlib-pathlib-over-ospath
description: pathlib.Path 面向对象路径取代 os.path — / 拼接 / read_text / glob / mkdir。Use when 拼接路径 / 读写文件 / 遍历目录 / 判断存在 / 取扩展名。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 路径处理
  - 文件遍历
  - pathlib
  - Path
  - glob
  - read_text
effort: low
context: inline
version: '1.0'
---
# Python · pathlib 取代 os.path

## 规则

| 需求 | pathlib | 取代的 os.path |
|------|---------|----------------|
| 拼接 | `base / "sub" / "f.txt"` | `os.path.join(...)` |
| 读全文 | `p.read_text(encoding="utf-8")` | `open(...).read()` |
| 写全文 | `p.write_text(s, encoding="utf-8")` | `open(..., "w").write(s)` |
| 通配遍历 | `p.glob("**/*.py")` | `glob.glob(...)` |
| 存在判断 | `p.exists()` / `p.is_file()` | `os.path.exists(...)` |
| 取名/后缀/父目录 | `p.name` / `p.suffix` / `p.parent` | `os.path.basename` 等 |
| 建目录 | `p.mkdir(parents=True, exist_ok=True)` | `os.makedirs(...)` |

## 正例

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# / 运算符拼接，跨平台正确分隔符
config_path = ROOT / "config" / "settings.toml"

# 一行读写，显式编码
text = config_path.read_text(encoding="utf-8")
(ROOT / "out.json").write_text(payload, encoding="utf-8")

# 递归 glob，惰性产出 Path 对象
for py_file in ROOT.glob("**/*.py"):
    if py_file.is_file():
        process(py_file)

# 属性访问取各部分
p = Path("/var/log/app.2024.log")
assert p.name == "app.2024.log"
assert p.suffix == ".log"
assert p.stem == "app.2024"
assert p.parent == Path("/var/log")

# 安全建目录，已存在不报错
(ROOT / "cache").mkdir(parents=True, exist_ok=True)
```

## 反例

```python
import os

# ❌ 字符串拼接路径：分隔符、重复斜杠、跨平台都易错
path = base + "/" + sub + "/" + name          # 用 base / sub / name

# ❌ os.path 函数式风格，可读性差、易拼错参数
full = os.path.join(os.path.dirname(__file__), "data", "x.csv")

# ❌ open 不带 encoding，依赖平台默认编码
with open(path) as f:                          # Windows 下可能非 UTF-8
    data = f.read()
```

理由：`Path` 用 `/` 运算符与属性访问表达路径，跨平台一致、可读、可链式；`read_text`/`write_text` 强制显式 `encoding`，避免平台默认编码踩坑。新代码统一用 pathlib。

## 自检

- [ ] 路径拼接用 `Path / "x"` 而非字符串相加或 `os.path.join`？
- [ ] 读写小文件用 `read_text` / `write_text` 并显式 `encoding="utf-8"`？
- [ ] 目录遍历用 `Path.glob` / `rglob` 而非 `glob` 模块？
- [ ] 取文件名/后缀/父目录用 `.name` / `.suffix` / `.parent`？
- [ ] 建目录用 `mkdir(parents=True, exist_ok=True)`？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`collections-toolkit.md`](./collections-toolkit.md) · [`functools-toolkit.md`](./functools-toolkit.md)
