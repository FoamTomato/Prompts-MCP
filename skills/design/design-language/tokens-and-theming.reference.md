# Tokens & Theming · 详细参考

主入口：[`tokens-and-theming.md`](tokens-and-theming.md)。本文是完整变量表与互换格式。

## 1. 完整三层变量表

```css
:root {
  /* ---- L1 primitive：原始调色盘，不直接给组件用 ---- */
  --blue-600:#0052CC; --blue-700:#0747A6;
  --slate-50:#F8FAFC; --slate-100:#F1F5F9; --slate-500:#64748B; --slate-900:#0F172A;
  --green-600:#15803D; --amber-500:#D97706; --red-600:#DC2626;

  /* ---- L2 semantic：角色别名，组件消费这一层 ---- */
  --surface:           var(--slate-50);
  --surface-elevated:  #FFFFFF;
  --text-primary:      var(--slate-900);
  --text-secondary:    var(--slate-500);
  --interactive:       var(--blue-600);
  --interactive-hover: var(--blue-700);     /* 深 ~12% */
  --border:            var(--slate-100);
  --success: var(--green-600); --warning: var(--amber-500); --error: var(--red-600);
  /* on-X 内容色，保证文字达对比度 */
  --on-interactive:#FFFFFF; --on-surface: var(--slate-900);

  /* ---- 间距 / 圆角 / 字号（同样可分层） ---- */
  --space-1:8px; --space-2:16px; --space-3:24px; --space-4:32px; --space-6:48px;
  --radius-sm:8px; --radius-md:12px; --radius-lg:20px;
  --text-sm:14px; --text-base:16px; --text-lg:20px; --text-xl:25px;

  /* ---- L3 component：可选，组件局部别名 ---- */
  --button-bg:        var(--interactive);
  --button-bg-hover:  var(--interactive-hover);
  --button-fg:        var(--on-interactive);
  --card-bg:          var(--surface-elevated);
  --card-border:      var(--border);
}
```

## 2. 换肤覆盖层（只动 semantic）

```css
[data-theme="luxury"] {
  --interactive:#6E1423; --interactive-hover:#5A0F1D;
  --surface:#F4EADE; --text-primary:#0A0A0A;
}
[data-theme="dark"] {
  --surface:#18181B; --surface-elevated:#27272A;
  --text-primary:#FAFAFA; --text-secondary:#A1A1AA;
  --interactive:#A855F7; --interactive-hover:#9333EA; --border:#3F3F46;
  --on-surface:#FAFAFA;
}
```

## 3. Light / Dark 三种实现

```css
/* (a) 自动 */
@media (prefers-color-scheme: dark) {
  :root { --surface:#18181B; --text-primary:#FAFAFA; /* ... */ }
}
/* (b) 手动：JS 在 <html> 上切 data-theme，配 localStorage 持久化 */
/* (c) light-dark()：需根上声明 color-scheme */
:root { color-scheme: light dark; }
.panel { background: light-dark(#FFFFFF, #18181B); color: light-dark(#0F172A, #FAFAFA); }
```

生产组合：默认 `prefers-color-scheme` 自动，`[data-theme]` 覆盖用户手选。

## 4. W3C DTCG 互换格式

跨工具交换用 W3C Design Tokens 格式（`$value` 必填 + `$type`，别名用花括号引用），经 Style Dictionary 编译成各端变量：

```json
{
  "color": {
    "blue":        { "$type": "color", "$value": "#0052CC" },
    "interactive": { "$type": "color", "$value": "{color.blue}" }
  },
  "space": { "2": { "$type": "dimension", "$value": "16px" } }
}
```

`$type` 支持 color / dimension / fontFamily / fontWeight / duration / cubicBezier / number，及复合类型 shadow / border / typography / gradient。

## 5. 常见错误

- 组件里写裸 hex → 换肤改不动，到处漏改。
- semantic 跳过直接 primitive 给组件 → 失去换肤入口。
- 换肤时把整套 primitive 全复制改 → 应只覆盖 semantic 映射。
- 忘了 `on-` 内容色 → 深色模式文字对比度崩。
