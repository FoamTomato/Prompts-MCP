# React · 异步竞态与请求取消 · 完整示例

> 两种解法各一份完整可运行写法。自写 fetch 时二选一即可；首选仍是 TanStack Query。

## 方案 A · useEffect + AbortController 真取消

适用：取数由依赖（关键词 / 页码）驱动，希望旧请求在网络层就被中断。

```tsx
import { useEffect, useState } from "react";
import { Input, List } from "antd";

interface Item {
  id: string;
  title: string;
}

// 取数下沉为纯函数：接收 signal，旧请求被 abort 后这里会抛 AbortError
async function fetchSearch(keyword: string, signal: AbortSignal): Promise<Item[]> {
  const res = await fetch(`/api/search?kw=${encodeURIComponent(keyword)}`, { signal });
  return res.json();
}

export function SearchBox() {
  const [keyword, setKeyword] = useState("");
  const [list, setList] = useState<Item[]>([]);

  useEffect(() => {
    // 空关键词不发请求，早返回
    if (!keyword) {
      setList([]);
      return;
    }

    // 为本次请求建专属 controller
    const controller = new AbortController();

    // 取数：拿到结果才 setState；被取消时进 catch 不动状态
    fetchSearch(keyword, controller.signal)
      .then(setList)
      .catch((err) => {
        // 被新输入取消的请求抛 AbortError，静默忽略，保留最新结果
        if (err.name !== "AbortError") throw err;
      });

    // cleanup：依赖变化或卸载时中断上一次请求，网络层真取消
    return () => controller.abort();
  }, [keyword]);

  return (
    <>
      <Input value={keyword} onChange={(e) => setKeyword(e.target.value)} placeholder="搜索" />
      <List dataSource={list} renderItem={(it) => <List.Item key={it.id}>{it.title}</List.Item>} />
    </>
  );
}
```

## 方案 B · stale-result guard 忽略非最新响应

适用：底层 SDK 不支持 AbortSignal，或滚动翻页这类无法取消但能比对序号的场景。

```tsx
import { useRef, useState, useCallback } from "react";
import { Button, List } from "antd";

interface Item {
  id: string;
  title: string;
}

// 取数下沉：返回某一页数据，page2 可能晚于 page3 到达
async function fetchPage(page: number): Promise<Item[]> {
  const res = await fetch(`/api/items?page=${page}`);
  return res.json();
}

export function InfiniteList() {
  const [list, setList] = useState<Item[]>([]);
  const [page, setPage] = useState(1);
  // 递增序号：每次请求自增，响应回来比对，只有最新序号的结果才采纳
  const seqRef = useRef(0);

  const loadMore = useCallback(async () => {
    // 计算下一页页码
    const nextPage = page + 1;
    // 本次请求领一个递增序号，并记为当前最新
    const mySeq = ++seqRef.current;
    // 取数
    const items = await fetchPage(nextPage);
    // 守卫：若期间已有更新的请求发出，本次为陈旧结果，丢弃
    if (mySeq !== seqRef.current) return;
    // 采纳：追加新一页并推进页码
    setList((prev) => [...prev, ...items]);
    setPage(nextPage);
  }, [page]);

  return (
    <>
      <List dataSource={list} renderItem={(it) => <List.Item key={it.id}>{it.title}</List.Item>} />
      <Button onClick={loadMore}>加载更多</Button>
    </>
  );
}
```
