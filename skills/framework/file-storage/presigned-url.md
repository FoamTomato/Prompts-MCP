---
name: file-storage-presigned-url
description: 预签名 URL 前端直传 — 应用服务器只签发带过期的临时上传/下载 URL，文件流不经过应用，省带宽防内存溢出。Use when 做前端直传 / 临时授权下载 / 避免大文件过应用服务器时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 预签名 URL
  - 前端直传
  - presigned URL
  - 临时授权
  - generatePresignedUrl
effort: medium
context: inline
version: '1.0'
---
# File Storage · 预签名 URL 前端直传

> 本条只管「让前端绕过应用直传/直下」。统一接口见 [`storage-abstraction.md`](./storage-abstraction.md)；超大文件分片见 [`multipart-upload.md`](./multipart-upload.md)。

## 规则

| 项 | 约定 |
|----|------|
| 何时用 | 上传/下载文件 → **不让流经过应用服务器**，省应用带宽与内存 |
| 流程 | 前端先调应用拿预签名 URL → 前端用该 URL 直接 PUT 到 OSS → 回传 key 给应用 |
| 过期 | URL 必须设短过期（上传 5~15min），过期即失效，禁长期有效 |
| 上传约束 | 签发时限定 `Content-Type` / `Content-Length` 上限，防滥用上传超大或非法文件 |
| 私有桶 | 桶设私有，下载也用预签名 URL 临时授权，禁公开读 |
| 回调校验 | 前端回传 key 后，应用要 `statObject` 校验文件真实存在再落库 |

## 正例：签发上传 URL（S3 SDK）

```java
public String presignUpload(String key, String contentType) {
    // 步骤 1：构造仅限本 key + 本 Content-Type 的 PUT 请求
    PutObjectRequest req = PutObjectRequest.builder()
            .bucket(bucket).key(key).contentType(contentType).build();

    // 步骤 2：签发 10 分钟有效的预签名 URL
    PresignedPutObjectRequest pre = presigner.presignPutObject(b -> b
            .signatureDuration(Duration.ofMinutes(10))
            .putObjectRequest(req));

    // 步骤 3：只把 URL 给前端，密钥永不下发
    return pre.url().toString();
}
```

```javascript
// 前端：拿到 URL 后直接 PUT，文件流不经过你的应用
await fetch(presignedUrl, { method: 'PUT', body: file,
    headers: { 'Content-Type': file.type } });
```

## 反例

```java
// ❌ 文件流经应用中转：大文件撑爆应用内存/带宽，失去直传意义
@PostMapping("/upload")
public String upload(@RequestParam MultipartFile file) {
    storageService.upload(bucket, key, file.getInputStream(), file.getContentType());
    return key;   // 100MB 文件全进了应用堆
}

// ❌ 预签名 URL 不设过期 / 设几天：泄露即被人长期白嫖上传
presigner.presignPutObject(b -> b.signatureDuration(Duration.ofDays(7)));
```

## 自检

- [ ] 上传/下载走前端直传，文件流不经过应用服务器？
- [ ] 预签名 URL 设了短过期（分钟级），不是长期有效？
- [ ] 签发时限定了 Content-Type / 大小上限？
- [ ] 桶是私有的，下载也用预签名授权而非公开读？
- [ ] 前端回传 key 后应用校验了文件真实存在再落库？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`storage-abstraction.md`](./storage-abstraction.md)（把签发方法放进统一接口）
- 兄弟：[`multipart-upload.md`](./multipart-upload.md)（分片每片也可用预签名 URL）
