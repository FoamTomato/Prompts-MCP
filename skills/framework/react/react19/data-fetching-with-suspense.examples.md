# use() + Suspense + ErrorBoundary 完整样例

```tsx
import { use, Suspense, createContext, type ReactNode } from "react";
import { ErrorBoundary } from "react-error-boundary";

// ── 上游：promise 在渲染体外稳定创建并缓存（loader / 父层 / 模块级），绝不在子组件渲染里新建 ──
const userPromiseCache = new Map<number, Promise<User>>();

// 建/取一个稳定 promise（同 id 复用，避免每渲染新 promise → 无限 pending）
function getUserPromise(userId: number): Promise<User> {
  // 命中缓存直接返回稳定引用
  const cached = userPromiseCache.get(userId);
  if (cached) return cached;
  // 未命中：建一次、存一次
  const promise = fetch(`/api/users/${userId}`).then(r => r.json() as Promise<User>);
  userPromiseCache.set(userId, promise);
  return promise;
}

// context 也可被 use() 条件读出
const FeatureFlagContext = createContext<{ debug: boolean }>({ debug: false });

// ── 叶子组件：只用 use() 同步读出上游 promise，不关心 loading/error 样板 ──
function UserCard({ userPromise }: { userPromise: Promise<User> }) {
  // 条件读 context：use() 是 Hook 顺序规则的唯一例外，允许写在 if 之后
  const flags = use(FeatureFlagContext);
  if (flags.debug) {
    // 此分支内再 use 一个值也合法
    console.debug("rendering UserCard in debug mode");
  }
  // 同步读出 promise：pending → 抛给 Suspense；reject → 抛给 ErrorBoundary
  const user = use(userPromise);
  return (
    <article className="user-card">
      <h3>{user.name}</h3>
      <p>{user.email}</p>
    </article>
  );
}

// ── 边界编排：Suspense 接 pending，ErrorBoundary 接 reject，二者成对出现 ──
function UserPanel({ userId }: { userId: number }) {
  // 第一步：取稳定 promise（外层创建，传给叶子，叶子内不再新建）
  const userPromise = getUserPromise(userId);
  // 第二步：reject 兜底（外）+ pending 兜底（内），缺一则未处理态会冒泡到上层
  return (
    <ErrorBoundary fallbackRender={({ error, resetErrorBoundary }) => (
      <UserErrorFallback error={error} onRetry={resetErrorBoundary} />
    )}>
      <Suspense fallback={<UserCardSkeleton />}>
        <UserCard userPromise={userPromise} />
      </Suspense>
    </ErrorBoundary>
  );
}

// ── reject 兜底：纯展示，重试即重置边界（promise 失效后由上游重建） ──
function UserErrorFallback({ error, onRetry }: { error: Error; onRetry: () => void }) {
  return (
    <div role="alert" className="user-error">
      <p>加载失败：{error.message}</p>
      <button type="button" onClick={onRetry}>重试</button>
    </div>
  );
}

function UserCardSkeleton() {
  return <div className="user-card skeleton" aria-busy="true" />;
}

interface User {
  id: number;
  name: string;
  email: string;
}
```

```tsx
// ── 列表场景：每个子项各自一对 Suspense/ErrorBoundary，互不阻塞（用 map，不手写 for） ──
function UserGrid({ userIds }: { userIds: number[] }) {
  // 每个 id 独立成边界：某一项失败/挂起不连累其余项
  return (
    <div className="user-grid">
      {userIds.map(id => (
        <UserPanel key={id} userId={id} />
      ))}
    </div>
  );
}
```

```tsx
// ── 与 TanStack Query 协作：取数仍归 query 层，use() 不替代它 ──
import { useSuspenseQuery } from "@tanstack/react-query";

function TextbookList() {
  // 服务端数据交给 useSuspenseQuery：缓存/去重/retry/失效全由 query 层负责，并接入 Suspense
  const { data } = useSuspenseQuery({
    queryKey: ["textbooks"],
    queryFn: () => textbooksApi.list(),
  });
  // 组件体只做编排：渲染列表
  return data.map(tb => <TextbookCard key={tb.id} textbook={tb} />);
}

// 外层同样需要 Suspense + ErrorBoundary 成对包裹（与上面 UserPanel 同形，此处略）
```
