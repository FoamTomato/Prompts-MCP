---
name: sql-alembic-migration-template
description: Alembic 迁移文件标准模板（含 upgrade/downgrade 对称）。Use when 写 Python 后端代码 / 评审涉及
  `alembic-migration-template` 的 PR。
parent: ./index.md
paths:
- py/migrations/**/*.py
- backend/alembic/versions/**/*.py
triggers:
  keywords:
  - Alembic
  - migration
  - upgrade
  - downgrade
  - 迁移文件
  - 移文件标
  - 文件标准
effort: medium
context: inline
version: '1.0'
---
# SQL · Alembic 迁移模板

## Quill 工具栈

Quill **不用 Alembic**，用 Tortoise ORM 的官方迁移工具 **Aerich**（兼容 Tortoise 语义）。本文件标题保留"alembic"是为了和 Python 生态约定俗成。

## 命名约定

```
py/migrations/models/
├── 0_init_textbooks.py
├── 1_init_themes.py
├── 2_init_outlines.py
├── 3_init_presentations_slides.py
├── 4_init_tasks.py
├── 5_init_assets.py
├── 6_init_llm_logs.py
├── 7_init_sessions.py
├── 8_init_papers.py
└── 9_init_referral.py
```

序号 + `init_<语义>.py` 或 `<seq>_alter_<table>_<field>.py`。

## 迁移文件骨架

```python
# py/migrations/models/9_init_referral.py
from tortoise import BaseDBAsyncClient

async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `referrals` (
            `id` CHAR(36) NOT NULL PRIMARY KEY,
            `inviter_session_id` CHAR(36) NOT NULL,
            `invitee_session_id` CHAR(36) NOT NULL UNIQUE,
            `invite_code` VARCHAR(16) NOT NULL,
            `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
            INDEX `idx_inviter` (`inviter_session_id`),
            INDEX `idx_code` (`invite_code`)
        ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

        ALTER TABLE `sessions`
            ADD COLUMN `invite_code` VARCHAR(16) NULL,
            ADD COLUMN `invited_by_code` VARCHAR(16) NULL,
            ADD COLUMN `bonus_credits` INT NOT NULL DEFAULT 0,
            ADD COLUMN `bonus_credits_lifetime` INT NOT NULL DEFAULT 0;
    """

async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `referrals`;
        ALTER TABLE `sessions`
            DROP COLUMN `invite_code`,
            DROP COLUMN `invited_by_code`,
            DROP COLUMN `bonus_credits`,
            DROP COLUMN `bonus_credits_lifetime`;
    """
```

## 规范

| 规则 | 说明 |
|------|------|
| upgrade / downgrade 对称 | 每条 upgrade 必有可回滚的 downgrade |
| 字段添加加 default | 避免 NOT NULL 加字段卡在已有数据 |
| 索引命名 `idx_<col>` | `uk_<col>` 唯一索引 |
| 字符集 utf8mb4 | 必须 |
| 主键 CHAR(36) UUID 或 BIGINT AUTO | Quill 业务表用 UUID |

## 操作命令

```bash
# 初始化
aerich init -t main.TORTOISE_ORM

# 生成迁移文件（基于 model 变化自动 diff）
aerich migrate --name "init_referral"

# 执行迁移
aerich upgrade

# 回滚一步
aerich downgrade -v 1
```

## 自检

- [ ] upgrade / downgrade 对称？
- [ ] 新增 NOT NULL 字段有 DEFAULT 或两步迁移（先 NULL 再回填再改 NOT NULL）？
- [ ] 索引命名规范 `idx_*` / `uk_*`？
- [ ] 大表 DDL 在低峰期跑（pt-online-schema-change 或维护窗口）？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：[`tortoise-model-template.md`](./tortoise-model-template.md) · [`../../../framework/tortoise/model-class-pattern.md`](../../../framework/tortoise/model-class-pattern.md)

