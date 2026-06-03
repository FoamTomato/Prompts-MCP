---
name: habit-code-baseline
description: 基础写法宪法 — 语言无关的七道关卡（命名→魔法值→错误→最小改动→无残留→边界→依赖），写码时按序流过。Use when 写或改任意源码、dev/dev-lite 启动、PR 兜底自检。
parent: ./index.md
paths:
- '**/*'
triggers:
  keywords:
  - baseline
  - 基础写法
  - 规约
  - 底线
  - 元规则
effort: low
context: inline
version: '1.0'
---
# Baseline · 基础写法宪法（语言无关）

> 写一段代码，从落笔到提交，依次流过下面七道关卡。
> 不分语言都成立；任意一关不过都算质量缺陷。语言级细则去 `lang/<lang>/`。

```text
落笔 → ①命名 → ②魔法值 → ③错误 → ④最小改动 → ⑤无残留 → ⑥边界 → ⑦依赖 → 提交
```

---

## ① 命名表意

落笔先定名。名字一眼读出"是什么 / 做什么"，需要注释解释命名 = 不合格。

```text
❌ proc(d, t)            ✅ process_order(order, order_type)
❌ flag / data / tmp     ✅ is_active / user_list / retry_count
❌ get(id)               ✅ get_user_by_id(uid)
```

- 布尔带前缀：`is_ / has_ / should_ / can_`
- 抛异常的函数把暗示写进名字：`*_or_raise`；返回可空的叫 `find_*`
- 禁拼音、禁中文标识符、禁自创缩写（`hdl`/`mgr`/`proc`）；允许通用缩写 `id/ctx/req/resp/cfg/err/i,j,k`

→ 语言级命名表：[`../../lang/python/naming/`](../../lang/python/index.md) · [`../../lang/typescript/naming/`](../../lang/typescript/index.md) · [`../../lang/java/naming/`](../../lang/java/index.md)

## ② 禁魔法值

写到字面量就停一拍：状态码 / 阈值 / 枚举串一律抽常量。

```text
❌ if status == 1:                 ✅ if status == OrderStatus.PAID:
❌ sleep(3600)                     ✅ sleep(ONE_HOUR_SECONDS)
❌ role in ("admin", "root")       ✅ role in ADMIN_ROLES
```

例外：自解释的 `0 / 1 / -1 / ""`（如 `len(x) == 0`、`index - 1`）可不抽。

→ 细则：[`../code-quality/no-magic-values.md`](../code-quality/no-magic-values.md)

## ③ 不吞错误

每个可能失败的调用，决定它：要么处理、要么带上下文上抛，绝不静默。

```text
❌ try: do() except: pass          # 空 catch，最严重
❌ catch (e) {}
❌ except Exception: return None   # 把错误偷换成正常返回
✅ except DBError as e: raise ServiceError("下单失败", cause=e)
✅ if not user: raise NotFound(f"user {uid} 不存在")
```

- 捕获尽量具体的异常类型，不裸 `except:` / `catch (Throwable)`
- 日志带够定位上下文（id / 关键入参），不是只 `log.error("失败")`

## ④ 最小改动

回看 diff：只动任务范围内的代码。

- 不顺手重排 import / 重新格式化整文件 / 改无关命名——会淹没 diff，让 review 失效
- 想做无关重构 → 单独提，不混进本次改动

## ⑤ 无调试残留

提交前清场：

- `print()` / `console.log()` / `System.out.println` 调试输出（正经日志走 logger）
- 注释掉的死代码（要删就删，版本控制会记得）
- 不带 issue 链接的临时 `TODO` / `FIXME` / `XXX`（要留必须写明"为什么留 + 谁跟进"）

## ⑥ 边界显式

逐个出入口问一遍"这里会不会空 / 越界 / 并发 / 失败"，把分支写出来。

```text
❌ return users[0].name            # users 可能空
✅ if not users: return None
   return users[0].name
```

- 空值 / 空集合：`None` / `null` / `[]` 的分支写出来
- 越界 / 除零：索引、切片、除法前先判
- 并发：共享可变状态有锁或无锁设计，不假设单线程
- 外部失败：网络 / IO / 反序列化 当作会失败来写

## ⑦ 依赖克制

提交前回看 import：

- 不为几十行能写完的小功能引入新第三方库
- 优先级：标准库 > 项目已有依赖 > 新依赖
- 真要加新依赖，在 PR 说明里给一句理由

---

## 收工自检（七关 checklist）

- [ ] ① 命名能自解释，没靠注释救烂名？
- [ ] ② 没有散落的魔法数字 / 状态串？
- [ ] ③ 没有空 catch / 静默吞异常？
- [ ] ④ diff 里只有任务相关改动，没顺手重构？
- [ ] ⑤ 没留 print/console.log/死代码/裸 TODO？
- [ ] ⑥ 空值 / 越界 / 并发 / 外部失败都显式处理了？
- [ ] ⑦ 没为小功能引新依赖？

## 相关

- 父：[`./index.md`](./index.md)
- 被它细化：[`../code-quality/naming-as-doc.md`](../code-quality/naming-as-doc.md) · [`../code-quality/no-magic-values.md`](../code-quality/no-magic-values.md)
- 语言级落地：[`../../lang/index.md`](../../lang/index.md)
