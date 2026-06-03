---
name: react-effect-cleanup-leak
description: useEffect 副作用清理防泄漏 — 注册的监听/定时器/订阅/请求必须在 cleanup 里对称解除。Use when 写 useEffect 订阅或监听 / 排查未解绑导致的长期持有泄漏 / 验证严格模式 effect 跑两次。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - useEffect cleanup
  - removeEventListener
  - clearInterval
  - AbortController
  - 取消订阅
  - 副作用泄漏
  - 严格模式
effort: medium
context: inline
version: '1.0'
---
# React · 副作用清理防泄漏

## 规则

**决策点：useEffect 注册的副作用，必须在返回的 cleanup 函数里对称解除。** 凡是"注册/订阅/开启"动作，都得有配对的"注销/取消/关闭"。

| 注册（effect 内） | 解除（cleanup 内） |
|------|------|
| `addEventListener` | `removeEventListener`（同一 handler 引用） |
| `setInterval` / `setTimeout` | `clearInterval` / `clearTimeout` |
| `subscribe` / `on` / WebSocket 连接 | `unsubscribe` / `off` / `close` |
| `fetch` | `AbortController.abort()` |

要点：
- **React18 严格模式下 effect 会跑两次**（mount → cleanup → mount），正是用来检验 cleanup 是否对称；跑两次后状态异常 = cleanup 没写对。
- **卸载后 setState 多数不是真泄漏**——React18 起已不再警告。真泄漏是**未解绑的订阅/监听/定时器长期持有组件引用**，阻止 GC 回收。
- 闭包会把 handler 连同其捕获的变量一起长期持有，更要解绑（见相关链接）。

## 反例 → 正例

```tsx
// ❌ 无 cleanup：每次 mount 都叠加一个 listener + 定时器，永不解绑
function ScrollIndicator() {
  const [top, setTop] = useState(false);
  useEffect(() => {
    window.addEventListener("scroll", () => setTop(window.scrollY === 0));
    setInterval(() => console.log("tick"), 1000);
  }, []);
  return <span>{top ? "顶部" : "下方"}</span>;
}

// ✅ 注册 ↔ cleanup 对称解除，严格模式跑两次也干净
function ScrollIndicator() {
  const [top, setTop] = useState(false);

  useEffect(() => {
    // 注册滚动监听，handler 提取为具名引用以便解绑
    const onScroll = () => setTop(window.scrollY === 0);
    window.addEventListener("scroll", onScroll);
    // 开启轮询定时器，保留句柄用于清理
    const timer = setInterval(() => console.log("tick"), 1000);
    // cleanup：对称解除监听与定时器
    return () => {
      window.removeEventListener("scroll", onScroll);
      clearInterval(timer);
    };
  }, []);

  return <span>{top ? "顶部" : "下方"}</span>;
}
```

```tsx
// ✅ fetch 用 AbortController.abort() 在 cleanup 中取消
function PreviewPane({ id }: { id: string }) {
  const [html, setHtml] = useState("");

  useEffect(() => {
    // 创建中止控制器，绑定到本次请求
    const controller = new AbortController();
    // 发起预览请求，命中信号即被取消
    previewApi.fetch(id, { signal: controller.signal }).then(setHtml);
    // cleanup：id 变化或卸载时中止在途请求
    return () => controller.abort();
  }, [id]);

  return <div dangerouslySetInnerHTML={{ __html: html }} />;
}
```

## 自检

- [ ] 每个 `addEventListener` / `setInterval` / `subscribe` / `fetch` 都有配对解除？
- [ ] cleanup 里用的是同一个 handler 引用（不是新建的匿名函数）？
- [ ] 定时器 / 控制器句柄用 `const` 接住并在 cleanup 引用？
- [ ] 在严格模式下挂载两次，行为仍然干净（无重复监听 / 残留定时器）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`race-condition-cancellation.md`](./race-condition-cancellation.md)（AbortController 防请求乱序）
- 跨引：[`../hook/order-and-rules.md`](../hook/order-and-rules.md)（依赖数组与 hook 规则）· [`../../../lang/typescript/closure/pitfalls.md`](../../../lang/typescript/closure/pitfalls.md)（闭包长期持有引用）
