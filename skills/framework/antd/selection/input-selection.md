---
name: antd-input-selection
description: antd 输入/选择控件选型，按互斥性·候选项数·层级在单选多选层级三类组件间收敛。Use when 挑字段采集控件 / 单选多选纠结 / Radio 太多想换 Select / Switch 与 Checkbox 选不定 / 树形层级选值。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
triggers:
  keywords:
  - Select
  - Radio
  - Segmented
  - Switch
  - Checkbox
  - Cascader
  - TreeSelect
  - AutoComplete
  - showSearch
  - 单选
  - 多选
  - 候选项
  - 选型
effort: medium
context: inline
version: '1.0'
---
# antd · 输入/选择控件选型

## 规则

决策点：先定**单选 / 多选 / 层级**，再按**候选项数量**和**是否即时生效**收敛到具体组件。

| 形态 | 条件 | 选 | 备注 |
|------|------|-----|------|
| 单选 | ≤2 互斥 + 即时副作用 | `Switch` | 开关立即生效，无需提交 |
| 单选 | ≤5 互斥 + 需全部可见 | `Radio` / `Segmented` | 表单字段→Radio；工具栏视图切换+短标签→Segmented |
| 单选 | 5–20 | `Select` | 收起为下拉省空间 |
| 单选 | >20 | `Select showSearch` / `AutoComplete` | 受限选项集→Select；允许自由文本→AutoComplete |
| 多选 | 少且需全部可见 | `Checkbox.Group` | 随表单提交 |
| 多选 | 多 | `Select mode="multiple"` / `mode="tags"` | tags 允许新增自定义项 |
| 层级 | 单路径树 | `Cascader` | 一次选一条路径 |
| 层级 | 树任意多选 | `TreeSelect` | `treeCheckable` 跨层勾选 |

近义辨析：
- **Radio vs Segmented**：表单里的互斥字段用 Radio；纯前端视图/列表/图表切换用 Segmented（短标签、无 name 提交语义）。
- **Switch vs Checkbox**：触发即时副作用（开关通知、启停服务）用 Switch；值随表单一起提交用 Checkbox。
- **AutoComplete vs Select showSearch**：允许用户输入选项外的自由文本用 AutoComplete；只能从受限集合选用 Select showSearch。

## 反例 → 正例

```tsx
// ❌ 30 个互斥城市硬塞 Radio —— 占满整屏、扫描成本爆炸
<Radio.Group options={cityOptions} />   // cityOptions.length === 30

// ✅ >20 项收起为可搜索下拉
import { Select } from "antd";

function CityField({ cityOptions }: { cityOptions: { value: string; label: string }[] }) {
  // 选项标准化为 antd options 形态
  const options = cityOptions;
  // 候选 >20 → showSearch + 拼音/子串过滤，收起省空间
  return (
    <Select
      showSearch
      placeholder="选择城市"
      options={options}
      optionFilterProp="label"
      style={{ width: 240 }}
    />
  );
}
```

```tsx
// ✅ 工具栏视图切换：短标签 + 即时切，用 Segmented（非表单字段）
import { Segmented } from "antd";
import { useState } from "react";

function ViewToolbar() {
  // 视图态由本地 state 持有，不进 Form
  const [view, setView] = useState<"list" | "grid" | "kanban">("list");
  // Segmented 切换即时生效，回调里只更新视图态
  return (
    <Segmented
      value={view}
      onChange={(v) => setView(v as typeof view)}
      options={[
        { value: "list", label: "列表" },
        { value: "grid", label: "网格" },
        { value: "kanban", label: "看板" },
      ]}
    />
  );
}
```

```tsx
// ✅ 即时副作用用 Switch（开关立即落库，非随表单提交）
import { Switch, App } from "antd";

function NotifyToggle({ enabled, onToggle }: { enabled: boolean; onToggle: (v: boolean) => Promise<void> }) {
  const { message } = App.useApp();
  // 切换即调用副作用，失败由调用方抛出后提示
  const handleChange = async (next: boolean) => {
    await onToggle(next);
    message.success(next ? "已开启通知" : "已关闭通知");
  };
  return <Switch checked={enabled} onChange={handleChange} />;
}
```

## 自检

- [ ] 先分清单选 / 多选 / 层级，再按数量收敛？
- [ ] 互斥项 >20 没硬塞 Radio，改用 Select showSearch？
- [ ] 视图切换用 Segmented、表单互斥字段用 Radio，没混用？
- [ ] 即时副作用用 Switch、随表单提交用 Checkbox？
- [ ] 允许自由文本才用 AutoComplete，受限集合用 Select？
- [ ] 单路径层级用 Cascader、跨层多选用 TreeSelect？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`overlay-selection.md`](./overlay-selection.md)
- 表单字段名规约（Radio/Checkbox/Select 进 Form 时）：[`../form/form-item-name.md`](../form/form-item-name.md)
