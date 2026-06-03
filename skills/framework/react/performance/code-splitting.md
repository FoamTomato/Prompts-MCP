---
name: react-code-splitting
description: 用 React.lazy + Suspense 动态 import 做路由级/重组件分包，配合 tree-shaking 把首屏 bundle 压到压缩后 <150KB。Use when 首屏白屏久 / bundle 体积超预算 / 引入图表富文本等重组件 / 排查全量 import 拖垮首屏。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - 代码分割
  - 懒加载
  - 首屏 bundle
  - React.lazy
  - Suspense
  - dynamic import
  - tree-shaking
  - lodash-es
  - 按需引入
effort: medium
context: inline
version: '1.0'
---
# React Performance · 代码分割与懒加载

## 规则

**决策点:这块代码该不该进首屏 bundle?** 不是首屏必需的就拆出去,首屏只留压缩后 <150KB(gzip) 的核心壳。

| 场景 | 处理 |
|------|------|
| 路由页面组件 | 一律 `lazy(() => import('./Page'))`,按路由分包,进哪个页才下载 |
| 重组件(图表/富文本/地图/PDF/二维码) | `lazy` 单独分包,首屏不引,用到再加载 |
| 首屏必现的轻组件 | 直接静态 import,别为拆而拆 |
| 工具库引用 | tree-shaking:用 `lodash-es` 而非 `lodash`;图标/组件按需具名引入,禁整库 `import * as` |

**tree-shaking 三条铁律**:① 工具库选 ESM 版本(`lodash-es`、`date-fns`)且只具名引入用到的函数;② 图标按路径具名引入 `import { UserOutlined } from '@ant-design/icons'`,不 `import * as Icons`;③ 任何 `import 整个库` 都会把全量打进 bundle。

每个 `lazy` 组件**必须**包在 `<Suspense>` 里:fallback 用 Skeleton 占位(见 [`../feedback/skeleton-loading.md`](../feedback/skeleton-loading.md)),分包下载失败需有 chunk 加载兜底(见 [`../reliability/chunk-load-recovery.md`](../reliability/chunk-load-recovery.md))。

## 反例 → 正例

```tsx
// ❌ 首屏全量静态 import:图表/编辑器/整个 lodash 全打进首屏 bundle
import { Line } from '@ant-design/charts';
import RichEditor from '@/components/RichEditor';
import _ from 'lodash';            // 整库进包,tree-shaking 失效
import * as Icons from '@ant-design/icons';  // 图标全量进包

export default function Dashboard() {
  // 首屏就被几百 KB 的图表+编辑器拖垮,白屏久
  const total = _.sumBy(rows, 'amount');
  return <><Line data={data} /><RichEditor /></>;
}
```

```tsx
// ✅ 重组件 lazy 分包 + Suspense 骨架兜底 + 按需具名引入
import { lazy, Suspense } from 'react';
import { Skeleton } from 'antd';
import { sumBy } from 'lodash-es';            // ESM 具名引入,只打这一个函数
import { UserOutlined } from '@ant-design/icons';  // 图标按需,不整库

// 重组件懒加载:单独分包,首屏不下载,赋值后不变用 const
const Chart = lazy(() => import('@/components/Chart'));
const RichEditor = lazy(() => import('@/components/RichEditor'));

export default function Dashboard({ rows, data }: DashboardProps) {
  // 纯计算下沉:>3 行的聚合走 utils,组件体只编排(此处一行直接用)
  const total = sumBy(rows, 'amount');
  // 编排:重组件各自包 Suspense,fallback 用 Skeleton 占位避免白屏
  return (
    <>
      <Statistic prefix={<UserOutlined />} value={total} />
      <Suspense fallback={<Skeleton active paragraph={{ rows: 6 }} />}>
        <Chart data={data} />
      </Suspense>
      <Suspense fallback={<Skeleton.Input active block />}>
        <RichEditor />
      </Suspense>
    </>
  );
}
```

```tsx
// ✅ 路由级分包:每个页面 lazy,外层一个 Suspense 兜全部路由切换
const HomePage = lazy(() => import('@/pages/Home'));
const ReportPage = lazy(() => import('@/pages/Report'));

const routes = [
  { path: '/', element: <HomePage /> },
  { path: '/report', element: <ReportPage /> },
].map((r) => ({ ...r, element: <Suspense fallback={<Skeleton active />}>{r.element}</Suspense> }));
```

## 自检

- [ ] 路由页面组件均用 `lazy(() => import(...))` 按路由分包,而非首屏静态 import?
- [ ] 图表/富文本/地图等重组件已 `lazy` 拆出首屏 bundle?
- [ ] 每个 `lazy` 都包在 `<Suspense>` 内,fallback 用 Skeleton 而非空白/小转圈?
- [ ] 工具库用 `lodash-es` 具名引入,无 `import _ from 'lodash'` / `import * as`?
- [ ] 图标按需具名引入,无整库 `import * as Icons`?
- [ ] 首屏 bundle 压缩后 <150KB(gzip),已用 bundle-analyzer 核对预算?
- [ ] 分包下载失败有 chunk 加载兜底(网络抖动/版本变更不白屏)?

## 相关

- 父:[`./index.md`](./index.md)
- 配套:[`../feedback/skeleton-loading.md`](../feedback/skeleton-loading.md)(Suspense fallback 用 Skeleton 占位)
- 配套:[`../reliability/chunk-load-recovery.md`](../reliability/chunk-load-recovery.md)(分包加载失败的兜底与重试)
- 正交:[`../component/re-render-minimization.md`](../component/re-render-minimization.md)(本层管加载/拆包量,re-render 管渲染次数 memo)
- 跨引:[`../../../lang/typescript/index.md`](../../../lang/typescript/index.md)(ESM 具名 import 是 tree-shaking 前提)
