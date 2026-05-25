---
name: pipeline-ppt-outline
description: PPT 大纲生成 pipeline — 章节 → 大纲 → 幻灯片
parent: ./index.md
paths:
  - "backend/services/outline_*.py"
  - "py/services/outline_*.py"
  - "backend/agents/**/*"
  - "py/agents/**/*"
triggers:
  keywords: [大纲, outline, PPT, pipeline]
effort: medium
context: inline
version: "1.0"
---

# Pipeline · PPT 大纲生成

## 流程

```
用户输入（章节 IDs）
        ↓
1. 加载章节内容
        ↓
2. 构造 prompt
        ↓
3. 调 LLM 流式生成
        ↓
4. 累积 chunks → 完整文本
        ↓
5. 用 with_structured_output 解析为 OutlineSection[]
        ↓
6. 持久化 outline 草稿
        ↓
返回 outline_id（前端 polling 或 SSE）
```

## Service 编排（流式版）

```python
# backend/services/outline_generator.py
async def generate_outline_stream(
    req: OutlineGenReq,
    user_id: int,
) -> AsyncGenerator[str, None]:
    """流式生成大纲 — 5 步"""

    # 1. 校验 + 配额
    OutlineValidator.validate_gen(req)
    await self._credits.assert_can_afford(user_id, cost=req.slide_count // 5)

    # 2. 加载章节
    chapters = await self._chapter_repo.find_by_ids(req.chapter_ids)
    OutlineValidator.assert_chapters_exist(chapters, req.chapter_ids)

    # 3. 构造 prompt
    prompt = build_outline_prompt(chapters, req.slide_count, req.style)

    # 4. 流式调用 LLM 并返回 chunk
    full_text = ""
    async for chunk in call_with_fallback(prompt):
        full_text += chunk
        payload = JsonData.stream_data(chunk.encode()).model_dump_json()
        yield f"data: {payload}\n\n"

    # 5. 解析 + 持久化
    try:
        parsed = OutlineParser.parse(full_text)   # → OutlineSection[]
        outline = await self._repo.save_draft(user_id, parsed)

        done = JsonData.stream_data(
            b"",
            msg="done",
            outline_id=str(outline.id),
            total_tokens=estimate_tokens(full_text),
        ).model_dump_json()
        yield f"data: {done}\n\n"

        # 6. 扣积分
        await self._credits.deduct(user_id, cost=req.slide_count // 5)

    except OutlineParseError as e:
        err = JsonData.stream_data(b"", msg="error", error=str(e)).model_dump_json()
        yield f"data: {err}\n\n"
```

## 与 Skills 协同

实现这条 pipeline 需要同时拉这些 skill：

| 维度 | skill |
|------|-------|
| lang | python/async/sse-streaming + python/error-handling/api-exception |
| framework | fastapi/router/sse-streaming + fastapi/llm/sse-protocol |
| design-pattern | pipeline/method-as-flow + factory/llm-provider-factory |

## 测试策略

```python
# 单元测试 — Validator / Parser 单独测
def test_outline_parser():
    text = "1. 引言\n  - 主题\n2. 主体\n..."
    sections = OutlineParser.parse(text)
    assert len(sections) == 2
    assert sections[0].title == "引言"

# 集成测试 — mock LLM 流
@pytest.fixture
def mock_llm(monkeypatch):
    async def fake_stream(prompt):
        yield "1. 引言\n"
        yield "  - 主题\n"
        yield "2. 主体\n"

    monkeypatch.setattr("services.llm_client.call_with_fallback", fake_stream)
```

## 自检

- [ ] 5-6 步骤清晰？
- [ ] 每步前有中文注释？
- [ ] 校验 / 解析独立类？
- [ ] LLM 调用走工厂 + 降级？
- [ ] SSE 用 done / error 帧通知？
- [ ] 失败不扣积分？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`method-as-flow.md`](./method-as-flow.md) · [`validator-converter-split.md`](./validator-converter-split.md)
- 配套：[`../../framework/fastapi/llm/sse-protocol.md`](../../framework/fastapi/llm/sse-protocol.md) · [`../factory/llm-provider-factory.md`](../factory/llm-provider-factory.md)

