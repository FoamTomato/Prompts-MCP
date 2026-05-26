---
name: error-code-prefix
description: 错误码前缀分配 — S/R/AC/B/V/I — 完整字典在 .ai/skills/core/error_code_dict.md。Use
  when 写 Python 后端代码 / 评审涉及 `prefix-allocation` 的 PR。
parent: ./index.md
paths:
- backend/**/*.py
- py/**/*.py
- frontend/src/**/*.ts
triggers:
  keywords:
  - 错误码
  - error code
  - ApiException
effort: medium
context: inline
version: '1.0'
---
# Error Code · 前缀分配

## 当前前缀

| 前缀 | 用途 | 范围 |
|------|------|------|
| **S** | anonymous_session 系列 | S101 ~ S199 |
| **R** | referral 系列（含 referral_config / referrals / referral_rewards） | R301 ~ R399 |
| **AC** | anti_crawler 风控系列 | AC401 ~ AC499 |
| **B** | 通用业务异常（NotFound / Forbidden / Conflict） | B400 ~ B499 |
| **V** | 校验失败（Validation） | V101 ~ V199 |
| **I** | 集成失败（外部 API / LLM / OSS / 存储） | I501 ~ I599 |

## 编号规则

```
<前缀><HTTP 状态码 第一位><两位流水>
```

例：
- `B402` → 业务 / 4xx / 流水 02 → "积分不足"
- `I503` → 集成 / 5xx / 流水 03 → "LLM 调用超时"
- `V101` → 校验 / 1（4xx 子段） / 流水 01 → "参数 title 必填"

## 使用

```python
# backend/services/credits.py
if not user.has_quota:
    raise ApiException(
        msg="积分不足",
        code=403,
        error_code="B402",
    )
```

## 完整字典

详见 `.ai/skills/core/error_code_dict.md`（**不迁移到新树**，保留为单一字典文件）。

新增错误码必须先在字典里登记，再投入使用。

## 新增前缀的规则

新业务领域加新前缀：

```
1. 检查 .ai/skills/core/error_code_dict.md 看是否已有可复用前缀
2. 否：在字典文件末尾加新前缀（按字母序）
3. 在 project-index/conventions.md 第 6 节追加
4. 通知团队
```

避免字母冲突。不用 `O / I / L`（与 0/1/L 易混）。

## 前端使用

```ts
// frontend/src/api/errors.ts
import { ApiError } from "@/types/error";

export const ERROR_MESSAGES: Record<string, string> = {
  B402: "积分不足，邀请好友可获赠积分",
  I503: "AI 服务繁忙，请稍后重试",
  S101: "会话已过期，请刷新页面",
  // ...
};

export function getErrorMessage(error: ApiError): string {
  if (error.error_code && ERROR_MESSAGES[error.error_code]) {
    return ERROR_MESSAGES[error.error_code];
  }
  return error.msg ?? "网络异常";
}
```

## 反例

```python
# ❌ 没 error_code
raise ApiException(msg="积分不足")

# ❌ 复用 HTTP code 做业务码（信息量低）
raise ApiException(msg="积分不足", code=403)

# ✅
raise ApiException(msg="积分不足", code=403, error_code="B402")
```

## 自检

- [ ] 新业务异常分配了 error_code？
- [ ] 前缀符合现有约定？
- [ ] 在 error_code_dict.md 登记？
- [ ] 前端 ERROR_MESSAGES 同步？

## 相关

- 父：[`./index.md`](./index.md)
- 配套：`.ai/skills/core/error_code_dict.md`（保留原位）· `project-index/conventions.md` 第 6 节 · [`../../lang/python/error-handling/api-exception.md`](../../lang/python/error-handling/api-exception.md)

