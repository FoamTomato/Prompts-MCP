---
name: react-compound-components
description: "复合组件 — 一组协作组件经 Context 共享父级隐式状态、暴露 <Tabs.Tab> 式声明组合 API。Use when 设计 Tabs/Accordion/Menu/Select 等父统筹多子项组件 / 配置 props 膨胀成 prop soup / 想让调用方自由组合子项时。"
parent: ./index.md
paths:
- frontend/src/**/*.tsx
triggers:
  keywords:
  - 复合组件
  - 组合式 API
  - prop soup
  - compound components
  - Tabs.Tab
  - createContext
  - useContext
  - 静态属性挂载
effort: high
context: inline
version: '1.0'
---
# Design Pattern · React 复合组件

## 规则

决策点:**这组组件是否「父统筹 + 多个可变子项」且需调用方自由组合**。是则用复合组件(父经 Context 隐式共享状态,子声明式排布);否则别上,避免过度设计。

| 信号 | 选择 |
|------|------|
| Tabs/Accordion/Menu/Select 等父管激活态、子项数量/顺序由调用方定 | 复合组件 |
| 子项要插自定义内容、夹分隔符、条件渲染某些项 | 复合组件(声明式天然支持) |
| 配置 props 已超 ~5 个 / 出现 `items=[{...}]` + 一堆 `renderXxx` 回调 | 复合组件替代 prop soup |
| 无子项变化、纯展示、props ≤ 3 个 | 普通组件,别上 |

实现三件套:① 父 `createContext` 提供状态与操作;② 子 `useContext` 读、缺 Provider 时 throw;③ 父挂静态属性 `Tabs.Tab = Tab` 暴露组合 API。状态共享是隐式的——调用方不手动透传 props 给子项。

## 反例 · 正例

```tsx
// ❌ prop soup:30 个配置 props 描述子项,加一种子项就改 props,无法自由组合
<Tabs
  items={[{ key: 'a', label: '基础', content: <A /> }]}
  activeKey={key}
  onChange={setKey}
  tabBarGutter={8}
  renderTabBar={...}
  renderTabContent={...}
  /* ...还有 24 个 prop... */
/>
```

```tsx
// ✅ 父:Context 共享激活态,缺 Provider 即报错
interface TabsCtx { activeKey: string; setActiveKey: (k: string) => void }
const TabsContext = createContext<TabsCtx | null>(null);

// 子组件统一从此 hook 取上下文,把"漏用 Provider"变成显式错误
const useTabsContext = (): TabsCtx => {
  const ctx = useContext(TabsContext);
  if (!ctx) throw new Error('Tabs.* 必须用在 <Tabs> 内');
  return ctx;
};

const Tabs = ({ defaultKey, children }: { defaultKey: string; children: ReactNode }) => {
  // 父持有唯一激活态
  const [activeKey, setActiveKey] = useState(defaultKey);
  // 上下文值 memo 化,避免每次 render 让所有子项重渲
  const value = useMemo<TabsCtx>(() => ({ activeKey, setActiveKey }), [activeKey]);
  // 经 Provider 隐式下发,子项无需手动接 props
  return <TabsContext.Provider value={value}>{children}</TabsContext.Provider>;
};
```

```tsx
// ✅ 子:useContext 读隐式状态,自身只管"我是否激活"
const Tab = ({ tabKey, children }: { tabKey: string; children: ReactNode }) => {
  // 从父上下文读激活态与切换方法
  const { activeKey, setActiveKey } = useTabsContext();
  // 派生当前项是否激活(纯计算,直接内联)
  const active = activeKey === tabKey;
  return (
    <button data-active={active} onClick={() => setActiveKey(tabKey)}>
      {children}
    </button>
  );
};

// ✅ 父挂静态属性,对外暴露声明式组合 API
Tabs.Tab = Tab;

// 调用方:自由组合、夹任意内容、条件渲染——无 prop soup
<Tabs defaultKey="a">
  <Tabs.Tab tabKey="a">基础</Tabs.Tab>
  <Tabs.Tab tabKey="b">进阶</Tabs.Tab>
</Tabs>
```

## 自检

- [ ] 这组组件确是「父统筹 + 多可变子项 + 调用方自由组合」,而非可被 ≤3 props 普通组件解决?
- [ ] 父用 Context 隐式共享状态,子用 `useContext` 读,而非把状态手动 props 透传给每个子项?
- [ ] 子组件读上下文经统一 hook 且缺 Provider 时 throw,而非裸 `useContext` 拿到 null 后静默?
- [ ] Provider 的 value 已 `useMemo`,未每次 render 新建对象引发全体子项重渲?
- [ ] 静态属性 `Parent.Child = Child` 暴露,而非靠调用方各处 import 散装子组件?

## 相关

- 父:[`./index.md`](./index.md)
- 状态共享底座(本模式的 Context 用法):[`./provider-context.md`](./provider-context.md)
- 子项内部组织/命名等组件结构规约:[`../../framework/react/component/structure.md`](../../framework/react/component/structure.md)
