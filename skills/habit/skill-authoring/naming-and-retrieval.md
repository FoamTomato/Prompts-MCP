---
name: skill-naming-and-retrieval
description: skill 文件/文件夹命名规范 + 检索友好规则 — 路径每段都是检索 keyword，命名直接决定召回。Use when 新建 skill / 改 skill 路径或文件夹 / 评审涉及目录结构的 PR / 索引召回不准时。
parent: ./index.md
paths:
  - "skills/**/*.md"
triggers:
  keywords:
    - 命名规范
    - naming convention
    - 文件夹命名
    - folder naming
    - 检索友好
    - retrieval-friendly
    - 路径关键词
    - path token
    - kebab-case
    - 目录结构
effort: low
version: "1.0"
---

# Skill 命名与检索规范

## 为什么命名 = 检索

索引器（`build-skill-index.sh`）把每条 skill 的**路径按 `/` 切段**，每一段都进 keyword 倒排表（再加 H1 标题切词）。`skill-pick` / `skill-match` 就靠这些 keyword 召回。

> 所以：**路径里每一段文件夹名、每个文件名，都是一个检索词。** 名字起得准 = 召回得准；名字含糊 / 缩写 / 黑话 = 那一段白白浪费、甚至召回错。

## 路径结构：`<域>/<子域>[/<模块>]/<叶>.md`

- **域**（第一段）= 索引的 `kind`，固定四个：`design-pattern` / `framework` / `habit` / `lang`（外加运行时生成的 `style`）。**不要新增顶级域**（`skill-pick.sh` 的 kind_filters 硬编码了它们）。
- **能拆出有意义的层就拆，不强求三段**：`framework/antd/form/form-item-name.md` 四段是好的——`antd`（库）、`form`（模块）都是有用的检索词。但**不要为凑层数硬塞**没意义的中间段。
- **每一段都必须是一个会被搜索的关键词**。判据：「用户描述这个场景时会不会说出这个词？」会 → 留；不会（策略黑话 / 泛化噪声）→ 改或删。

## 文件夹命名规则

- 用**检索友好的领域词**：`form` / `table` / `modal` / `async` / `typing` / `error-handling`。
- ❌ **禁单子文件夹**：一个文件夹只有 `index.md` + 1 个内容文件 = 这层没有分组价值，把内容文件提到上一层、删掉空壳。（例：`antd/mcp-first/antd-mcp-usage.md` → `antd/antd-mcp-usage.md`。）
- ❌ **禁策略黑话做文件夹名**：`mcp-first`、`boundary` 这种没人会搜的词，换成内容词或直接提层。
- **跨域同概念用同名**：异常处理统一叫 `error-handling`（不要 java 叫 `exception`、其它叫 `error-handling`），这样跨语言检索一致。
- **内容归位**：文件夹名要和内容真实匹配。`must-have-where`（UPDATE/DELETE 必带 WHERE）属 `dml/` 不属 `select/`——放错文件夹会漏检 + 污染该文件夹的检索语义。

## 文件（叶子）命名规则

- 全小写 **kebab-case**，`动词-名词` 或 `名词-名词`，自带语义：`no-select-star`、`form-item-name`、`side-effect-cleanup`。
- ❌ **不用 camelCase**（`no-business-in-useEffect` ❌ → `no-fetch-in-use-effect` ✅）——全库统一 kebab，破坏一致性会显得突兀（索引虽 tolower 容错，但文件名本身要规范）。
- ❌ **不重复父文件夹关键词**：`pr/` 下面别叫 `pr-create-and-close.md`（路径读成「pr pr-create」），直接 `create-and-close.md`——`pr` 这个词文件夹已经贡献了。
- ❌ **不加无检索价值的后缀**：`split-prd-method.md` 的 `-method` 是噪声 → `split-method.md`；`claim-issue-in-message.md` 在 `commit/` 下 `-in-message` 是废话 → `claim-issue.md`。
- ❌ **不用泛化词**：`usage-rule.md`（任何文件夹都能叫这名）→ 用具体内容词 `crud-contract.md`。
- `index.md` 是每层的入口/索引，**保留**这个固定名。
- `*.examples.md` / `*.reference.md` 是 progressive-disclosure 的外链层，与主文件同名前缀（见 [`progressive-disclosure.md`](./progressive-disclosure.md)）。

## frontmatter `name:` 跟随路径

- `name:` 用 `<子域>-<叶>` 或 `<域>-<子域>-<叶>` 形式，与路径语义一致、**全库唯一**。
- 改了文件/文件夹名 → **同步改 `name:`**（如 `java/exception/` → `java/error-handling/`，`name: lang-java-exception-index` → `lang-java-error-handling-index`）。

## 改名时的连带动作（缺一不可）

1. `git mv` 文件 / 文件夹
2. 改该文件 frontmatter `name:`
3. **全仓 grep 旧 token**，改掉所有反向引用：同目录 `index.md` 的 children/表/下钻链接、兄弟文件的 `相关` 链接、根 `index.md`。
4. 删空壳文件夹（含其 `index.md`）后，把父 `index.md` 里指向它的 `folder` 条目改成指向新位置的 `skill` 条目。
5. 改完**重跑 `build-skill-index.sh`**（检索 token 取自路径，不重建索引不生效）。
6. grep 确认旧 token 零残留 + 无新增悬空链接。

> ⚠️ grep 旧 token 时注意**子串误伤**：改 `prd-writer` 别碰 `prd-writer-lite`；改 antd 的 `boundary` 别碰 React 的 `error-boundary`。用足够精确的 pattern（带路径段 `antd/boundary` 而非裸 `boundary`）。

## 自检清单

- [ ] 路径每一段都是「用户会搜的词」，没有黑话 / 缩写 / 泛化噪声
- [ ] 没有单子文件夹（只有 index + 1 文件）
- [ ] 叶子是 kebab、不重复父文件夹词、无 `-method`/`-in-xxx` 等废后缀
- [ ] 跨域同概念同名（如 `error-handling`）
- [ ] 内容真实归属该文件夹（没放错域/模块）
- [ ] `name:` 与路径一致且全库唯一
- [ ] 改名后重跑了 build-skill-index 且旧 token 零残留

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`trigger-phrasing.md`](./trigger-phrasing.md)（keywords 怎么补，与路径段 keyword 互补）
- 兄弟：[`description-format.md`](./description-format.md)
