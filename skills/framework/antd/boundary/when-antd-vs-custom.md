---
name: antd-vs-custom-boundary
description: 决策：通用 primitive 一律 antd / 业务高度差异化的组件自研
parent: ./index.md
paths:
  - "frontend/src/**/*.tsx"
triggers:
  keywords: [antd, 自研, primitive]
effort: medium
context: inline
version: "1.0"
---

# antd · 与自研的边界

## 决策表

| 场景 | 用 antd | 自研 |
|------|--------|-----|
| 表单（Form / Input / Select / Checkbox / Radio / Switch / Slider / InputNumber） | ✅ | — |
| 表格 Table | ✅ | — |
| 弹窗 Modal / Drawer | ✅ | — |
| 选择器 DatePicker / TimePicker / Cascader | ✅ | — |
| 反馈 message / notification / Tooltip / Popover | ✅ | — |
| 数据展示 Tag / Badge / Avatar / Statistic | ✅ | — |
| 导航 Menu / Breadcrumb / Pagination / Steps | ✅ | — |
| 上传 Upload | ✅ | — |
| 课件卡 / 试卷卡 / 模板卡 | — | ✅（视觉差异化大） |
| 三级联动筛选（H5） | — | ✅（教学语义 + chip 步骤） |
| 编辑器画布（M6）+ 元素拖拽 | — | ✅（GSAP Draggable 性能） |
| 演示模式画笔 / 双屏 | — | ✅（全屏沉浸） |
| 课件 / 试卷 A4 实时预览 | — | ✅（教育特定布局） |
| 智能推荐卡（H4） | — | ✅（含徽章 + 学科色） |
| Hero 区 / 营销 CTA | — | ✅（蓝紫渐变 + 光晕） |

## 决策原则

```
是通用 primitive 且视觉差异不大？
  是 → antd
  否 → 自研

业务高度差异化（视觉 / 交互）？
  是 → 自研
  否 → antd

需要 GSAP 复杂动画？
  是 → 自研外壳 + GSAP，内部可嵌 antd primitive
  否 → antd
```

## 自研 + antd 混合的合法模式

```tsx
// 自研外壳 + antd 表单
function CustomPresentationCard({ data }: Props) {
  return (
    <div className="brand-card">
      <CoverImage src={data.cover} />
      <div className="meta">
        <h3>{data.title}</h3>
        <Tag color={data.subject_color}>{data.subject}</Tag>   {/* antd Tag */}
      </div>
      <ActionMenu />   {/* 内部用 antd Dropdown */}
    </div>
  );
}
```

外层视觉自研（card-shadow、Hover transform、独特圆角），内层用 antd 通用组件（Tag、Dropdown）。

## 反例

```tsx
// ❌ 把 antd Modal 改造成自研营销弹窗（CSS 大量覆盖）
<Modal
  className="hero-marketing-modal"
  styles={{ body: { background: "linear-gradient(...)" } }}
  closeIcon={<CustomCloseIcon />}
  ...
>
  <HeroContent />
</Modal>

// ✅ 干脆自研一个 <HeroMarketingModal>
```

```tsx
// ❌ 自研一个 Select 完整功能
function CustomSelect() {
  const [open, setOpen] = useState(false);
  // ... 重新发明键盘导航、a11y、虚拟滚动
}

// ✅ 用 antd Select + 主题定制
<Select options={options} className="brand-select" />
```

## 自检

- [ ] 通用 primitive 优先选 antd？
- [ ] 高度差异化视觉 / 教学语义独特 → 自研？
- [ ] 自研外壳内可以嵌 antd Tag / Dropdown 等小 primitive？
- [ ] 不要为了 1-2 处定制把 antd 改得面目全非（改写超过 50% 样式 → 干脆自研）？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`../../react/component/flat-ui-principles.md`](../../react/component/flat-ui-principles.md)

