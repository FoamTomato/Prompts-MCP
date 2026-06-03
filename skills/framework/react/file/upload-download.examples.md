# React · 浏览器文件处理 — 完整示例

> 流水线编排风格：纯计算/转换下沉 util，hook/组件体只做顺序编排。

## 分片切块 util(纯函数)

```ts
// src/utils/chunk.ts
export interface FileChunk {
  index: number;
  blob: Blob;
}

// 把 File 按固定块大小切成有序块，纯计算无副作用
export function sliceFile(file: File, chunkSize = 5 * 1024 * 1024): FileChunk[] {
  const total = Math.ceil(file.size / chunkSize);
  // 用 Array.from 生成块索引，map 出 [start,end) 切片
  return Array.from({ length: total }, (_, index) => ({
    index,
    blob: file.slice(index * chunkSize, (index + 1) * chunkSize),
  }));
}
```

## 受限并发池 util(纯函数)

```ts
// src/utils/concurrentPool.ts
// 受限并发执行任务,避免一次性 Promise.all 打满连接;每完成一个回调进度
export async function runWithLimit<T>(
  tasks: Array<() => Promise<T>>,
  limit: number,
  onDone: () => void,
): Promise<T[]> {
  const results: T[] = new Array(tasks.length);
  let cursor = 0;

  // 单个 worker:循环领取下一个任务直到取完
  const worker = async (): Promise<void> => {
    while (cursor < tasks.length) {
      const current = cursor++;
      results[current] = await tasks[current]();
      onDone();
    }
  };

  // 启动 limit 个 worker 并行消费任务队列
  const workers = Array.from({ length: Math.min(limit, tasks.length) }, worker);
  await Promise.all(workers);
  return results;
}
```

## 分片上传 hook(编排 + 断点续传 + 进度)

```ts
// src/hooks/useChunkUpload.ts
import { useState, useCallback } from "react";
import { sliceFile } from "@/utils/chunk";
import { runWithLimit } from "@/utils/concurrentPool";
import { uploadApi } from "@/api/upload";

const CONCURRENCY = 3;

export function useChunkUpload() {
  const [progress, setProgress] = useState(0);

  const upload = useCallback(async (file: File, fileHash: string) => {
    // 切块:固定 5MB,得到有序分片
    const chunks = sliceFile(file);
    // 断点续传:先问后端已传哪些块索引
    const uploaded = await uploadApi.listUploaded(fileHash);
    // 过滤掉已传块,只保留待传块
    const pending = chunks.filter((chunk) => !uploaded.includes(chunk.index));
    // 进度基线:已传块计入初始进度
    const doneBase = chunks.length - pending.length;
    let done = doneBase;
    setProgress(Math.round((done / chunks.length) * 100));
    // 每块包装成一个上传任务(惰性,交给并发池调度)
    const tasks = pending.map((chunk) => () =>
      uploadApi.putChunk({ fileHash, index: chunk.index, blob: chunk.blob }),
    );
    // 受限并发上传,每完成一块累加进度
    await runWithLimit(tasks, CONCURRENCY, () => {
      done += 1;
      setProgress(Math.round((done / chunks.length) * 100));
    });
    // 全部块就位后通知后端合并
    await uploadApi.merge({ fileHash, total: chunks.length, filename: file.name });
  }, []);

  return { progress, upload };
}
```

## 图片预览 + revoke cleanup(防泄漏)

```tsx
// src/components/ImagePreview.tsx
import { useState, useEffect } from "react";
import { Image } from "antd";

export function ImagePreview({ file }: { file: File }) {
  const [url, setUrl] = useState("");

  useEffect(() => {
    // 为当前文件创建 ObjectURL(比 Base64 省内存)
    const objectUrl = URL.createObjectURL(file);
    setUrl(objectUrl);
    // cleanup:换图(file 变)或卸载时 revoke,释放底层文件引用防泄漏
    return () => URL.revokeObjectURL(objectUrl);
  }, [file]);

  return <Image src={url} alt="preview" width={160} />;
}
```

## 大文件流式下载(避免整块 Blob 驻留)

```ts
// src/utils/streamDownload.ts
// 流式拉取并写盘:边下边消费,不把整文件攒成一个 Blob,避免大文件 OOM
export async function streamDownload(url: string, filename: string): Promise<void> {
  // 发起请求,取可读流
  const response = await fetch(url);
  if (!response.body) throw new Error("响应无可读流");
  // 借助 File System Access API 拿到可写流(渐进式写盘)
  const handle = await (window as unknown as {
    showSaveFilePicker: (opts: { suggestedName: string }) => Promise<FileSystemFileHandle>;
  }).showSaveFilePicker({ suggestedName: filename });
  const writable = await handle.createWritable();
  // 把网络可读流直接 pipe 到磁盘可写流,内存只过当前 chunk
  await response.body.pipeTo(writable);
}
```
