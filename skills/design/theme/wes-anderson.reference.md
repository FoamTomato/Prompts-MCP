# Wes Anderson · 详细参考

主入口：[`wes-anderson.md`](wes-anderson.md)。本文是按需取用的完整调色板、排版、组件与配置。

## 1. 六套调色板（每套 5 色：背景 / 卡片 / 强调 / 标题 / 深色文字）

```text
布达佩斯大饭店（温暖粉红）
  #F1BB93 奶油杏(背景) · #E89B93 蜜桃粉(卡片) · #D96B7C 玫瑰红(强调) · #A13B5D 酒红(标题) · #5B2439 深莓红(深文字)
月升王国（自然绿）
  #E6DCA6 麦穗黄 · #BECBA4 苔藓绿 · #9FA8A3 雾灰绿 · #7D7C87 石板灰 · #5D4F63 暗紫灰
天才一族（暖棕）
  #CFBDA2 浅驼 · #C1A391 暖沙棕 · #B38C81 赤陶 · #A4736D 红木 · #905452 深砖红
了不起的狐狸爸爸（秋橘）
  #CEB780 蜜金 · #B89E66 琥珀黄 · #A4854D 焦糖 · #8E6D34 棕榈棕 · #7A551C 深栗
海海人生（冷蓝绿）
  #E5EDE9 薄荷白 · #CCD7D0 浅灰绿 · #9EB8B6 海雾绿 · #6A8E8F 深海绿 · #3D5C5D 墨绿
法兰西特派（淡紫）
  #F2E6F1 薰衣草白 · #E0D1DF 丁香灰 · #C2B4C2 藕荷紫 · #A496A6 灰紫 · #6B5A6E 深紫灰
```

中性文字 `#4A3F35`（暖深棕，替纯黑）· 次要 `#8C7E72` · 白 `#FDF8F0`（奶白，替纯白）。

### 配色层级映射

```text
背景 = 调色板[0] · 内容容器 = [1] · 分隔/标签 = [2] · 按钮/链接 = [3] · 标题/主文字 = [4]
```

### 情绪 → 调色板

温暖浪漫→布达佩斯 · 冒险好奇→月升王国 · 经典家族→天才一族 · 俏皮机敏→狐狸爸爸 · 沉静深邃→海海人生 · 优雅知性→法兰西特派。

### 配色禁止

- 不用纯黑 `#000`/纯白 `#fff`；不混两套调色板；强调色 <5%；不用高饱和霓虹；渐变仅同色系两色极微弱过渡。

## 2. 字体与排版层级

```css
--font-display: 'Futura PT', 'Josefin Sans', 'Century Gothic', system-ui;  /* 标题，免费替代 Josefin Sans */
--font-body:    'Playfair Display', 'Lora', Georgia, serif;                 /* 正文 */
--font-mono:    'Courier Prime', 'Courier New', monospace;                  /* 数据/标签 */
```

| 元素 | size | weight | letter-spacing | transform |
|------|------|--------|----------------|-----------|
| Hero 标题 | 56px | 700 | .12em | uppercase |
| 章节标题 | 32px | 600 | .08em | uppercase |
| 卡片标题 | 20px | 600 | .06em | uppercase |
| 正文 | 17px / 1.7 | 400 | .02em | none（衬线） |
| 标签小字 | 10-12px | 500-700 | .15-.2em | uppercase |

排版规则：标题全大写宽字距；正文衬线居中为主（长段落左对齐）；段距 2em、行高 1.7；弯引号 `""''`；em dash `—` 两侧半角空格；章节用 `CHAPTER I` / 罗马数字年份 `MMXXVI`。

## 3. 组件

```css
/* 按钮：近直角 + 复古 */
.wa-btn { font-family: var(--font-display); text-transform: uppercase; letter-spacing: .15em;
  padding: 14px 36px; border: 2px solid currentColor; border-radius: 2px; transition: all .3s ease; }
.wa-btn--primary { background: var(--accent); color: var(--light); }
.wa-btn--ghost   { background: transparent; color: var(--accent); }
.wa-btn:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,.15); }

/* 卡片：微圆角 + 顶部装饰线 */
.wa-card { background: var(--card-bg); border: 1.5px solid var(--border); border-radius: 4px;
  padding: 40px 32px; text-align: center; position: relative; }
.wa-card::before { content:''; position:absolute; top:0; left:20%; right:20%; height:3px; background: var(--accent); }

/* 装饰分隔线：✦ ─── TITLE ─── ✦ */
.wa-divider { display:flex; align-items:center; justify-content:center; gap:16px; margin:32px 0; }
.wa-divider::before, .wa-divider::after { content:''; width:60px; height:1px; background: var(--accent); }

/* 输入框：直角 + 居中 placeholder */
.wa-input { border:1.5px solid var(--border); border-radius:2px; text-align:center; padding:12px 20px; }
```

图标：线性 1.5px 圆角端点（Phosphor thin / Lucide），禁填充型/彩色/3D/emoji。
图片：`filter: saturate(.85) contrast(.95)`（胶片感），细边框，圆角 2px。

## 4. 纹理与阴影

- 背景叠极淡噪点（opacity .03-.08），别完全平滑。
- 阴影偏暖，用调色板深色 `color-mix` 而非纯黑：`0 4px 8px color-mix(in srgb, var(--text) 8%, transparent)`；默认无阴影 hover 才出。

## 5. 动效

```css
--ease-elegant: cubic-bezier(.25,.46,.45,.94);
@keyframes wa-rise   { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }   /* 元素升起 stagger .1s */
@keyframes wa-curtain{ from{clip-path:inset(0 50%)} to{clip-path:inset(0 0)} }                               /* 图片幕布展开 */
@media (prefers-reduced-motion: reduce){ * { animation:none !important; transition:none !important; } }
```

禁弹跳/果冻、3D 旋转、粒子光效；页面切换用淡入淡出（电影换幕）。

## 6. Tailwind 主题变量（切调色板只覆盖 5 个核心变量）

```css
:root {
  --wa-bg:#F1BB93; --wa-card-bg:#E89B93; --wa-accent:#D96B7C; --wa-accent-dark:#A13B5D; --wa-deep:#5B2439;
  --wa-text:#4A3F35; --wa-light:#FDF8F0;
  --wa-font-display:'Josefin Sans',system-ui; --wa-font-body:'Playfair Display',Georgia,serif;
  --wa-radius:2px; --wa-radius-sm:4px;
}
[data-theme="life-aquatic"] {   /* 换肤示例：海海人生 */
  --wa-bg:#E5EDE9; --wa-card-bg:#CCD7D0; --wa-accent:#6A8E8F; --wa-accent-dark:#3D5C5D; --wa-deep:#2A3E3F;
}
```

Google Fonts：`Josefin Sans`（标题，最接近 Futura 的免费替代）+ `Playfair Display`（正文）+ `Courier Prime`（等宽）。

## 7. 文案语气

CTA/标题带叙事感：`BEGIN YOUR STORY` 而非 `Sign Up`；空状态用温暖比喻 `THE COLLECTION IS EMPTY — awaiting its first artifact`；加载 `PREPARING YOUR DOSSIER...`。

## 8. 注意

- 本风格适合展示类页面，不推荐数据密集后台；宽字距 uppercase 只用于标题，正文切回衬线正常排版。
- 低饱和配色在深色模式需重新调色，不简单反转。
- `color-mix()` 需现代浏览器；噪点用内联 SVG data URI 不产生网络请求；装饰伪元素设 `pointer-events:none`。
