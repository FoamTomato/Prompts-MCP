# 参考 · 控件 → 必需 ARIA 矩阵

总原则：原生语义元素自带的 role / 状态**不要重复声明**；矩阵只列「自研壳层或原生无法表达时」必须补的属性。**no ARIA 好过 bad ARIA**。

## 原生语义元素（首选，自带语义，无需 ARIA）

| 元素 | 隐含 role | 自带能力 |
|------|----------|---------|
| `<button>` | button | 键盘 Enter/Space 触发、焦点 |
| `<a href>` | link | 键盘 Enter 跳转、焦点 |
| `<nav>` | navigation | 地标 |
| `<main>` | main | 地标（每页唯一） |
| `<header>`/`<footer>` | banner / contentinfo | 地标 |
| `<ul>`/`<ol>`/`<li>` | list / listitem | 列表语义、条目计数 |
| `<label htmlFor>` | — | 关联控件、点击聚焦 |
| `<table>`/`<th>` | table / columnheader | 行列关系 |

## 自研控件 → 必需 ARIA

| 控件 | role | 必需状态/属性 | 备注 |
|------|------|--------------|------|
| 开关 / toggle | （button 即可省 role） | `aria-pressed={bool}` | 优先用 `<button>` |
| 复选 toggle | `checkbox` | `aria-checked={bool}` `tabindex=0` | 原生 `<input type=checkbox>` 更佳 |
| tablist 容器 | `tablist` | `aria-orientation` | |
| tab 项 | `tab` | `aria-selected={bool}` `aria-controls={panelId}` | |
| tabpanel | `tabpanel` | `aria-labelledby={tabId}` | |
| 下拉菜单触发器 | `button` | `aria-haspopup="menu"` `aria-expanded={bool}` | |
| 菜单 / 菜单项 | `menu` / `menuitem` | — | |
| 模态对话框 | `dialog` | `aria-modal="true"` `aria-labelledby` | antd Modal 自带 |
| 提示/警告条 | `alert` 或 `aria-live="assertive"` | — | 打断式播报 |
| 异步更新区 | — | `aria-live="polite"` | 不打断，读完当前再播 |
| 进度 | `progressbar` | `aria-valuenow/min/max` | |
| 禁用态 | 原生用 `disabled`；ARIA 控件用 `aria-disabled` | | |

## 图片 alt 决策

| 图片用途 | alt 写法 |
|----------|---------|
| 传达信息（图表/头像） | `alt="月度营收柱状图"` 描述信息 |
| 纯装饰（背景纹理/分隔图标） | `alt=""`（空串，读屏跳过） |
| 可点图片链接 | `alt` 写目的地，不写「图片」 |
| 图标按钮里的图标 | 图标 `aria-hidden`，名给外层 `aria-label` |

## label 关联三法

| 方式 | 写法 | 适用 |
|------|------|------|
| 显式 htmlFor | `<label htmlFor="id">` + `<input id="id">` | 自研控件首选 |
| 包裹 | `<label>姓名<input/></label>` | label 与控件相邻 |
| aria-label | `<input aria-label="搜索">` | 无可见 label 时（如纯图标搜索框） |
| aria-labelledby | `aria-labelledby="titleId"` | 引用已有可见文本作名 |

antd `Form.Item label="姓名"` 自动生成 `htmlFor` 并关联子控件，**不要再手写 label**。

## live region 取值

| 取值 | 行为 | 用途 |
|------|------|------|
| `off` | 不播报 | 默认 |
| `polite` | 读完当前内容再播 | 列表刷新、轮询结果、表单提示 |
| `assertive` | 立即打断播报 | 错误、超时等紧急信息（等价 `role="alert"`） |
