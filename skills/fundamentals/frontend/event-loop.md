---
name: fundamentals-frontend-event-loop
description: "事件循环宏任务微任务的执行顺序与调度决策 — 同步栈清空后先排空全部微任务再取一个宏任务。Use when 看不懂 Promise/setTimeout/await 谁先跑 / 长计算阻塞渲染要让出主线程 / 选微任务还是宏任务还是 rAF 时。"
parent: ./index.md
paths:
- frontend/src/**/*.ts
- frontend/src/**/*.tsx
- frontend/src/**/*.vue
triggers:
  keywords:
  - 事件循环
  - 微任务
  - 宏任务
  - event loop
  - microtask
  - macrotask
  - queueMicrotask
  - requestAnimationFrame
  - setTimeout 0
effort: medium
context: inline
version: '1.0'
---
# Fundamentals 前端 · 事件循环宏任务微任务

## 规则

**决策点：异步代码该排进哪个队列，取决于你要"尽快、紧贴当前栈"还是"让出主线程给渲染/响应"。** JS 单线程：同步调用栈跑空后，**先排空全部微任务队列**（排空过程中新入队的微任务也一并跑完），**再取一个宏任务**，然后下一轮循环又先清微任务。渲染时机插在两者之间（浏览器自行决定是否绘制）。

| 你的诉求 | 选什么 | 入哪个队列 |
|---------|-------|-----------|
| DOM 改完想在浏览器绘制前同步收尾、读最终布局 | 微任务：`Promise.then` / `queueMicrotask` / `MutationObserver` | 微任务，本轮排空 |
| 让出主线程给渲染与用户输入、打散长任务 | 宏任务：`setTimeout(fn, 0)` / `MessageChannel` | 宏任务，下一轮才取一个 |
| 跟随屏幕刷新做动画 / 视觉更新 | `requestAnimationFrame`（**另算**，绘制前回调，约 16.7ms/帧，需自测） | rAF 队列，非宏非微 |
| 不在乎时机、只想异步解耦 | 优先微任务（开销更小、更早） | 微任务 |

要点：`await x` 之后的代码等价于 `.then` 回调，是**微任务**，不是同步续跑；`setTimeout(0)` 最小延迟受浏览器钳制（通常 ≥4ms，嵌套更久）。

## 反例 → 正例

```ts
// ❌ 长同步计算独占主线程：微任务里无限链式 then 会饿死渲染，页面冻结无法响应
function renderAll(rows: Row[]): void {
  // 一次性同步处理十万行，主线程被占满，浏览器无机会绘制/响应点击
  rows.forEach((row) => paintRow(row));
}
```

```ts
// ✅ 拆 chunk + 用宏任务让出主线程：每批之间还给浏览器一帧去绘制和响应输入
function renderAllChunked(rows: Row[], size = 500): void {
  // 切片：把大数组按批大小拆成二维数组（>3 行转换下沉纯函数 chunk）
  const batches = chunk(rows, size);
  // 取出下一批并递归排下一个宏任务，逐批让出主线程
  const step = (index: number): void => {
    // 边界：处理完所有批次即结束
    if (index >= batches.length) return;
    // 同步绘制当前批
    batches[index].forEach((row) => paintRow(row));
    // 让出主线程，下一轮事件循环再处理下一批（给渲染/响应留窗口）
    setTimeout(() => step(index + 1), 0);
  };
  // 启动流水线
  step(0);
}

// 纯函数：等长切片，列表用 reduce 不手写 for
function chunk<T>(arr: T[], size: number): T[][] {
  return arr.reduce<T[][]>((acc, item, i) => {
    // 每满一批开新组，否则追加到当前组
    if (i % size === 0) acc.push([]);
    acc[acc.length - 1].push(item);
    return acc;
  }, []);
}
```

```ts
// ✅ DOM 改完、绘制前同步读最终布局：用微任务紧贴当前栈，避免读到中间态
function flushThenMeasure(node: HTMLElement, text: string): void {
  // 写：更新内容
  node.textContent = text;
  // 微任务收尾：本轮排空时执行，仍在浏览器本帧绘制前
  queueMicrotask(() => reportLayout(node.getBoundingClientRect()));
}
```

## 自检

- [ ] 想清楚诉求是"紧贴当前栈尽快跑"（微任务）还是"让出主线程给渲染/响应"（宏任务）？
- [ ] 动画 / 视觉更新用了 `requestAnimationFrame` 而非 `setTimeout`？
- [ ] 没有在微任务里无限链式 `then` / 递归 `queueMicrotask`（会饿死渲染、冻结页面）？
- [ ] 记得 `await` 后续代码是微任务，不是同步续跑，顺序推断按微任务算？
- [ ] 长同步计算已拆 chunk + 宏任务让出，而非一次性占满主线程？

## 相关

- 父：[`./index.md`](./index.md)
- 平行：[`./rendering-pipeline.md`](./rendering-pipeline.md)（让出后浏览器何时重排重绘）· [`./debounce-throttle.md`](./debounce-throttle.md)（用定时器降频）
- 跨引：[`../../lang/typescript/async/index.md`](../../lang/typescript/async/index.md)（await 微任务语义与 Promise 用法）
- 跨引：[`../../framework/react/reliability/race-condition-cancellation.md`](../../framework/react/reliability/race-condition-cancellation.md)（异步乱序到达的防护，与微任务排队相关）
