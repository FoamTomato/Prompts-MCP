---
name: py-ctx-exitstack-suppress
description: contextlib 工具 ExitStack 动态多资源、suppress 忽略异常、nullcontext 占位、redirect_stdout。Use when 资源数量运行时才定 / 想跳过 try-except-pass / 条件性进 with / 重定向输出。
parent: ./index.md
paths:
- '*.py'
- py/**/*.py
triggers:
  keywords:
  - 动态资源
  - ExitStack
  - suppress
  - nullcontext
  - redirect_stdout
effort: medium
context: inline
version: '1.0'
---
# Python · ExitStack / suppress / nullcontext

## 规则

| 工具 | 用途 | 何时用 |
|------|------|--------|
| `ExitStack()` | 把任意个上下文管理器压入同一个栈，退出时**逆序**全部关闭 | 资源个数运行时才知道（如打开一批文件） |
| `stack.enter_context(cm)` | 进入一个 cm 并登记，返回其 `__enter__` 值 | 在循环里逐个进栈 |
| `stack.callback(fn, *a)` | 登记一个普通清理回调（非上下文管理器） | 清理无 `with` 接口的资源 |
| `suppress(*excs)` | 忽略指定异常，等价于 `try/except <excs>: pass` | 删不存在的文件等"没有就算了"场景 |
| `nullcontext(x)` | 什么都不做的占位 cm，`as` 得到 `x` | 条件性决定是否真正进 `with` |
| `redirect_stdout(f)` | 临时把 `print` 重定向到 `f` | 捕获第三方库的 stdout |

## 正例

```python
from contextlib import ExitStack, suppress, nullcontext, redirect_stdout
import io

# 1. 动态多资源：N 个文件全部安全关闭，逆序退出
def merge(paths: list[str], out: str) -> None:
    with ExitStack() as stack:
        files = [stack.enter_context(open(p)) for p in paths]
        with open(out, "w") as dst:
            for f in files:
                dst.write(f.read())     # 任一步抛异常，已开的文件都会被关

# 2. suppress：替代 try/except-pass
with suppress(FileNotFoundError):
    os.remove("cache.tmp")              # 不存在就算了，不报错

# 3. nullcontext：条件性进 with，避免 if/else 重复块
cm = open(path) if path else nullcontext(sys.stdin)
with cm as src:
    process(src)

# 4. redirect_stdout：捕获库的 print
buf = io.StringIO()
with redirect_stdout(buf):
    noisy_lib.run()
captured = buf.getvalue()
```

## 反例

```python
# ❌ 1. 嵌套 with 管理可变数量资源 —— 写死层数，数量一变就崩
with open(a) as fa, open(b) as fc:      # 只能处理固定个数
    ...

# ❌ 2. try/except 后 pass —— 用 suppress 更短且意图明确
try:
    os.remove(p)
except FileNotFoundError:
    pass                                # → with suppress(FileNotFoundError):

# ❌ 3. suppress(Exception) 一把抓 —— 退化成裸 except，吞掉真错误
with suppress(Exception):               # 只 suppress 你预期的具体异常
    risky()

# ❌ 4. 用 if/else 重复整段逻辑，只为决定要不要进 with —— 改 nullcontext
if path:
    with open(path) as f: process(f)
else:
    process(sys.stdin)
```

## 自检

- [ ] 资源个数运行时才定 → 用 `ExitStack`，没有写死嵌套 `with`？
- [ ] `try/except <Specific>: pass` 已替换为 `suppress(<Specific>)`？
- [ ] `suppress` 传的是**具体**异常，不是 `Exception`？
- [ ] 条件性进 `with` 用 `nullcontext` 占位，没有重复代码块？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`contextmanager-protocol.md`](./contextmanager-protocol.md) · [`async-context-manager.md`](./async-context-manager.md)
