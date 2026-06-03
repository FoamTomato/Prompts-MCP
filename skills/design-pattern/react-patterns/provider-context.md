---
name: design-pattern-react-provider-context
description: "用 Context + 封装 Provider 跨多层共享低频变更全局值(主题/locale/用户),按变更频率拆分。Use when 跨层级共享主题或登录态 / prop 透传太痛苦 / 高频值放 Context 致全量重渲染。"
parent: ./index.md
paths:
- frontend/src/**/*.tsx
triggers:
  keywords:
  - Context
  - Provider
  - createContext
  - useContext
  - prop drilling
  - 跨层级共享
  - 低频变更
  - 主题 locale
  - 当前用户
effort: medium
context: inline
version: '1.0'
---
# Design Pattern · React Provider/Context

## 规则

决策点:**只有"低频变更的全局值"才进 Context**。

| 值的特征 | 例子 | 放哪 |
|---------|------|------|
| 低频变更、跨多层共享 | 主题 / locale / 当前用户 / 权限 / 表单聚合状态 | Context + 封装 Provider |
| 高频变更(每次输入/拖拽/滚动) | 输入框文本、画布坐标、滚动位置 | 拆细 Context 或 [Zustand](../../framework/react/state/client-state-zustand.md)(selector 精准订阅) |
| 局部、单组件内 | 折叠开关、hover | `useState` 就地持有 |

> Context value 一变,**所有消费者重渲染**。高频值塞 Context 会拖垮整棵子树。
> 同一 Context 内不同频率的值要**按变更频率拆成多个 Context**,各自独立刷新。

封装铁律:对外只暴露 `<XxxProvider>` + `useXxxContext()`,**不导出裸 Context**;读取 hook 内校验"是否在 Provider 内"。

## 反例:所有状态塞一个 Context

```tsx
// ❌ 主题(低频)和草稿文本(每次输入都变)挤同一个 Context
const AppContext = createContext<any>(null);
// theme 没变,但 draft 一变 → 全部消费者(含只读 theme 的组件)重渲染
<AppContext.Provider value={{ theme, setTheme, draft, setDraft }}>
```

## 正例:按变更频率拆 Context + 自定义读取 hook

```tsx
// src/contexts/theme.tsx —— 低频:主题
import { createContext, useContext, useMemo, useState, type ReactNode } from "react";
import { resolveTheme } from "./theme.utils"; // >3 行的派生逻辑下沉纯函数

interface ThemeContextValue {
  mode: "light" | "dark";
  toggle: () => void;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  // 1. 持有低频状态
  const [mode, setMode] = useState<"light" | "dark">("light");
  // 2. 稳定的更新函数
  const toggle = () => setMode((m) => (m === "light" ? "dark" : "light"));
  // 3. value 用 useMemo,避免父级重渲染时引用变化触发下游
  const value = useMemo<ThemeContextValue>(() => resolveTheme(mode, toggle), [mode]);
  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

// 4. 读取 hook 内校验:脱离 Provider 直接抛错,而非静默 null
export function useThemeContext(): ThemeContextValue {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useThemeContext 必须在 <ThemeProvider> 内使用");
  return ctx;
}
```

```tsx
// 高频草稿文本走独立通道(拆分 Context 或 Zustand),不污染 ThemeContext
const draft = useDraftStore((s) => s.draft);   // selector 精准订阅,只重渲染用到 draft 的组件
const theme = useThemeContext();               // theme 不变 → 此组件不因 draft 变化重渲染
```

Provider 组合在应用根挂载,顺序由外到内按依赖排列:

```tsx
// src/App.tsx —— 一步一注释,读注释即读装配流程
export function App() {
  // 1. 主题最外层(全站可见)
  // 2. 当前用户(部分页面依赖)
  // 3. i18n
  return (
    <ThemeProvider>
      <CurrentUserProvider>
        <LocaleProvider>
          <Routes />
        </LocaleProvider>
      </CurrentUserProvider>
    </ThemeProvider>
  );
}
```

## 自检

- [ ] 进 Context 的值是"低频变更"?高频(每次输入)的拆出去或用 Zustand?
- [ ] 不同变更频率的值已拆成独立 Context,而非挤一个?
- [ ] value 用 `useMemo` 包裹,引用稳定?
- [ ] 只导出 `<XxxProvider>` + `useXxxContext()`,裸 Context 没外泄?
- [ ] 读取 hook 内校验"在 Provider 内",脱离时抛错?

## 相关

- 父:[`./index.md`](./index.md)
- 兄弟:[`./compound-components.md`](./compound-components.md)(复合组件用 Context 做父子隐式协作)
- 高频客户端状态:[`../../framework/react/state/client-state-zustand.md`](../../framework/react/state/client-state-zustand.md)
