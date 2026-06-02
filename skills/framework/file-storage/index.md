---
name: framework-file-storage-index
description: 对象存储（MinIO/阿里 OSS/AWS S3）Java 接入约定 — 统一抽象接口/预签名 URL 前端直传/分片上传大文件三个独立决策点。Use when 接入对象存储 / 切换存储厂商 / 做前端直传 / 上传大文件时。
parent: ../index.md
children:
  - { name: file-storage-storage-abstraction, path: storage-abstraction.md, tag: skill, note: 统一 StorageService 接口，切 MinIO/OSS/S3 不改业务 }
  - { name: file-storage-presigned-url, path: presigned-url.md, tag: skill, note: 预签名 URL 让前端直传，不经过应用服务器 }
  - { name: file-storage-multipart-upload, path: multipart-upload.md, tag: skill, note: 大文件分片上传 + 桶/路径/权限/CDN 规范 }
when_to_descend: 写 / 改 Java 里操作对象存储的代码：定义存储抽象、生成预签名 URL、做大文件分片上传或定桶/路径/权限规范。
---

# File Storage · 对象存储接入约定索引

三个**独立决策点**，按你正在做的事下钻：

| 你在做什么 | 进哪个 |
|-----------|-------|
| 定义统一存储接口、避免业务绑死某厂商 SDK | [storage-abstraction](storage-abstraction.md) |
| 让前端绕过应用服务器直传 / 直下对象存储 | [presigned-url](presigned-url.md) |
| 上传大文件分片 / 断点续传，定桶/路径/权限/CDN | [multipart-upload](multipart-upload.md) |

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../redis/index.md`](../redis/index.md) · [`../netty/index.md`](../netty/index.md)
