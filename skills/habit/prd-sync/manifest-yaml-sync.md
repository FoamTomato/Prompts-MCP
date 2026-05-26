---
name: prd-manifest-sync
description: artifacts 增删 → 同步 manifest.yaml submodule.artifacts。Use when 改子模块 PRD
  / 评审涉及 `manifest-yaml-sync` 的 PR。
parent: ./index.md
paths:
- project-index/manifest.yaml
- project-index/modules/**
triggers:
  keywords:
  - manifest.yaml
  - artifacts
  - submodule
  - 增删
  - 同步
effort: medium
context: inline
version: '1.0'
---
# PRD Sync · manifest.yaml 同步

## 规则

当一个子模块的 artifacts 路径发生增删，**必须**同步 `project-index/manifest.yaml` 对应 submodule 的 `artifacts` 数组。

## manifest.yaml 结构

```yaml
home_page:
  submodules:
    H1:
      title: "HomePage（容器壳）"
      issue: 54
      prd_path: project-index/modules/home_page/H1-page-shell.md   # （文件夹格式才有）
      artifacts:
        - frontend/src/pages/HomePage.tsx
    H2:
      title: "ContentTypeSelector"
      issue: 55
      artifacts:
        - frontend/src/features/home/ContentTypeSelector.tsx
```

## 何时同步

| 触发 | 操作 |
|------|------|
| 新增组件文件 | artifacts 数组 push 一条 |
| 删除组件文件 | artifacts 数组移除 |
| 重命名（mv） | 删旧 + 加新 |
| 拆分多个文件 | 拆成多条 |
| 改文件路径 | 改对应条目 |

## 操作示例

实施 H1 时新增了 `useHomeInit.ts` hook：

```yaml
# 原
H1:
  artifacts:
    - frontend/src/pages/HomePage.tsx

# 改后
H1:
  artifacts:
    - frontend/src/pages/HomePage.tsx
    - frontend/src/hooks/useHomeInit.ts    # 新增
```

## 反例

```bash
# ❌ 加了新文件但 manifest 未更新
git add frontend/src/features/home/NewComponent.tsx
git commit -m "feat(H4):新增推荐卡"
# manifest.yaml 还说 H4 只有 RecommendedTextbooks.tsx，新的 NewComponent.tsx 不在清单
# → snapshot.json 无法识别 → 看板进度异常
```

## prd-manifest-consistency CI

未来 W5 实施 `prd-manifest-consistency.yml`：

- 扫所有 `modules/<X>/<SUB_ID>-*.md` 的 frontmatter.artifacts
- 与 manifest 的 `<X>.submodules.<SUB_ID>.artifacts` 互验
- 不一致 → CI fail

## 自检

- [ ] artifacts 增删时同步了 manifest？
- [ ] 重命名文件时改了 manifest 路径？
- [ ] 拆分文件时 manifest artifacts 数组扩了？
- [ ] manifest 改动与代码改动同 commit？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`update-on-code-change.md`](./update-on-code-change.md) · [`triplet-rule.md`](./triplet-rule.md)

