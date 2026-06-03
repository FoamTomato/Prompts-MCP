---
name: react-web-vitals-cls
description: Core Web Vitals 三指标(LCP<2.5s/INP<200ms/CLS<0.1)与 CLS 布局抖动治理:媒体定尺寸、LCP 图禁懒加载、字体 swap。Use when 加载时元素跳动 / Lighthouse CLS 偏红 / 图片视频 iframe 占位 / 字体 FOIT 时。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - CLS
  - Core Web Vitals
  - 布局抖动
  - aspect-ratio
  - LCP 图片
  - loading lazy
  - font-display swap
  - 占位尺寸
effort: medium
context: inline
version: '1.0'
---
# React Performance · Core Web Vitals 与 CLS 防抖

## 规则

**决策点**:首要治理 CLS(布局位移)——凡加载后会改变高度/位置的元素,加载前必须先占满最终尺寸。三指标达标线:

| 指标 | 含义 | 达标 |
|------|------|------|
| LCP | 最大内容绘制 | < 2.5s |
| INP | 交互到下一帧 | < 200ms |
| CLS | 累积布局位移 | < 0.1 |

CLS 防抖五条(按命中频率):

| 场景 | 做法 |
|------|------|
| 图片 / 视频 / iframe | 必设固定 `width`+`height` 或 `aspect-ratio` 先占位,禁止裸 `<img>` 撑开 |
| 骨架占位 | 占位尺寸 ≈ 真实内容(呼应骨架屏房规),同栅格布局 |
| LCP 关键图(首屏大图) | **禁 `loading="lazy"`**,改 `fetchPriority="high"`——约 16% 页面误给 LCP 图懒加载拖垮 LCP |
| 自定义字体 | `font-display: swap` 防 FOIT(文字空白闪烁) |
| 动态插入内容(广告/通知条) | 预留 `min-height` 空间,不向上挤压已有内容 |

## 反例

```tsx
function Hero({ cover }: { cover: string }) {
  // ❌ 裸 img 无尺寸:加载完瞬间撑开页面,下方内容被挤掉 → CLS 飙高
  // ❌ LCP 首屏大图给了 lazy:延迟解码,LCP 直接超 2.5s
  return <img src={cover} loading="lazy" alt="封面" />;
}
```

## 正例

```tsx
import { Skeleton } from "antd";

const HERO_RATIO = "16 / 9"; // 封面等比占位,加载前后高度恒定

function Hero({ cover, loaded }: { cover: string; loaded: boolean }) {
  // 加载态:骨架占位尺寸贴合真实封面比例,不跳动
  if (!loaded) {
    return <Skeleton.Image active style={{ width: "100%", aspectRatio: HERO_RATIO }} />;
  }

  // 数据态:LCP 首屏大图用 fetchPriority 抢优先级,禁 lazy;aspect-ratio 先占位
  return (
    <img
      src={cover}
      alt="封面"
      fetchPriority="high"
      decoding="async"
      style={{ width: "100%", aspectRatio: HERO_RATIO, objectFit: "cover" }}
    />
  );
}
```

```tsx
function VideoEmbed({ src }: { src: string }) {
  // iframe 必设等比占位,避免加载后撑高布局
  return (
    <div style={{ width: "100%", aspectRatio: "16 / 9" }}>
      <iframe src={src} title="视频" style={{ width: "100%", height: "100%", border: 0 }} />
    </div>
  );
}
```

```css
/* 自定义字体 swap 防 FOIT:先用兜底字体渲染,字体到位再换,不空白 */
@font-face {
  font-family: "AppSans";
  src: url("/fonts/app-sans.woff2") format("woff2");
  font-display: swap;
}
```

> 列表懒加载的非首屏图片可保留 `loading="lazy"`;仅首屏 LCP 候选图禁懒加载。

## 自检

- [ ] 图片 / 视频 / iframe 都设了固定 `width`+`height` 或 `aspect-ratio` 占位?
- [ ] 首屏 LCP 大图没有 `loading="lazy"`,且加了 `fetchPriority="high"`?
- [ ] 骨架占位尺寸 ≈ 真实内容,加载前后高度恒定?
- [ ] 自定义字体加了 `font-display: swap` 防 FOIT?
- [ ] 动态插入内容预留了 `min-height`,不挤压已有布局?
- [ ] Lighthouse CLS < 0.1、LCP < 2.5s、INP < 200ms?

## 相关

- 父:[`./index.md`](./index.md)
- 兄弟:[`code-splitting.md`](./code-splitting.md)(拆包优化 LCP 首屏 bundle)
- 跨引:[`../feedback/skeleton-loading.md`](../feedback/skeleton-loading.md)(骨架屏房规,占位尺寸贴合真实内容防跳动)
