---
name: commit-conventional
description: Conventional Commit — feat/fix/chore/docs/refactor/test/style + 中文描述。Use
  when 评审涉及 `conventional-commit` 的 PR。
parent: ./index.md
paths:
- .git/**
- '**'
triggers:
  keywords:
  - commit
  - conventional
  - 'feat:'
  - 'fix:'
  - 中文描述
effort: medium
context: inline
version: '1.0'
---
# Commit · Conventional Commit

## 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

## type 词表

| type | 用途 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat:增加用户登录接口` |
| `fix` | bug 修复 | `fix:解决冲突` |
| `refactor` | 重构（不改功能） | `refactor:拆分 outline_generator` |
| `chore` | 杂务（依赖 / 配置） | `chore:升级 antd 到 5.20` |
| `docs` | 文档 | `docs:更新 PRD home_page` |
| `style` | 代码风格（不改逻辑） | `style:格式化 import 顺序` |
| `test` | 测试 | `test:添加 useSSE 单测` |
| `perf` | 性能优化 | `perf:列表加 Redis 缓存` |
| `ci` | CI/CD | `ci:增加 prd-sync-check workflow` |

## 示例

```
abc1234 feat:增加用户登录接口
def5678 fix:解决冲突
9abcdef Merge branch 'feature' into main
2fbd438 feat:增加向量入库流程
fb908e5 feat: 列表搜索改为 LIKE + 向量混合检索
```

注意：若团队约定 `type:` 后**无空格**直接接中文 subject，**新提交保持一致**（与仓库历史对齐）。

## subject 写作

| 要 | 不要 |
|----|------|
| 动词开头："增加" / "修复" / "重构" | 名词开头 |
| 简洁明确 ≤ 50 字 | 长 + 含混 |
| 中文（团队约定用中文 subject，与历史对齐） | 英文 |
| 一句话能说清"做了什么" | 还要展开才知道 |

## scope（可选）

scope 是模块名。可用子模块编号或语义名（如 `feature-x` / `billing` / `auth`）：

```
feat(feature-x): 实现三级联动筛选
fix(billing): InvoiceCard 卡片悬停动画卡顿
refactor(editor): 拆分 AI 编辑双触发器
```

## body / footer（多行 commit）

```
feat:增加 SSE 流式大纲生成

- 实现 generate_outline_stream service
- 用 useSSE hook 接前端
- 配合 LLM provider 工厂支持主备降级

Closes #54
```

## 自检

- [ ] type 词表内？
- [ ] subject 动词开头？
- [ ] subject ≤ 50 字？
- [ ] 中文？
- [ ] 与仓库历史风格一致（type 后无空格）？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`claim-issue-in-message.md`](./claim-issue-in-message.md)

