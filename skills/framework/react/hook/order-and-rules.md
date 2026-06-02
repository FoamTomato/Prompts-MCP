---
name: react-hook-order-and-rules
description: Hooks 调用顺序：state → ref → derived(useMemo) → effect → animation → callback。Use
  when 写 React 组件 / 改 .tsx 文件 / 评审涉及 `order-and-rules` 的 PR。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/hooks/**/*.ts
triggers:
  keywords:
  - useState
  - useRef
  - useEffect
  - useMemo
  - useCallback
  - 调用顺序
effort: medium
context: inline
version: '1.0'
---
# React · Hooks 顺序与规则

## 标准顺序

```tsx
function MyComponent(props: Props) {
  // 1. state
  const [hovered, setHovered] = useState(false);
  const [zoom, setZoom] = useState(1);

  // 2. ref
  const containerRef = useRef<HTMLDivElement>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  // 3. derived (useMemo / 自定义 hook 返回值)
  const subtitle = useMemo(
    () => `${props.subject} · ${props.grade}`,
    [props.subject, props.grade]
  );
  const { data, isLoading } = useQuery(...);

  // 4. effect
  useEffect(() => {
    // 仅 DOM 同步 / 订阅 / 清理
    return () => timerRef.current && clearTimeout(timerRef.current);
  }, []);

  // 5. animation (useGSAP)
  useGSAP(() => {
    gsap.to(containerRef.current, { scale: zoom, duration: D.micro });
  }, { scope: containerRef, dependencies: [zoom] });

  // 6. callback (useCallback / handlers)
  const handleClick = useCallback(() => {
    setHovered(true);
  }, []);

  // 7. render
  return <div ref={containerRef} onClick={handleClick}>...</div>;
}
```

## React 三铁律

1. **顶层调用**：不在循环 / 条件 / 嵌套函数里
2. **只在 React 函数内**：组件 / 自定义 hook
3. **依赖完整**：useEffect / useMemo / useCallback 的依赖数组**必须列出所有引用的外部变量**

## 反例

```tsx
// ❌ 条件调用
function Bad({ flag }) {
  if (flag) {
    const [x] = useState(0);   // ❌
  }
}

// ❌ 依赖不完整
useEffect(() => {
  fetch(`/api/users/${userId}`);
}, []);   // userId 未列入 → 永远用第一次的 userId

// ❌ useEffect 拉数据
useEffect(() => {
  fetch("/api/users").then(setUsers);   // 用 useQuery
}, []);
```

## ESLint 强制

```json
{
  "rules": {
    "react-hooks/rules-of-hooks": "error",
    "react-hooks/exhaustive-deps": "error"
  }
}
```

## 自检

- [ ] Hook 都在顶层（无条件 / 循环）？
- [ ] 依赖数组完整？
- [ ] 顺序：state → ref → derived → effect → animation → callback？
- [ ] useEffect 不拉数据（用 useQuery）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`custom-hook-naming.md`](./custom-hook-naming.md) · [`no-fetch-in-use-effect.md`](./no-fetch-in-use-effect.md)

