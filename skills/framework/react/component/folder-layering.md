---
name: react-folder-layering
description: components/ features/<page>/ pages/ 三层目录约定。Use when 写 React 组件 / 改 .tsx
  文件 / 评审涉及 `folder-layering` 的 PR。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
triggers:
  keywords:
  - 目录
  - components
  - features
  - pages
effort: medium
context: inline
version: '1.0'
---
# React · 三层目录

## 规则

```
src/
├── components/      # 通用 UI（Button / Input / Modal / Toast / ...）
├── features/        # 业务组件（按页面分组）
│   ├── home/
│   ├── outline/
│   └── editor/
├── pages/           # 路由级组件（只做容器和编排）
└── hooks/           # 自定义 hooks
```

## 跨层 import 方向（单向）

| 谁可以 import 谁 | 谁不可以 |
|----------------|---------|
| `pages/` → `features/`、`components/`、`hooks/`、`stores/`、`api/` | — |
| `features/<page>/` → `components/`、`hooks/`、`stores/`、`api/` | 不要 import 其他 `features/<page>/`（横向耦合） |
| `components/` → `hooks/`、`utils/` | **禁止** import `features/`、`pages/`、`stores/`、`api/` |
| `hooks/` → `api/`、`stores/`、`utils/` | 不直接 import `features/` |

破坏方向 = 循环依赖风险 + 通用组件无法复用。

## 反例

```tsx
// ❌ components/ 引入了业务
// src/components/MyAvatar.tsx
import { useSessionStore } from "@/stores/session";

// ✅ 让调用方传 props
// src/components/Avatar.tsx
interface AvatarProps { src: string; name: string }
export function Avatar({ src, name }: AvatarProps) { ... }

// 业务方在 features/ 拼装
import { Avatar } from "@/components/Avatar";
function FeatureAvatar() {
  const user = useSessionStore(s => s.user);
  return <Avatar src={user.avatar} name={user.name} />;
}
```

```tsx
// ❌ features/home/ 直接 import features/editor/
import { EditorPanel } from "@/features/editor/EditorPanel";

// ✅ 共享下沉到 components/ 或新建 features/_shared/
```

## components/ 内禁止业务依赖

| 应当 ✅ | 不应当 ❌ |
|--------|---------|
| antd / react / @gsap | features / stores / api |
| 接受 props | useSessionStore |
| 受控组件 | 内部假设业务实体 |

## 自检

- [ ] 文件在 components / features / pages 哪个目录？是否符合分层语义？
- [ ] features 间无横向 import？
- [ ] components 无业务依赖？
- [ ] pages 不写业务逻辑，只做容器和编排？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`structure.md`](./structure.md)

