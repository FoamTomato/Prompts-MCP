---
name: prd-update-on-code
description: CLAUDE.md Step 8 — 代码改 → 必更对应 <SUB_ID>-*.md Change Log
parent: ./index.md
paths:
- project-index/modules/**
- '**'
triggers:
  keywords:
  - PRD
  - Change Log
  - Step 8
  - 代码改
  - 必更对应
effort: medium
context: inline
version: '1.0'
---
# PRD Sync · 代码改 → 必更 PRD

## 规则（CLAUDE.md Step 8 硬性节点）

每次代码改动后**必须**同步更新对应 PRD 子模块的 `Change Log`。

## 操作步骤

```
1. 反查：改动文件 → mapping/module_path_map.md → 找到 module + SUB_ID
2. 编辑 modules/<module>/<SUB_ID>-*.md（文件夹格式）或 modules/<module>.md 对应小节
   - 刷 status（如 spec-ready → in-progress）
   - 勾产物清单（⬜ → ✅）
   - 加 Change Log 行
3. 如果 artifacts 路径有增删 → 同步 manifest.yaml submodule.artifacts
4. 如果新增/删除子模块 → 同步 <module>/README.md 子模块清单
5. PRD 改动 + 代码改动 → 同一个 commit
```

## Change Log 格式

每个子模块 .md 末尾固定段：

```markdown
## Change Log

| 日期 | 改动 | commit |
|------|------|--------|
| 2026-05-24 | 实现卡片组件初版 | abc1234 |
| 2026-05-25 | 加 hover 动画 | def5678 |
```

每次代码改动追加一行。`commit` 用 short hash。

## 三层保险（与 CLAUDE.md Step 8 配套）

| 层 | 实现 | 强度 |
|----|------|-----|
| 软 | CLAUDE.md Step 8 流程契约 | 靠遵守 |
| 中 | PostToolUse hook (`quill-post-tool.sh`) | stderr 告警 |
| 硬 | CI workflow (`prd-sync-check.yml`) | PR 时阻断 merge |

## PostToolUse hook 行为

```bash
# 检测：源码改了但 PRD 未改 → stderr 警告（不阻断）
$ vim backend/routers/textbooks.py
⚠️  Quill PRD-sync 提醒：
   你改了 backend/routers/textbooks.py （归属模块: textbook_data）
   但本会话未更新对应 PRD（project-index/modules/textbook_data/ 或 .md）
   CLAUDE.md Step 8 要求同步更新对应子模块 .md 的 Change Log
```

详见 `.claude/hooks/quill-post-tool.sh`。

## CI workflow 行为

```yaml
# .github/workflows/prd-sync-check.yml
# 改了 backend/ / frontend/ / py/ 但未改 project-index/modules/ → 阻断
```

PR 标签 `prd-sync-deferred` 可跳过（仅紧急 hotfix）。

## 反例

```bash
# ❌ 只 commit 代码不动 PRD
git add backend/routers/textbooks.py
git commit -m "feat(TD4):新增 textbooks 路由"
# CI 阻断：PRD 未同步

# ✅
git add backend/routers/textbooks.py
git add project-index/modules/textbook_data.md   # 更新 Change Log + 勾产物
git commit -m "feat(TD4):新增 textbooks 路由"
```

## 自检

- [ ] PRD Change Log 添加了一行？
- [ ] artifacts 清单状态更新（⬜ → ✅）？
- [ ] PRD 改动与代码改动同一 commit？
- [ ] CI prd-sync-check 通过？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`manifest-yaml-sync.md`](./manifest-yaml-sync.md) · [`triplet-rule.md`](./triplet-rule.md)
- 配套：CLAUDE.md Step 8 · `.claude/hooks/quill-post-tool.sh` · `.github/workflows/prd-sync-check.yml`

