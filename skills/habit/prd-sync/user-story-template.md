---
name: prd-user-story
description: User Story 模板 — As a / I want / So that
parent: ./index.md
paths:
- project-index/modules/**
triggers:
  keywords:
  - User Story
  - as a
  - i want
  - 模板
effort: medium
context: inline
version: '1.0'
---
# PRD Sync · User Story 模板

## 标准格式

```
As a <角色>,
I want to <动作>,
So that <价值/目的>.

[Acceptance Criteria]
- AC1: <可验收条件>
- AC2: ...
```

## Quill 实例

```
Story H1：主页选择课本
  As a 教师
  I want to 在主页通过三级联动（学段 → 学科 → 年级）找到课本
  So that 我能快速定位本周的教学内容

  AC1: 三级联动各级有渐入动画
  AC2: 选完末级自动跳转到章节列表
  AC3: 历史选过的课本置顶
  AC4: 移动端可横向滑动 chip
```

```
Story H7：生成 CTA
  As a 教师
  I want to 看到一个明显的"生成课件"按钮
  So that 我不需要找按钮就能开始生成

  AC1: 按钮蓝紫渐变（品牌 CTA）
  AC2: 含 ✨ icon
  AC3: 选课本前禁用 + 文字"请先选择课本"
  AC4: 选完后启用 + hover 上浮
```

## 角色词表（Quill）

| 角色 | 场景 |
|------|------|
| 教师 | 主要用户，生成课件 / 试卷 |
| 学生 | 浏览公开课件（少数）/ 答题 |
| 教研组长 | 管理课件 + 模板 |
| 管理员 | 后台管理（admin_textbooks） |
| 匿名访客 | 未登录探索 |

## "I want to" 写作要求

- 动词开头："找到" / "下载" / "分享"
- 一句话 ≤ 25 字
- 描述**用户感知的动作**而非系统实现

```
❌ "I want to 调用 /api/textbooks/list 接口"
✅ "I want to 看到所有课本的列表"
```

## "So that" 是价值

不是技术实现，是**用户为什么要这个**。

```
❌ "So that 我能拿到 textbook 数组"
✅ "So that 我能选择本周需要的课本"
```

## AC 是验收标准

可观察、可测试。包括：

| 类型 | 例 |
|------|------|
| 视觉 | "按钮蓝紫渐变" |
| 交互 | "hover 时 transform translateY(-2px)" |
| 性能 | "首屏渲染 < 1s" |
| 数据 | "返回最多 100 条" |
| 边界 | "选 0 项时按钮禁用" |
| 错误 | "网络失败时显示重试按钮" |

## 拆解到子模块

每个 User Story 对应 1 个或多个子模块：

```
Story H1: 主页选择课本
  → 子模块：H5 TextbookCascader（三级联动）
  → 子模块：H8 useTextbookHistory（历史置顶）

Story H7: 生成 CTA
  → 子模块：H7 GenerateButton
```

详见 [`split-prd-method.md`](./split-prd-method.md)。

## 反例

```
❌ "I want a system that handles textbooks well"
  → 太抽象

❌ "用户 / 看课本 / 选课本"
  → 不是完整 story

✅ Story: 教师选课本（按 As a / I want to / So that 写完整）
```

## 自检

- [ ] As a / I want to / So that 三段齐？
- [ ] 角色明确？
- [ ] 动作是用户视角而非系统视角？
- [ ] So that 是价值不是实现？
- [ ] 有 AC（≥ 2 条）？
- [ ] 已映射到子模块？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`map-requirements-method.md`](./map-requirements-method.md) · [`split-prd-method.md`](./split-prd-method.md)

