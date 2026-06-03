---
name: react-chunk-load-recovery
description: 部署新版后旧页面懒加载报 ChunkLoadError 白屏的恢复:contenthash 文件名 + 捕获 preloadError 重载 + sessionStorage 去重防死循环。Use when React.lazy 路由白屏 / 报 Loading chunk failed。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - ChunkLoadError
  - vite:preloadError
  - Loading chunk failed
  - React.lazy
  - 动态 import
  - contenthash
  - 部署后白屏
  - chunk 加载失败
effort: medium
context: inline
version: '1.0'
---

# React · chunk 加载失败恢复

## 规则

决策点：部署新版后旧页面的 `React.lazy` 动态 import 找不到被替换的旧 chunk → 抛 `ChunkLoadError` / `Loading chunk failed` → 白屏。三招组合兜底：

| 招式 | 做什么 | 解决 |
|------|--------|------|
| 1 构建 contenthash | 产物文件名带内容 hash（`[name].[hash].js`），内容不变 hash 不变 | 未改动的 chunk 仍命中缓存，缩小失效面 |
| 2 捕获并重载 | 监听 Vite `vite:preloadError` 或包裹动态 import 的 reject | 失效时引导/自动 `location.reload()` 拉取新清单 |
| 3 sessionStorage 去重 | 记上次失败时间戳，短时间内同错误不再 reload | 防新版本仍坏导致的无限刷新死循环 |

构建侧（vite.config.ts）固定 contenthash：

```ts
// 产物文件名带内容哈希：内容变 hash 才变，命中缓存更稳
export default defineConfig({
  build: { rollupOptions: { output: {
    entryFileNames: 'assets/[name].[hash].js',
    chunkFileNames: 'assets/[name].[hash].js',
  } } },
})
```

反例（直接 reload，新版仍坏时无限刷新）：

```ts
// 反例：无去重守卫，部署的新版若同样加载失败会一直刷
window.addEventListener('vite:preloadError', () => location.reload())
```

正例：守卫先行，超窗口才允许再次 reload（早返回防死循环）。

```ts
// utils/chunkRecovery.ts —— 纯函数下沉判定与记账
const RELOAD_KEY = 'chunk-reload-at'
const COOLDOWN_MS = 10_000

// 判定：距上次因 chunk 失败重载是否仍在冷却窗口内
export const isWithinReloadCooldown = (now: number): boolean => {
  const last = Number(sessionStorage.getItem(RELOAD_KEY) ?? 0)
  return now - last < COOLDOWN_MS
}

// 记账：写入本次重载时间戳
export const markReloaded = (now: number): void => {
  sessionStorage.setItem(RELOAD_KEY, String(now))
}
```

```ts
// app/bootstrap.ts —— 平坦编排，每步一注释
import { isWithinReloadCooldown, markReloaded } from '@/utils/chunkRecovery'
import { message } from 'antd'

// 注册全局监听 + 包裹 lazy 的 import，二者共用同一恢复入口
export const registerChunkRecovery = (): void => {
  window.addEventListener('vite:preloadError', () => recoverFromChunkError())
}
export const lazyWithRecovery = (load: () => Promise<unknown>) =>
  load().catch((err) => { recoverFromChunkError(); throw err })

// 恢复流程：守卫去重 → 记账 → 提示并重载
const recoverFromChunkError = (): void => {
  const now = Date.now()
  // 守卫：冷却窗口内已 reload 过，说明新版仍坏，停止刷新避免死循环
  if (isWithinReloadCooldown(now)) {
    message.error('页面资源加载失败，请稍后重试或清除缓存')
    return
  }
  // 记账后拉取最新版本
  markReloaded(now)
  message.loading('检测到新版本，正在刷新…')
  location.reload()
}
```

## 自检

- [ ] 构建产物文件名带 contenthash，内容不变 hash 不变
- [ ] 监听了 `vite:preloadError` 或包裹动态 import 的 reject
- [ ] reload 前用 sessionStorage 时间戳做了冷却去重，不会无限刷新
- [ ] 冷却窗口内再次失败给出明确提示而非静默白屏
- [ ] 恢复逻辑下沉 utils 纯函数，入口只做编排

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`./effect-cleanup-leak.md`](./effect-cleanup-leak.md) · [`./prevent-double-submit.md`](./prevent-double-submit.md)
- 跨引：[`../performance/code-splitting.md`](../performance/code-splitting.md)（lazy + Suspense 拆包是本恢复方案的前置场景）
