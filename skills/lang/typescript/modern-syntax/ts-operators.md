---
name: ts-operators-satisfies-using
description: TS 专属运算符 — satisfies 校验值合规又不拓宽字面量 / using 与 await using 作用域结束确定性释放资源。Use when 配置对象或常量映射要类型校验但保窄推断 / 句柄锁连接需自动释放 / 纠结 satisfies vs as vs 类型注解
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - satisfies
  - using
  - await using
  - Symbol.dispose
  - Symbol.asyncDispose
  - 字面量推断
  - 资源释放
  - 配置对象
effort: medium
context: inline
version: '1.0'
---
# TypeScript · satisfies 与 using 资源管理

## 规则

两个 **TS-only** 语法(JS 无 `satisfies`;`using` 需 TS5.2+ 且转译/polyfill),与 runtime 标准库方法分属不同责任。

### satisfies:既校验又不拓宽字面量

决策点:想让值「符合类型」又「保留最窄推断」,选 `satisfies`,别用 `as` 或 `: T`。

| 写法 | 类型校验 | 字面量推断 | 问题 |
|------|---------|-----------|------|
| `: Config` 注解 | 校验 | **被拓宽** | 取值丢失字面量,`config.env` 变 `string` 而非 `"prod"` |
| `as Config` 断言 | **不校验** | 拓宽 | 谎报类型,拼错 key / 缺字段不报错 |
| `satisfies Config` | 校验 | **保留** | 首选:配置对象 / 路由表 / 常量映射 |

### using / await using:确定性释放

决策点:资源(文件句柄 / 锁 / 订阅 / 连接)需「作用域结束即释放」,且对象实现了 `Symbol.dispose`(同步)或 `Symbol.asyncDispose`(异步)→ 用 `using` / `await using` 替代手写 try/finally。门槛:TS5.2+、`target`/`lib` 含 `esnext.disposable`、运行时或 polyfill 支持。**前端浏览器场景门槛高、可释放对象稀少,不滥用**;多用于 Node 工具脚本 / 测试夹具。

## 反例 → 正例

```ts
// ❌ : T 注解吞掉字面量推断
const config: AppConfig = { env: "prod", retries: 3 };
config.env; // 推断成 string,switch 无法穷尽

// ❌ as 断言不校验,拼错字段静默通过
const routes = { home: "/", uesr: "/user" } as RouteMap; // uesr 拼错不报错

// ✅ satisfies:校验合规 + 保留窄类型
const config = { env: "prod", retries: 3 } satisfies AppConfig;
config.env; // 仍是 "prod" 字面量,可被穷尽收窄
```

```ts
// ❌ 手写 try/finally,提前 return / 抛错易漏释放
async function readBatch(paths: string[]): Promise<string[]> {
  const handle = await openFile(paths[0]);
  try {
    return await handle.readAll();
  } finally {
    await handle.close(); // 多资源时嵌套臃肿
  }
}

// ✅ await using:作用域结束自动调用 Symbol.asyncDispose
async function readBatch(paths: string[]): Promise<string[]> {
  // 声明即托管,函数退出(含异常)时确定性释放
  await using handle = await openFile(paths[0]);
  // 体内只做业务,无需 finally
  return handle.readAll();
}
```

```ts
// ✅ 自定义可释放资源:实现 Symbol.dispose
class Subscription {
  constructor(private readonly off: () => void) {}
  [Symbol.dispose]() {
    // 退出作用域时退订
    this.off();
  }
}

function watch(emitter: Emitter): void {
  // using 声明:块结束自动退订
  using sub = new Subscription(emitter.on("tick", handleTick));
  // 业务编排,无需手动 sub.off()
  emitter.flush();
}
```

## 自检

- [ ] 配置对象 / 路由表 / 常量映射用 `satisfies T` 而非 `: T`(拓宽)或 `as T`(不校验)?
- [ ] 需保留字面量推断又要类型约束时,没有错用注解或断言?
- [ ] `using` / `await using` 仅用于实现了 `Symbol.dispose` / `Symbol.asyncDispose` 的资源?
- [ ] 已确认 TS5.2+ 且 `target` / `lib` 支持 disposable;浏览器侧无合适资源时不强用?
- [ ] 未把 satisfies(纯类型)与 runtime 数组/对象方法混为一谈?

## 相关

- 父:[`./index.md`](./index.md)
- 兄弟:[`array-object-methods.md`](./array-object-methods.md)
- 跨引:`as` 断言为何不安全 → [`../typing/no-any.md`](../typing/no-any.md)
