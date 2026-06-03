---
name: antd-navigation-selection
description: antd 导航组件 Tabs / Steps / Menu / Breadcrumb 按视图关系选型。Use when 在 Tabs 与 Steps 间纠结要不要按序 / 不确定用 Menu 还是 Tabs 承载导航 / 给页面加面包屑路径 / 多步流程选错组件想纠偏。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
triggers:
  keywords:
  - Tabs
  - Steps
  - Menu
  - Breadcrumb
  - 导航选型
  - 标签页
  - 步骤条
  - antd navigation
effort: low
context: inline
version: '1.0'
---

# antd · 导航组件选型

## 规则

决策点：**视图之间是什么关系**——这决定用哪个导航组件。

| 视图关系 | 选型 | 判据 |
|----------|------|------|
| 平级视图、同层、顺序自由 | `Tabs` | 用户可任意顺序看，互不依赖 |
| 有序线性、多步、带进度 | `Steps` | 必须按序完成，前一步定后一步 |
| 站点/应用层级区块、常驻 | `Menu` | 路由级导航，侧栏或顶栏 |
| "你在这"的路径轨迹 | `Breadcrumb` | 显示当前层级位置，可回溯 |

`Breadcrumb` 与 `Menu` **互补非互斥**:`Menu` 选区块、`Breadcrumb` 标位置,常组合使用。

- **Tabs vs Steps**:顺序无关 → `Tabs`;须按序完成 → `Steps`。
- **Menu vs Tabs**:应用路由级导航(切页面/区块)→ `Menu`;页内内容分区(同页切视图)→ `Tabs`。
- **Breadcrumb 通常与 Menu 组合**,而非二选一。

### 反例:用 Steps 承载无序设置组

```tsx
// 反例：基础/通知/安全 三组设置彼此独立、顺序无关，却用 Steps 逼用户"按序"
<Steps current={current} items={[{ title: '基础' }, { title: '通知' }, { title: '安全' }]} />
```

### 正例:无序分组用 Tabs、有序流程用 Steps、路由用 Menu+Breadcrumb

```tsx
import { Tabs, Steps, Menu, Breadcrumb } from 'antd';
import { buildSettingTabs } from './converters/settingNav';
import { useCheckoutFlow } from './hooks/useCheckoutFlow';

// 无序设置组：互不依赖，用 Tabs 让用户随意切
function SettingsPanel() {
  // 步骤一：把设置分组配置转成 Tabs items（>3 行转换下沉 converter）
  const items = buildSettingTabs();
  // 步骤二：渲染标签页，默认停在第一组
  return <Tabs defaultActiveKey="basic" items={items} />;
}

// 有序结算流程：须按序完成，用 Steps 表达进度
function CheckoutFlow() {
  // 步骤一：从 hook 拿当前步索引与步骤定义（编排只取值，逻辑在 hook 内）
  const { current, items } = useCheckoutFlow();
  // 步骤二：渲染步骤条，current 驱动进度高亮
  return <Steps current={current} items={items} />;
}

// 应用路由导航：Menu 选区块 + Breadcrumb 标位置，二者组合
function AppShell({ menuItems, crumbItems, activeKey }: AppShellProps) {
  // 步骤一：侧栏 Menu 承载路由级区块切换
  const sider = <Menu mode="inline" selectedKeys={[activeKey]} items={menuItems} />;
  // 步骤二：顶部 Breadcrumb 标出"你在这"的路径轨迹
  const crumb = <Breadcrumb items={crumbItems} />;
  // 步骤三：平坦组合，Menu 与 Breadcrumb 互补呈现
  return (
    <>
      {crumb}
      {sider}
    </>
  );
}
```

## 自检

- [ ] 视图顺序自由用了 `Tabs`,而非 `Steps`
- [ ] 多步且须按序完成才用 `Steps`,无序分组改回 `Tabs`
- [ ] 路由级/区块级导航用 `Menu`,页内同页切视图用 `Tabs`,没有混用
- [ ] `Breadcrumb` 作为路径轨迹与 `Menu` 组合,没有当成 `Menu` 的替代二选一
- [ ] 转换/取值逻辑下沉到 converter / hook,组件体只做编排

## 相关

- 父:[`./index.md`](./index.md)
- 兄弟:[`./overlay-selection.md`](./overlay-selection.md)(弹出层选型)、[`./data-display-selection.md`](./data-display-selection.md)(数据展示选型)
- 跨引:[`../../react/component/folder-layering.md`](../../react/component/folder-layering.md)(导航壳与页面组件的目录分层)
