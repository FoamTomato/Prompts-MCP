---
name: fundamentals-frontend-http-caching
description: "HTTP 强缓存（Cache-Control 命中不发请求）vs 协商缓存（ETag / Last-Modified 拿 304）的资源分级配置决策。Use when 部署后拿旧版 / 配 Cache-Control 与 ETag / index.html 该否缓存 / API 缓存选型。"
parent: ./index.md
paths:
- frontend/src/**/*.ts
- frontend/src/**/*.tsx
- frontend/src/**/*.vue
triggers:
  keywords:
  - Cache-Control
  - ETag
  - If-None-Match
  - Last-Modified
  - 强缓存
  - 协商缓存
  - 304
  - immutable
  - no-cache
  - contenthash
  - 部署后旧版
effort: medium
context: inline
version: '1.0'
---

# Fundamentals · HTTP 强缓存 vs 协商缓存

## 规则

决策点：**资源是否带内容指纹（contenthash）**决定走强缓存还是协商缓存。带 hash → 内容变则文件名变，可放心长缓存且命中时不发请求；不带 hash（入口、会变资源）→ 每次必须协商，由服务端用 304 判定可否复用本地副本。

| 资源类型 | 缓存头 | 行为 | 为什么 |
|----------|--------|------|--------|
| 带 contenthash 的 chunk（js/css/图） | `Cache-Control: max-age=31536000, immutable` | 强缓存，命中不发请求 | hash 变即新文件名，长缓存 1 年也不会拿到旧内容 |
| `index.html` | `Cache-Control: no-cache` | 每次协商，配 ETag 拿 304 | 入口必须最新，才能引用到带新 hash 的 chunk |
| API（多数） | `Cache-Control: no-store` | 不缓存，每次回源 | 业务数据时效敏感，缓存易脏 |
| API（可缓存的字典/配置） | `Cache-Control: no-cache` + ETag | 协商，命中返 304 省传输 | 内容稳定但需保证新鲜，304 只省 body |

要点辨析：
- `no-cache` ≠ 不缓存，而是**每次都先协商**（缓存了但用前必问服务端）；真正不存的是 `no-store`。
- `immutable` 告诉浏览器有效期内连协商都免了（用户刷新也不发条件请求），仅对永不变更的 hash 资源用。
- 强缓存命中走本地，**不产生请求**；协商缓存仍发请求，命中返 `304 Not Modified`（无 body）省的是传输不是往返。
- ETag（内容指纹，强/弱）优先级高于 Last-Modified（秒级时间戳，同秒内多次改测不出），两者可并存。

## 反例

```ts
// 反例：给 index.html 配长强缓存 —— 部署新版后用户本地命中旧 html，
// 旧 html 引用的旧 chunk 文件名已被删除 → 白屏 / ChunkLoadError，且无法自愈
// 响应头: Cache-Control: max-age=31536000, immutable   ❌ 入口绝不能强缓存
```

```ts
// 反例：给带 hash 的 chunk 配 no-cache —— 每次刷新都发协商请求拿 304，
// 平白增加 RTT；hash 已保证内容唯一,这里就该 immutable 强缓存   ❌
```

## 正例

前端侧能控的是**产物带 hash** 与**请求级缓存语义**，缓存头本身由部署层（nginx/CDN）按文件名规则下发。

```ts
// vite.config.ts —— 产物带 contenthash，是 chunk 走 immutable 强缓存的前置
import { defineConfig } from 'vite'

// 文件名内嵌内容哈希:内容变 hash 才变,部署层据此对带 hash 文件下发长缓存
export default defineConfig({
  build: { rollupOptions: { output: {
    entryFileNames: 'assets/[name].[hash].js',
    chunkFileNames: 'assets/[name].[hash].js',
    assetFileNames: 'assets/[name].[hash][extname]',
  } } },
})
```

```ts
// api/dict.ts —— 协商缓存友好:工具函数下沉,入口平坦编排,每步一注释
const buildRevalidateHeaders = (etag: string | null): HeadersInit =>
  etag ? { 'If-None-Match': etag } : {}

// 拉取可缓存字典:带上次 ETag 协商,304 则复用本地缓存,200 则更新
export const fetchDict = async (etag: string | null): Promise<DictResult> => {
  // 携带条件请求头发起协商
  const res = await fetch('/api/dict', { headers: buildRevalidateHeaders(etag) })
  // 早返回:服务端判定未变,直接命中本地
  if (res.status === 304) return { changed: false }
  // 内容已变:取新 body 与新 ETag 落本地
  const data = (await res.json()) as DictData
  return { changed: true, data, etag: res.headers.get('ETag') }
}
```

## 自检

- [ ] 带 contenthash 的 chunk 配 `max-age=31536000, immutable`，命中不发请求
- [ ] `index.html` 配 `no-cache`（非 `no-store`、非长 `max-age`），每次协商拿最新入口
- [ ] 区分清 `no-cache`（每次协商）与 `no-store`（绝不缓存），API 默认 `no-store`
- [ ] 协商缓存优先用 ETag，理解 304 省的是 body 而非往返
- [ ] 构建产物带 hash，部署后旧 chunk 与新 chunk 文件名不冲突（白屏自愈见跨引）

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`./build-tooling.md`](./build-tooling.md)（contenthash 与拆包） · [`./cors-same-origin.md`](./cors-same-origin.md)
- 跨引：[`../../framework/react/reliability/chunk-load-recovery.md`](../../framework/react/reliability/chunk-load-recovery.md)（HTML 误配强缓存导致部署后拿旧版、懒加载白屏时的运行时兜底）
