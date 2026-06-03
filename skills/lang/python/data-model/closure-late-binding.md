---
name: py-closure-late-binding
description: 闭包延迟绑定——内层函数按名字而非值捕获外层变量，循环里建的闭包共享最终值。Use when 在 for 循环里建 lambda / 回调 / 装饰器全引用同一变量 / 理解 LEGB 与 nonlocal。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 闭包
  - 延迟绑定
  - late binding
  - LEGB
  - nonlocal
effort: medium
context: inline
version: '1.0'
---
# Python · 闭包延迟绑定与 LEGB

## 规则

| 概念 | 含义 |
|------|------|
| 延迟绑定 | 闭包捕获的是外层**变量名**，调用时才查值——不是定义时的值 |
| 循环陷阱 | 循环里建的所有闭包共享同一个循环变量，最终全读到末值 |
| 修复 | 用**默认参数**在定义时快照：`lambda x, i=i: ...` |
| LEGB | 名字解析顺序：Local → Enclosing → Global → Built-in |
| `nonlocal` | 让内层函数**赋值**外层（非全局）变量；只读不需要 |

## 正例

```python
# ✅ 默认参数把当前值快照进闭包
funcs = [lambda i=i: i for i in range(3)]
print([f() for f in funcs])      # [0, 1, 2]
```

```python
def make_counter():
    count = 0
    def inc() -> int:
        nonlocal count           # ✅ 要“赋值”外层变量，必须声明 nonlocal
        count += 1
        return count
    return inc

c = make_counter()
print(c(), c(), c())             # 1 2 3
```

## 反例

```python
# ❌ 循环里建闭包，全部捕获同一个 i，循环结束后 i==2
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])      # [2, 2, 2] —— 不是 [0,1,2]

# ❌ 内层只赋值不声明 nonlocal → 被当成新的局部变量
def make_counter():
    count = 0
    def inc():
        count += 1               # UnboundLocalError: count 成了局部、读时未定义
        return count
    return inc
```

理由：`lambda: i` 没有捕获 `i` 的值，只记住“去 enclosing 作用域查名字 `i`”。三个 lambda 共享同一个 `i`，循环跑完 `i` 停在 2，调用时全读到 2。函数体内对名字赋值会让它整段变成 Local，因此 `count += 1` 在赋值前读取就报 `UnboundLocalError`。

## 自检

- [ ] 循环里建的 lambda / 函数，用了 `arg=value` 默认参数快照当前值？
- [ ] 内层函数要修改外层变量时声明了 `nonlocal`（改全局才用 `global`）？
- [ ] 清楚闭包按名字延迟取值，不是定义时拷贝值？
- [ ] 没有在赋值前读取同名局部变量（`UnboundLocalError`）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`mutable-default-arg.md`](./mutable-default-arg.md)（同样靠默认参数，但注意可变默认坑） · [`is-vs-equals.md`](./is-vs-equals.md)
- 应用：[`../decorators/decorator-basics.md`](../decorators/decorator-basics.md)（装饰器正是闭包包裹的典型用法）
