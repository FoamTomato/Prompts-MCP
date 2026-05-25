---
name: javascript-async-await-only
description: 禁 callback 风格 — 全 async/await
parent: ./index.md
paths:
  - "*.js"
  - "*.ts"
triggers:
  keywords: [async, await, callback]
effort: medium
context: inline
version: "1.0"
---

# JS · 全 async/await

## 规则

**禁 callback 风格**（除非第三方库强制）。全部走 Promise + async/await。

## 反例 → 正例

```js
// ❌ callback 风格
fs.readFile("data.json", (err, data) => {
  if (err) return console.error(err);
  parse(data, (err2, result) => { ... });
});

// ✅ async/await + util.promisify
import { readFile } from "node:fs/promises";
async function loadData() {
  const data = await readFile("data.json", "utf-8");
  return parse(data);
}
```

## 错误处理

```js
// ✅ try/catch
async function handler(req, res, next) {
  try {
    const data = await loadData(req.params.id);
    res.json(data);
  } catch (err) {
    next(err);   // Express 错误中间件接管
  }
}
```

## 并发

```js
// ❌ 串行
const a = await callA();
const b = await callB();

// ✅ Promise.all
const [a, b] = await Promise.all([callA(), callB()]);
```

## 自检

- [ ] 无嵌套 callback（pyramid of doom）？
- [ ] try/catch 完整覆盖 await？
- [ ] 并发请求用 Promise.all？

## 相关

- 父：[`./index.md`](./index.md)

