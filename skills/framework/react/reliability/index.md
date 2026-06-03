---
name: framework-react-reliability-index
description: React 前端运行可靠性索引：异步竞态取消 / 副作用清理防泄漏 / 防重复提交 / chunk 加载恢复。Use when 写异步取数或表单提交 / 排查数据乱序或卸载报错 / 处理懒加载部署后白屏。
parent: ../index.md
children:
  - { name: race-condition-cancellation, path: race-condition-cancellation.md, tag: skill, note: AbortController / ignore 标志位避免并发请求乱序覆盖 }
  - { name: effect-cleanup-leak, path: effect-cleanup-leak.md, tag: skill, note: useEffect 清理订阅 / 定时器 / 事件防卸载后 setState 泄漏 }
  - { name: prevent-double-submit, path: prevent-double-submit.md, tag: skill, note: 提交中态锁 + 按钮 loading 禁用防重复提交 }
  - { name: chunk-load-recovery, path: chunk-load-recovery.md, tag: skill, note: ChunkLoadError 捕获重载兜底防部署后懒加载白屏 }
when_to_descend: |
  写异步取数 / 表单或下单提交 / React.lazy 懒加载分包；
  或排查数据乱序覆盖、组件卸载后 setState 报错、用户连点重复提交、新版本部署后旧页面点击白屏。
---

# React · 运行可靠性索引

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| race-condition-cancellation | skill | AbortController / ignore 标志避免请求乱序覆盖 |
| effect-cleanup-leak | skill | useEffect 清理订阅 / timer / listener 防卸载泄漏 |
| prevent-double-submit | skill | 提交中态锁 + loading 禁用防重复提交 |
| chunk-load-recovery | skill | ChunkLoadError 捕获重载防部署后白屏 |

## 何时下钻

- 异步取数受快速切换 / 翻页影响导致结果乱序覆盖 → `race-condition-cancellation.md`
- useEffect 里订阅、定时器、监听器、未取消请求，卸载后报 setState 警告 → `effect-cleanup-leak.md`
- 表单 / 下单 / 支付按钮被连点造成重复请求 → `prevent-double-submit.md`
- 部署新版本后旧页面点路由懒加载报 ChunkLoadError 白屏 → `chunk-load-recovery.md`

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../hook/index.md`](../hook/index.md) · [`../error-handling/index.md`](../error-handling/index.md) · [`../state/index.md`](../state/index.md)
