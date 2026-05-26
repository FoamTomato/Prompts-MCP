---
name: prd-split-method
description: 拆 PRD 方法 — 子模块按字母前缀编号 + 三件套。Use when 改子模块 PRD / 评审涉及 `split-prd-method`
  的 PR。
parent: ./index.md
paths:
- project-index/modules/**
triggers:
  keywords:
  - 拆 PRD
  - split
  - 子模块
effort: medium
context: inline
version: '1.0'
---
# PRD Sync · 拆 PRD 方法

## 拆 PRD 触发

| 触发 | 行动 |
|------|------|
| 用户提出新需求 | 拆 PRD（新建模块） |
| 现有模块功能爆炸（子模块 > 13 或单文件 > 600 行） | 文件夹化重组（参考 W4 dashboard / ppt_generator） |
| 多个用户故事重叠 | 提取公共子模块（如 dashboard / scaffold） |

## 拆解步骤

```
1. 读用户需求文档 / 会议记录
2. 提炼 User Story（详见 user-story-template.md）
3. 按子模块拆解（每个子模块独立交付）
4. 给每个子模块分配字母前缀（见 conventions.md 第 1 节）
5. 起草 PRD 7 章节
6. 同步草图 + 拆解页（三件套）
7. 注册到 index.md / manifest.yaml / module_path_map.md
8. 刷新 prd-dashboard.html
```

## 子模块拆解原则

| 原则 | 说明 |
|------|------|
| **单一职责** | 一个子模块只解决一个用户感知问题 |
| **可独立交付** | 单 PR / 单 Issue 可完成 |
| **粒度** | 1-3 人天工作量 / 100-500 行代码 |
| **命名直白** | `D6 PresentationCard` 而非 `D6 Component-1` |
| **依赖明确** | 标明前置子模块（如 D6 依赖 D1 路由壳） |

## 字母前缀分配

详见 `project-index/conventions.md` 第 1 节。已有：

```
H = home_page (H1-H8)
O = outline_review (O1-O7)
M = ppt_generator (M1-M17)
W = task_waiting (W1-W6)
D = dashboard (D1-D22)
S = anonymous_session (S1-S6)
P = present_mode (P1-P10)
PE = paper_editor (PE1-PE11)
R = referral (R1-R8)
SC = scaffold (SC1-SC12)
DB = database_setup (DB1-DB13)
TD = textbook_data (TD1-TD9)
C = collab_dashboard (C1-C12)
AC = anti_crawler (AC1-AC10)
```

新模块**选未占用字母**（避免 I/O/L/R 与 1/0 易混的，R 已被 referral 占）。

## 反例

```markdown
# ❌ 子模块太粗
H1: 主页

# ✅ 子模块按可独立交付拆
H1: HomePage 路由壳（容器 + 路由）
H2: ContentTypeSelector（PPT / Word / 网页 选择器）
H3: GenerateOptionsBar（生成参数栏）
H4: RecommendedTextbooks（智能推荐 6 张卡）
H5: TextbookCascader（三级联动筛选）
...
```

## 自检

- [ ] User Story → 子模块映射清晰？
- [ ] 每个子模块单一职责？
- [ ] 字母前缀未被占用？
- [ ] 三件套同步创建？
- [ ] index / manifest / mapping 全部注册？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`triplet-rule.md`](./triplet-rule.md) · [`map-requirements-method.md`](./map-requirements-method.md) · [`user-story-template.md`](./user-story-template.md) · [`write-prd-7-sections.md`](./write-prd-7-sections.md)

