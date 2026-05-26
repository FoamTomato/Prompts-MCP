---
name: antd-modal-lazy-mount
description: '框架约定 · antd: destroyOnClose 懒挂载 — 避免大内容预渲染'
parent: ./index.md
paths:
- frontend/src/**/*.tsx
triggers:
  keywords:
  - destroyOnClose
  - Modal
  - Drawer
  - 懒挂载
  - 避免大内
  - 免大内容
effort: medium
context: inline
version: '1.0'
---
# antd · Modal/Drawer 懒挂载

## 规则

**含大量内容或表单状态的 Modal / Drawer 必须设 `destroyOnClose`**，关闭时卸载内部组件树。

## 反例 → 正例

```tsx
// ❌ 不设 destroyOnClose
<Modal title="编辑" open={open} onCancel={close}>
  <BigForm />   {/* 关闭后 BigForm 仍挂载，订阅、定时器、表单状态都在 */}
</Modal>

// ✅
<Modal title="编辑" open={open} onCancel={close} destroyOnClose>
  <BigForm />   {/* 关闭即卸载，下次打开是干净的 */}
</Modal>
```

## 何时设

| 内容 | 建议 |
|------|------|
| 大型表单（重新打开应重置） | ✅ destroyOnClose |
| 视频 / 大图片 | ✅（释放内存） |
| 含 useEffect 订阅 / 定时器 | ✅（避免泄漏） |
| AI 流式生成内容（如 D13 AIImagePanel） | ✅ |
| 纯展示文字 | ❌（保持挂载省 mount 开销） |
| 频繁开关的 confirm | ❌ |

## Drawer 同理

```tsx
<Drawer
  title="幻灯片细节"
  open={open}
  onClose={close}
  destroyOnClose
  width={520}
>
  <SlideInspector />
</Drawer>
```

## 性能权衡

| destroyOnClose=true | destroyOnClose=false |
|---------------------|---------------------|
| 每次打开都 mount（首次稍慢） | mount 一次（保留状态） |
| 释放内存 | 内存常驻 |
| 状态干净（无残留） | 状态保留（可能有问题） |
| 适合大型 / 表单 | 适合小型 / 频繁切 |

## 与 React 19 协同

React 19 的 `<Suspense>` + lazy import 可以让首次 mount 也快。结合 destroyOnClose 双保险：

```tsx
const SlideInspector = lazy(() => import("./SlideInspector"));

<Drawer destroyOnClose open={open} onClose={close}>
  <Suspense fallback={<SkeletonGrid />}>
    <SlideInspector />
  </Suspense>
</Drawer>
```

## 自检

- [ ] 大表单 / 大内容的 Modal 设了 destroyOnClose？
- [ ] 关闭 Modal / Drawer 后 cleanup 函数被调用？
- [ ] 频繁开关的 confirm 不设 destroyOnClose（性能）？
- [ ] 大组件用 lazy + Suspense + destroyOnClose 三件套？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`confirm-vs-modal.md`](./confirm-vs-modal.md)

