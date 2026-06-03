---
name: react-custom-hook-extraction
description: "把可复用的有状态逻辑抽成 useXxx 自定义 hook,2025 复用首选,替代 HOC/render props。Use when 一组相关状态逻辑要跨组件复用 / 组件里 useState+useEffect 复制粘贴 / 想复用逻辑又不想加 DOM 包裹时。"
parent: ./index.md
paths:
- frontend/src/**/*.tsx
triggers:
  keywords:
  - 抽离 hook
  - useXxx
  - 逻辑复用
  - 跨组件复用
  - 有状态逻辑抽离
effort: medium
context: inline
version: '1.0'
---
# Design Pattern · 自定义 Hook 抽逻辑

## 规则

决策点:复用的是逻辑还是 UI?逻辑→抽 hook;UI→抽组件(两者不互斥但勿混)。

| 信号 | 动作 |
|------|------|
| 组件里出现"一组相关 `useState` + `useEffect` + 处理函数",且要在第 2 个组件复用 | 抽 `useXxx` hook |
| 只是一段 JSX/样式要复用,无私有状态 | 抽组件,不是 hook |
| 想包裹组件注入 props（HOC）/ 用函数子组件给数据（render props） | 优先改写为 hook：不加 DOM 包裹、组合自然、易单测 |
| hook 需要返回多个相关项 | 返回**对象**(命名清晰、可选取);仅一对值用**元组**(像 useState) |

命名 `useXxx`、文件 `useXxx.ts`,见 [`../../framework/react/hook/custom-hook-naming.md`](../../framework/react/hook/custom-hook-naming.md)。

## 反例:逻辑在组件里复制粘贴

```tsx
// ❌ 查询+防抖+取消逻辑直接堆在组件,第二个搜索框只能 Ctrl-C/V
function UserPanel() {
  const [keyword, setKeyword] = useState("");
  const [users, setUsers] = useState<User[]>([]);
  useEffect(() => {
    const ctrl = new AbortController();
    const timer = setTimeout(() => {
      fetch(`/api/users?q=${keyword}`, { signal: ctrl.signal })
        .then((r) => r.json())
        .then(setUsers);
    }, 300);
    return () => { clearTimeout(timer); ctrl.abort(); };
  }, [keyword]);
  return <SearchBox value={keyword} onChange={setKeyword} options={users} />;
}
```

## 正例:抽成 useUserSearch()

```tsx
// frontend/src/features/user/useUserSearch.ts —— 封装查询+防抖+取消
import { useEffect, useState } from "react";
import { fetchUsers } from "@/api/user";

interface UserSearch {
  keyword: string;
  setKeyword: (v: string) => void;
  users: User[];
  loading: boolean;
}

export function useUserSearch(debounceMs = 300): UserSearch {
  const [keyword, setKeyword] = useState("");
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // 前置:空关键词不发请求,清空结果早返回
    if (!keyword.trim()) {
      setUsers([]);
      return;
    }
    // 取消令牌:卸载或下次输入时中断在途请求
    const ctrl = new AbortController();
    // 防抖:停止输入 debounceMs 后才查询
    const timer = setTimeout(async () => {
      setLoading(true);
      // 查询:取数下沉 api 层纯函数,signal 透传以支持取消
      const list = await fetchUsers(keyword, ctrl.signal);
      setUsers(list);
      setLoading(false);
    }, debounceMs);
    return () => { clearTimeout(timer); ctrl.abort(); };
  }, [keyword, debounceMs]);

  // 返回对象:多个相关项,调用方按需解构
  return { keyword, setKeyword, users, loading };
}

// 组件只剩编排,逻辑零重复,换个搜索框直接复用同一 hook
function UserPanel() {
  const { keyword, setKeyword, users, loading } = useUserSearch();
  return <SearchBox value={keyword} onChange={setKeyword} options={users} loading={loading} />;
}
```

## 自检

- [ ] 复用的是有状态**逻辑**而非纯 UI?(纯 UI 应抽组件)
- [ ] hook 名以 `use` 开头、文件名一致?
- [ ] 副作用都在 `useEffect` 内、清理函数取消订阅/在途请求?
- [ ] 返回值形态正确?(多项→对象;一对→元组)
- [ ] 取数/复杂转换已下沉 api/utils 纯函数,hook 只编排,且无多余 DOM 包裹?

## 相关

- 父:[`./index.md`](./index.md) · 替代方案:[`./render-props-headless.md`](./render-props-headless.md)
- 命名规约:[`../../framework/react/hook/custom-hook-naming.md`](../../framework/react/hook/custom-hook-naming.md)
- Hook 用法侧:[`../../framework/react/hook/index.md`](../../framework/react/hook/index.md)
