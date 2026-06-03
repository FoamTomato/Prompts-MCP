# Design Language · 详细参考

主入口：[`design-language.md`](design-language.md)。本文给一套完整设计语言范例（照此结构定自己项目的），外加字体配对清单与配色档案。

---

## A. 范例设计语言（结构照搬，色值按品牌替换）

下面是一套「干净白底 + 单一品牌强调色」设计语言的完整定义，演示七件套如何落地。

### 1. 文字灰阶（5 级，暖灰链）

| 级 | hex | 用途 |
|----|-----|------|
| L1 强 | `#1C1917` | 标题、关键数据、激活文字 |
| L2 主 | `#57534E` | 正文、描述 |
| L3 次 | `#78716C` | 预览文字、meta |
| L4 弱 | `#A8A29E` | 标签、副标题、占位、图标 |
| L5 禁用 | `#D6D3D1` | 禁用态、分隔线、箭头 |

### 2. 品牌强调色 scale（示例用紫，换品牌只改这一条）

```text
50 #F5F3FF · 100 #EDE9FE · 200 #DDD6FE · 300 #C4B5FD · 400 #A78BFA
500 #8B5CF6 · 600 #7C3AED · 700 #6D28D9 · 800 #5B21B6 · 900 #4C1D95
```

语义映射：`--accent:600` · `--accent-hover:700` · `--accent-active:800` · `--accent-subtle-bg:50` · `--accent-subtle-border:200`。
强调渐变：`linear-gradient(135deg, #7C3AED 0%, #A78BFA 100%)`（用于关键 CTA / 选中态）。

### 3. 背景与边框

页面 bg `#fff` · 内容区 bg `#f8f6f4` · 卡片 hover/标签 bg `#F5F5F4` · 顶栏 `#FAFAF9`。
主边框 `#E7E5E4`（分区、卡片、输入）· 浅边框 `#F5F5F4`（列表行分隔）。

### 4. 状态色（不复用品牌色）

成功 `#16A34A` · 警告 `#F59E0B`(琥珀) · 错误 `#DC2626` · 信息 `#3B82F6`。

### 5. 排版层级

字体族 `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, system-ui, sans-serif`。

| 元素 | size | weight | color |
|------|------|--------|-------|
| 页标题 | 18 | 600 | L1 |
| 区标题 | 16-22 | 600-700 | L1 |
| 卡片标题 | 14-17 | 600 | L1 |
| 正文 | 13-14 | 400-500 | L3 |
| 标签/meta | 11-12 | 500-600 | L4（uppercase, .04em） |

### 6. 组件五态

```css
/* 主按钮（深色，页面级主操作） */
.btn-primary { background:#1C1917; color:#fff; border-radius:8px; height:34px; font-weight:600; }
/* CTA（品牌渐变，生成/提交/升级类） */
.btn-cta { background:linear-gradient(135deg,#7C3AED,#A78BFA); color:#fff; }
.btn-cta:hover { box-shadow:0 4px 14px rgba(124,58,237,.32); }
/* 描边次按钮 */
.btn-outline { background:#fff; border:1px solid #7C3AED; color:#7C3AED; }
.btn-outline:hover { background:#F5F3FF; }
/* 幽灵 */
.btn-ghost { background:#fff; border:1px solid #E7E5E4; color:#78716C; }

/* 输入：聚焦上品牌色 + halo */
.input { border:1px solid #E7E5E4; border-radius:10px; background:#fff; }
.input:focus { border-color:#7C3AED; box-shadow:0 0 0 2px rgba(124,58,237,.08); }

/* 卡片：默认无阴影，hover 浮起 */
.card { background:#fff; border:1px solid #E7E5E4; border-radius:12px; transition:all .2s ease; }
.card:hover { border-color:#D6D3D1; box-shadow:0 4px 16px rgba(28,25,23,.06); transform:translateY(-2px); }
```

### 7. 动效曲线

| 名 | 值 | 用 |
|----|----|----|
| 标准 | `cubic-bezier(.4,0,.2,1)` | 布局/滑块过渡 |
| 弹性 | `cubic-bezier(.22,1,.36,1)` | 卡片入场、缩放 |

时长：hover .15s · 滑块 .25s · 卡片入场 .4-.5s · stagger .04-.08s/项。入场 `translateY(20px)→0` + fade。

### 8. 浮动 pill 指示器（tab/侧边菜单/切换的滑动高亮）

```css
.pill { position:absolute; z-index:0; border-radius:8px; opacity:0; pointer-events:none;
  transition: left .25s cubic-bezier(.4,0,.2,1), width .2s, opacity .15s ease; }
```
激活项背后滑入一块品牌 subtle-bg（或渐变）作为高亮，平滑跟随选中项移动。

---

## B. 字体配对清单（标题 / 正文 / 调性 / 用途）

| 标题 | 正文 | 调性 | 用途 |
|------|------|------|------|
| Inter | Inter | 干净中性 | SaaS 默认（单一可变字体） |
| Manrope | Inter | 高效现代 | 金融 / 后台 / 仪表盘 |
| Space Grotesk | Inter | 技术感 | AI / Web3 |
| Bricolage Grotesque | Inter | 个性专业 | 新锐创业风 |
| Playfair Display | Source Sans | 编辑戏剧 | 奢华 / 杂志 |
| Fraunces | Inter | 复古现代 | 编辑品牌 |
| Poppins | Inter | 友好几何 | 趣味 / 消费 |
| Atkinson Hyperlegible | Inter | 高易读 | 无障碍优先 |

规则：标题管个性、正文管易读；族 ≤2（硬上限 3）；优先可变字体靠字重造层级。

---

## C. 配色档案（按产品原型，全部 ≥WCAG AA）

| 原型 | bg / surface | text 主/次 | interactive(CTA) | 语义/强调 |
|------|--------------|-----------|------------------|-----------|
| SaaS / B2B 信任(浅) | `#FFFFFF` / `#F1F5F9` | `#0F172A` / `#475569` | `#2563EB`，链接 `#1D4ED8` | 成功 `#15803D`、错误 `#DC2626`、边框 `#E2E8F0` |
| 金融(Stripe 风) | `#F8FAFC` / `#EFF6FF` | navy `#0A2540` | `#635BFF` | 金 `#C7A84B`、成功 `#0D9488`、错误 `#B91C1C` |
| 医疗(沉静) | `#E8F5E9` / `#C8E6C9` | `#263238` / `#455A64` | teal `#26A69A`/`#0D9488` | 中 teal `#80CBC4`；暖色仅用于告警 |
| 奢侈电商 | ivory `#F4EADE` | onyx `#0A0A0A` | 酒红 `#6E1423`/`#800020` | 单一金属色 24k 金 `#C69B3C` |
| 创意 / AI(暗) | `#09090B` / `#18181B` | `#FAFAFA` / `#A1A1AA` | purple `#A855F7` | indigo `#6366F1`、边框 `#3F3F46` |
| 暖中性 SaaS | `#FAFAF8` / `#F5F0EB` | warm-black `#1C1917` | blue `#0369A1` | terracotta `#C2410C` |

任何新配色都按 [`../foundations/accessibility.md`](../foundations/accessibility.md) 的对比度底线复核。
