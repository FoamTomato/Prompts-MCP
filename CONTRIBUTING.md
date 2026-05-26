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
- **description** must be **30–150 visible characters** and use the **two-sentence structure**:
  1. *First sentence* — what the skill is about, with concrete nouns (class/field/layer names). No generic copy like `组件命名规则`.
  2. *Second sentence* — must start with `Use when ` and list 2–4 concrete trigger situations separated by `/`. Example: `Use when 新建 Model 子类 / 改字段类型 / 评审 Migration 时。`
  See [`skills/habit/skill-authoring/description-format.md`](skills/habit/skill-authoring/description-format.md) for full guidance.
- **paths** are glob patterns. Used by `match_task_skills` to surface this skill when the caller is editing a matching file.
- **triggers.keywords** must contain **at least 3 entries** and include **at least one Chinese term and one English term**. Include common synonyms — this is the primary recall signal. Keywords are **noun phrases / class names / API names**, not sentences (sentences belong in the `Use when` half of `description`). See [`skills/habit/skill-authoring/trigger-phrasing.md`](skills/habit/skill-authoring/trigger-phrasing.md).
- **effort** ranks reading/applying cost; `low` skills get a small relevance boost on ties.
- **version** is a free-form string; bump it when behavior changes meaningfully.

### Body length

The skill body (everything after the closing `---` of frontmatter) must be:

- ≤ **100 lines** ideally — at this point the agent can absorb the whole thing in one read.
- ≤ **150 lines** as a hard cap — beyond this, the linter raises a **body-too-long** error. Split into:
  - `my-skill.md` — main entry, 30–100 lines of rules + self-check
  - `my-skill.reference.md` — detailed API tables, full field lists (no frontmatter)
  - `my-skill.examples.md` — full code examples (no frontmatter)
  - `scripts/` — optional companion scripts

Linter warns at 100 lines (`body-long`), errors at 150 (`body-too-long`). See [`skills/habit/skill-authoring/body-length-budget.md`](skills/habit/skill-authoring/body-length-budget.md) and [`progressive-disclosure.md`](skills/habit/skill-authoring/progressive-disclosure.md).

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
