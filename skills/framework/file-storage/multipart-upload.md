---
name: file-storage-multipart-upload
description: 对象存储大文件分片上传 — initiate/uploadPart/complete 三段式支持断点续传，附桶划分/路径分层/权限/CDN 加速规范。Use when 上传大文件 / 做断点续传 / 定桶与路径规范 / 配 CDN 时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 分片上传
  - 断点续传
  - multipart upload
  - 路径规范
  - CDN 加速
effort: high
context: inline
version: '1.0'
---
# File Storage · 大文件分片上传与桶/路径/CDN 规范

> 本条只管「大文件分片 + 桶路径权限 CDN 怎么定」。统一接口见 [`storage-abstraction.md`](./storage-abstraction.md)；前端直传见 [`presigned-url.md`](./presigned-url.md)。

## 规则

| 项 | 约定 |
|----|------|
| 何时分片 | 文件 > 100MB（或网络差）→ 分片上传，否则普通 putObject 即可 |
| 三段式 | `initiateMultipartUpload` → 并发 `uploadPart` → `completeMultipartUpload` 合并 |
| 分片大小 | 单片 5MB~100MB（S3 最小 5MB，最后一片可小于），片数 ≤ 10000 |
| 断点续传 | 持久化 uploadId + 已传 partNumber/ETag，重连只补缺片 |
| 中断清理 | 失败/超时调 `abortMultipartUpload` 释放碎片，否则计费且占空间 |
| 桶划分 | 按业务+环境分桶（`app-avatar-prod` / `app-doc-prod`），不要一个桶塞所有 |
| 路径分层 | `业务/日期/uuid.ext`，如 `avatar/2026/06/{uuid}.png`，禁原始文件名（重名/中文/注入） |
| 权限 | 桶默认私有，按需用预签名授权；公开资源单独放公共读桶 |
| CDN | 静态资源套 CDN 加速回源，配缓存策略 + 防盗链（Referer/签名 URL） |

## 正例：分片上传三段式（S3 SDK）

```java
public void uploadLargeFile(String key, List<ByteBuffer> parts) {
    // 步骤 1：发起分片上传，拿 uploadId（断点续传要持久化它）
    String uploadId = s3.createMultipartUpload(b -> b.bucket(bucket).key(key))
            .uploadId();
    List<CompletedPart> done = new ArrayList<>();
    try {
        // 步骤 2：逐片上传，partNumber 从 1 开始，记录每片 ETag
        for (int i = 0; i < parts.size(); i++) {
            int partNo = i + 1;
            String etag = s3.uploadPart(b -> b.bucket(bucket).key(key)
                    .uploadId(uploadId).partNumber(partNo),
                    RequestBody.fromByteBuffer(parts.get(i))).eTag();
            done.add(CompletedPart.builder().partNumber(partNo).eTag(etag).build());
        }
        // 步骤 3：合并所有分片
        s3.completeMultipartUpload(b -> b.bucket(bucket).key(key).uploadId(uploadId)
                .multipartUpload(m -> m.parts(done)));
    } catch (Exception e) {
        // 步骤 4：失败必须中止，释放已传碎片
        s3.abortMultipartUpload(b -> b.bucket(bucket).key(key).uploadId(uploadId));
        throw new StorageException("分片上传失败: " + key, e);
    }
}
```

## 反例

```java
// ❌ 大文件一次性读进内存再 putObject：2GB 文件直接 OOM
byte[] all = Files.readAllBytes(bigFile);
storageService.upload(bucket, key, new ByteArrayInputStream(all), type);

// ❌ 失败不 abort：残留分片长期计费 + 占空间
// ❌ 用原始文件名当 key：中文/重名/路径穿越，且无法分层管理
String key = file.getOriginalFilename();   // "我的 报告(1).pdf"
```

## 自检

- [ ] 大文件（>100MB）走分片，普通文件直接 putObject 不过度设计？
- [ ] 单片 ≥5MB、片数 ≤10000，记录 uploadId + 各片 ETag 支持续传？
- [ ] 失败/超时调用了 `abortMultipartUpload` 清理碎片？
- [ ] 桶按业务+环境划分，key 用 `业务/日期/uuid.ext` 不用原始文件名？
- [ ] 桶默认私有，静态公开资源套了 CDN + 防盗链？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`storage-abstraction.md`](./storage-abstraction.md)（分片上传也封进统一接口）
- 兄弟：[`presigned-url.md`](./presigned-url.md)（每个分片也可签发预签名 URL 由前端直传）
