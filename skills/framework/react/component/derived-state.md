---
name: react-derived-state
description: 派生值渲染期直接算 — 能从 props/已有 state 推出的值别存 useState 再 useEffect 同步。Use when 写 React 组件 /
  改 .tsx 文件 / 见到 useState+useEffect 同步衍生值 / 评审 `derived-state` 的 PR。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - 派生值
  - derived state
  - useMemo
  - 渲染期计算
  - useState
  - 同步
effort: medium
context: inline
version: '1.0'
---
# React · 派生值渲染期算

## 规则

**决策点：能从 props 或已有 state 算出来的值，渲染期直接算，不另存 useState + useEffect 同步。**

| 这个值… | 怎么处理 |
|---------|---------|
| 能由 props / 已有 state 推出 | 渲染期直接算（const） |
| 推算 >3 行 / 遍历大数组 / 开销大 | 用 `useMemo` 缓存 |
| 需被用户编辑后脱离来源 props | 才用 `useState`；props 变要重置则给组件加 `key` 重挂 |

冗余 state + useEffect 同步会引入额外一次渲染、容易漏更新、来源与副本不一致。

## 反例 → 正例

```tsx
// ❌ 派生值存 state + useEffect 同步：多一次渲染、易漂移
function NameCard({ first, last }: { first: string; last: string }) {
  const [full, setFull] = useState("");
  useEffect(() => {
    setFull(first + " " + last);
  }, [first, last]);
  return <span>{full}</span>;
}

// ✅ 渲染期直接算
function NameCard({ first, last }: { first: string; last: string }) {
  // 派生值：拼全名，渲染期算
  const full = `${first} ${last}`;
  return <span>{full}</span>;
}
```

```tsx
// ✅ 贵的派生用 useMemo（filter + sort 遍历大数组）
function ArticleTable({ articles, keyword }: ArticleTableProps) {
  // 派生值：按关键词过滤再按更新时间倒序，依赖变才重算
  const visible = useMemo(
    () => filterAndSortArticles(articles, keyword),
    [articles, keyword],
  );
  return <Table dataSource={visible} rowKey="id" columns={columns} />;
}

// >3 行的转换下沉到纯函数
function filterAndSortArticles(list: Article[], keyword: string): Article[] {
  return list
    .filter((it) => it.title.includes(keyword))
    .sort((a, b) => dayjs(b.updatedAt).valueOf() - dayjs(a.updatedAt).valueOf());
}
```

## 何时确实需要 state

仅当值需被用户编辑、从此脱离 props 独立演化（如把 props 当草稿初始值）。此时若 props 变要丢弃旧编辑、重置为新初值，**不要在 useEffect 里 setState 同步**，改用 `key` 触发重挂：

```tsx
// 父层：换条目就换 key，子组件连同内部草稿 state 整体重挂、自然重置
<DraftEditor key={article.id} initialTitle={article.title} />

function DraftEditor({ initialTitle }: { initialTitle: string }) {
  // 用户可编辑、脱离 props：才用 useState，initialTitle 仅作初值
  const [title, setTitle] = useState(initialTitle);
  return <Input value={title} onChange={(e) => setTitle(e.target.value)} />;
}
```

## 自检

- [ ] 没有"useState + useEffect 同步"来维护能从 props/state 算出的值？
- [ ] 简单派生用 const 渲染期直接算？
- [ ] 贵的派生（遍历/排序/大计算）才上 useMemo，依赖数组准确？
- [ ] >3 行的转换下沉到纯函数，组件体只做编排？
- [ ] 受控初值需随 props 重置时，用 `key` 重挂而非 useEffect setState？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`state-completeness.md`](./state-completeness.md)
- 边界呼应：[`../hook/no-fetch-in-use-effect.md`](../hook/no-fetch-in-use-effect.md)
