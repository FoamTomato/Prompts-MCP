---
name: python-function-naming
description: Python 函数命名 — snake_case + 动词开头 + 语义化前缀
parent: ./index.md
paths:
  - "backend/**/*.py"
  - "py/**/*.py"
triggers:
  keywords: [def, 函数命名, 方法命名, snake_case]
effort: low
context: inline
version: "1.0"
---

# Python · 函数命名

## 规则

| 规则 | 示例 |
|------|------|
| snake_case | `create_user` / `get_brand_or_raise` |
| 动词开头 | `fetch_*` / `build_*` / `compute_*` / `validate_*` |
| Service 编排函数前缀 `service_` | `service_create_xxx`（区别于 Adapter / Repo） |
| 抛异常时带 `_or_raise` 后缀 | `get_brand_or_raise(brand_id)` |
| 异步函数同步命名 | `async def fetch_user(uid)`（不加 `async_` 前缀，调用方靠 `await` 区分） |
| 私有/内部函数加单下划线 | `_compute_internal(...)` |

## 动词词表（推荐）

| 用途 | 动词 | 示例 |
|------|------|------|
| 查询单条 | `get` / `find` / `fetch` | `get_user_by_id` |
| 查询列表 | `list` / `query` | `list_active_brands` |
| 创建 | `create` / `make` / `build` | `create_session` |
| 更新 | `update` / `patch` | `update_progress` |
| 删除 | `delete` / `remove` | `delete_asset` |
| 校验 | `validate` / `check` / `assert` | `validate_quota` |
| 转换 | `to` / `from` / `convert` | `to_response_model` |
| 持久化 | `save` / `persist` | `save_outline` |
| 计算 | `compute` / `calculate` | `compute_progress` |

## 反例

```python
# ❌ 名词开头（看着像变量）
def user_id(): ...

# ❌ 单字母 / 缩写
def proc(x): ...
def hdl_req(r): ...

# ❌ 中文 / 拼音
def 获取用户(): ...
def huoqu_user(): ...

# ❌ 驼峰
def getUserById(uid): ...

# ❌ 异常路径不显式
def get_brand(bid):
    b = Brand.filter(id=bid).first()
    if not b: raise ApiException(...)  # 名字未暗示会抛 → 改 get_brand_or_raise
```

## 自检

- [ ] 函数名是动词开头？
- [ ] 抛异常的函数有 `_or_raise` 后缀？
- [ ] 不是缩写 / 拼音 / 驼峰？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`variable-naming.md`](./variable-naming.md) · [`module-naming.md`](./module-naming.md)
- 配套：[`../../../habit/code-quality/naming-as-doc.md`](../../../habit/code-quality/naming-as-doc.md)
