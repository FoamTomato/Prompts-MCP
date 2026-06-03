---
name: py-copy-semantics
description: Python 是引用语义，赋值不复制；浅拷贝只复制一层，深拷贝用 copy.deepcopy。Use when 改一个对象另一个跟着变 / 复制嵌套 dict/list / 传可变对象给函数怕被改。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 引用语义
  - 浅拷贝
  - 深拷贝
  - shallow copy
  - deepcopy
effort: medium
context: inline
version: '1.0'
---
# Python · 拷贝语义（引用 / 浅 / 深）

## 规则

| 操作 | 复制了什么 | 嵌套对象 |
|------|-----------|---------|
| `b = a` | 什么都没复制，只多个名字 | 共享同一对象 |
| `a[:]` / `dict(a)` / `a.copy()` / `copy.copy(a)` | 顶层容器新建一份 | **仍共享**（浅拷贝） |
| `copy.deepcopy(a)` | 递归复制每一层 | 完全独立 |

判据：**只要内层还有可变对象（list/dict/自定义对象），浅拷贝就不够，要 deepcopy。** 全是不可变元素（int/str/tuple）时浅拷贝即够。

## 正例

```python
import copy

cfg = {"retries": 3, "headers": {"Auth": "x"}}

shallow = cfg.copy()
shallow["retries"] = 5            # 顶层独立：不影响 cfg
shallow["headers"]["Auth"] = "y"  # ⚠️ 内层共享：cfg["headers"] 也被改

deep = copy.deepcopy(cfg)
deep["headers"]["Auth"] = "z"     # ✅ 完全独立，cfg 不动
```

```python
def normalize(items: list[str]) -> list[str]:
    items = items[:]              # ✅ 想改入参先拷一份，不污染调用方
    items.sort()
    return items
```

## 反例

```python
# ❌ 以为 = 是复制
default_tags = ["new"]
user_tags = default_tags          # 同一个 list
user_tags.append("vip")
print(default_tags)               # ['new', 'vip'] —— 模板被污染

# ❌ 二维结构用 * 复制行，所有行是同一个 list
grid = [[0] * 3] * 3
grid[0][0] = 1
print(grid)                       # [[1,0,0],[1,0,0],[1,0,0]] —— 全改了
# ✅ 推导式各行独立
grid = [[0] * 3 for _ in range(3)]
```

理由：`b = a` 只是给同一对象绑第二个名字；`[x] * n` 把同一个内层对象重复 n 次。要独立副本必须显式 `copy()` / `deepcopy()` / 推导式。

## 自检

- [ ] 想要副本时用了 `copy()` / `deepcopy()` / 切片，而不是直接 `=`？
- [ ] 嵌套结构（dict 套 dict、list 套 list）用的是 `deepcopy`？
- [ ] 没有用 `[[...]] * n` 构造可变二维结构？
- [ ] 函数要修改可变入参时，先拷贝避免污染调用方？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mutable-default-arg.md`](./mutable-default-arg.md)（默认值被复用的同源问题） · [`is-vs-equals.md`](./is-vs-equals.md)（判是否同一对象用 `is`）
