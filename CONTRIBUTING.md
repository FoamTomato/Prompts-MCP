# Contributing to Prompts-MCP

This repo is the source of truth for a markdown skill library that is exposed over MCP and a web viewer. Retrieval quality depends entirely on disciplined frontmatter — there is no vector index to paper over sloppy metadata.

## Frontmatter standard (required)

Every leaf `*.md` (i.e. an actual skill, not an `index.md`) must start with:

```yaml
---
name: <kebab-case-globally-unique>
description: <one sentence, 30–80 chars, concrete enough to be searchable>
parent: <relative path to the index.md one level up>
paths:
  - "frontend/src/**/*.tsx"
  - "frontend/src/**/*.ts"
triggers:
  keywords:
    - <Chinese term>
    - <English term>
    - <synonym>
effort: low | medium | high
version: 1.0
---
```

### Rules

- **name** is kebab-case, globally unique across the repo.
- **description** must be 30–80 visible characters. Bad: `组件命名规则` (too generic). Good: `React/antd 组件命名：Button vs CTA vs BrandButton 的三类区分与选用`.
- **paths** are glob patterns. Used by `match_task_skills` to surface this skill when the caller is editing a matching file.
- **triggers.keywords** must contain **at least 3 entries** and include **at least one Chinese term and one English term**. Include common synonyms — this is the primary recall signal for keyword search.
- **effort** ranks reading/applying cost; `low` skills get a small relevance boost on ties.
- **version** is a free-form string; bump it when behavior changes meaningfully.

### Index files

`index.md` at every directory level uses a different schema:

```yaml
---
name: <dir-kebab-name>
description: <what this folder groups>
parent: <relative path up>
children:
  - { name: foo, path: foo.md, tag: leaf, note: <one line> }
  - { name: bar, path: bar/index.md, tag: folder, note: <one line> }
when_to_descend: |
  Free-form prose describing when an agent should drill into this folder.
---
```

`children` must match the actual directory contents (the linter checks this).

## Linting

```bash
python scripts/lint_skills.py            # lint all skills under ./skills
python scripts/lint_skills.py --json     # machine-readable output
python scripts/lint_skills.py --fix-stubs  # (future) auto-add missing fields with placeholders
```

CI runs the linter on every PR. A green lint is a precondition for merge.

## File naming

- kebab-case, semantic: `button-naming.md`, not `naming.md` or `button_naming.md`.
- No file may share a name with a sibling directory.

## When in doubt

Open a draft PR and ask. Better to over-trigger the linter than to ship a skill that the recall layer can't find.
