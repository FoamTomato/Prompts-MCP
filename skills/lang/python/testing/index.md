---
name: lang-python-testing-index
description: Python pytest 测试规范（结构 / fixture / 参数化 / mock / 异步与 HTTP / 覆盖率门禁）。Use when 写或评审 pytest 测试。
parent: ../index.md
children:
  - { name: py-test-pytest-structure, path: pytest-structure.md, tag: skill, note: "测试发现 / 目录布局 / assert 自省" }
  - { name: py-test-fixture-usage, path: fixture-usage.md, tag: skill, note: "fixture 作用域 / yield 清理 / conftest / autouse" }
  - { name: py-test-parametrize, path: parametrize.md, tag: skill, note: "parametrize / ids / 间接参数化" }
  - { name: py-test-mock-patch, path: mock-patch.md, tag: skill, note: "patch 打桩位置 / MagicMock / monkeypatch" }
  - { name: py-test-async-and-http-test, path: async-and-http-test.md, tag: skill, note: "pytest-asyncio / respx / freezegun" }
  - { name: py-test-coverage-gate, path: coverage-gate.md, tag: skill, note: "pytest-cov / 分支覆盖 / CI 门禁" }
when_to_descend: 写 test_*.py / conftest.py / 配置 pytest 或覆盖率门禁
---

# Python · 测试（pytest）· 子项索引

| 你在做什么 | 进哪个 |
|-----------|-------|
| 新建测试文件、不知道放哪 / 怎么命名 / 怎么被发现 | [`pytest-structure.md`](./pytest-structure.md) |
| 准备/清理测试数据、共享 client、conftest 共享夹具 | [`fixture-usage.md`](./fixture-usage.md) |
| 同一逻辑要跑多组输入、想要可读的用例名 | [`parametrize.md`](./parametrize.md) |
| 隔离外部依赖（DB/时间/环境变量/第三方对象） | [`mock-patch.md`](./mock-patch.md) |
| 测 async 函数、mock HTTP 出站请求、冻结时间 | [`async-and-http-test.md`](./async-and-http-test.md) |
| 量覆盖率、开分支覆盖、在 CI 卡阈值 | [`coverage-gate.md`](./coverage-gate.md) |
