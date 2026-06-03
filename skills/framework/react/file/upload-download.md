---
name: react-file-upload-download
description: 浏览器侧文件处理 — 大文件 File.slice 分片上传 / 图片预览用 createObjectURL 必 revoke / 大文件流式下载防爆内存。Use when 写大文件上传或断点续传 / 做图片本地预览 / 排查 ObjectURL 内存泄漏 / 下载大文件占满内存时。
parent: ./index.md
paths:
- frontend/src/**/*.tsx
- frontend/src/**/*.ts
triggers:
  keywords:
  - File.slice
  - 分片上传
  - 断点续传
  - createObjectURL
  - revokeObjectURL
  - 图片预览
  - readAsDataURL
  - 流式下载
  - 内存泄漏
effort: high
context: inline
version: '1.0'
---
# React · 浏览器文件处理

## 规则

决策点：**按文件大小 / 用途选处理方式，预览类资源必须显式释放**。三条主线：

| 场景 | 做法 | 为什么 |
|------|------|--------|
| 大文件上传 | `File.slice(start, end)` 切块，顺序/并发传，逐块更新进度 | 单请求传整文件易超时/无进度；分片可并发可断点续传 |
| 图片本地预览 | `URL.createObjectURL(file)` | 比 `readAsDataURL` 出的 Base64 省内存（不把整文件编码进字符串） |
| 大文件下载 | `fetch` + `response.body` 流式写盘 | 整块塞 `Blob` 会把整文件驻留内存，大文件直接 OOM |

要点：
- **分片**：`chunkSize` 固定（如 5MB），`Math.ceil(file.size / chunkSize)` 算块数；并发用受限并发池（非全量 `Promise.all`），每块带 `index/hash` 供后端合并与续传跳过已传块。
- **createObjectURL 必配 revokeObjectURL**：URL 持有底层文件直到显式释放或页面卸载。释放时机 = 图片 `onLoad` 之后 **或** 组件卸载/换图时的 `useEffect` cleanup（见[相关](#相关) effect-cleanup-leak）。不 revoke = 内存随每次换图持续上涨。
- **Base64 受字符串长度上限限制**且体积膨胀约 33%，仅适合小图标/内联;预览大图一律 ObjectURL。
- 断点续传:上传前先问后端"已传哪些块",`filter` 掉已传块再传。

## 反例 → 正例

```tsx
// ❌ createObjectURL 不 revoke：每次换图都泄漏一个 URL，内存涨不下来
function Preview({ file }: { file: File }) {
  const url = URL.createObjectURL(file); // 渲染即创建，永不释放
  return <img src={url} />;
}

// ❌ 大文件整块读进 Base64：整文件编码驻留内存 + 超字符串上限
function readBig(file: File) {
  const reader = new FileReader();
  reader.readAsDataURL(file); // 大文件 → 内存爆 / 字符串溢出
}
```

```tsx
// ✅ ObjectURL 在 useEffect cleanup 中 revoke，换图/卸载即释放
function Preview({ file }: { file: File }) {
  const [url, setUrl] = useState("");

  useEffect(() => {
    // 为当前文件创建预览 URL
    const objectUrl = URL.createObjectURL(file);
    setUrl(objectUrl);
    // cleanup：file 变化或组件卸载时释放，防泄漏
    return () => URL.revokeObjectURL(objectUrl);
  }, [file]);

  return <img src={url} alt="preview" />;
}
```

分片上传 hook、并发池、流式下载完整编排见 [`upload-download.examples.md`](./upload-download.examples.md)。

## 自检

- [ ] 大文件上传用 `File.slice` 分片，块大小固定、带 `index`/`hash` 给后端合并？
- [ ] 并发上传用受限并发池而非全量 `Promise.all`，并逐块累加进度？
- [ ] 断点续传上传前先查已传块，`filter` 跳过？
- [ ] 图片预览用 `createObjectURL`，且 `onLoad` 后或 `useEffect` cleanup 里 `revokeObjectURL`？
- [ ] 大文件下载走 `response.body` 流式，没有把整文件塞进单个 `Blob`？
- [ ] 没有对大文件用 `readAsDataURL` 读成 Base64？

## 相关

- 父：[`./index.md`](./index.md)
- 跨引（释放时机）：[`../reliability/effect-cleanup-leak.md`](../reliability/effect-cleanup-leak.md)（cleanup 对称释放副作用）· [`../reliability/prevent-double-submit.md`](../reliability/prevent-double-submit.md)（上传/提交按钮防连点重复）
- 跨引（后端）：[`../../file-storage/multipart-upload.md`](../../file-storage/multipart-upload.md)（分片合并 / 预签名直传 / 秒传校验）
