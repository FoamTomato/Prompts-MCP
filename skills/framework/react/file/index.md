---
name: framework-react-file-index
description: 浏览器侧文件处理约定 — 大文件分片上传、createObjectURL 必 revoke、Base64 vs ObjectURL 选型、流式下载。Use when 写文件上传 / 做图片预览 / 大文件下载 / 排查 ObjectURL 内存泄漏时。
parent: ../index.md
children:
  - { name: framework-react-file-upload-download, path: upload-download.md, tag: skill, note: 分片上传 + createObjectURL 必 revoke + 流式下载 }
when_to_descend: 写 / 改前端文件上传、图片预览、大文件下载相关代码时
---

# React · 浏览器文件处理约定索引

浏览器侧文件读写按场景下钻；后端存储与预签名见 `framework/file-storage`。

## 本层包含

| 名称 | 类型 | 一句话 |
|------|------|-------|
| upload-download | skill | 分片上传 + createObjectURL 必 revoke + 流式下载 |

## 何时下钻

- 上传大文件、要分片 / 断点续传 → [upload-download](upload-download.md)
- 选图 / 选文件后做本地预览（Base64 还是 ObjectURL） → [upload-download](upload-download.md)
- 下载大文件、想边下边写不占满内存（流式） → [upload-download](upload-download.md)
- 预览图反复创建却不释放、内存涨不下来 → [upload-download](upload-download.md) 的 revoke 规则

## 链接

- 上层：[`../index.md`](../index.md)
- 平行：[`../component/index.md`](../component/index.md) · [`../hook/index.md`](../hook/index.md)
- 跨引（后端）：对象存储、预签名直传、分片合并见 [`../../file-storage/index.md`](../../file-storage/index.md)
