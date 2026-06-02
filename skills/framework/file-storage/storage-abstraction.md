---
name: file-storage-storage-abstraction
description: 对象存储统一抽象 — 定义 StorageService 接口屏蔽 MinIO/OSS/S3 差异，业务只依赖接口，切厂商靠换实现+配置不改业务代码。Use when 接入对象存储 / 切换存储厂商 / 抽象上传下载接口时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 存储抽象
  - StorageService
  - MinIO
  - 阿里 OSS
  - S3 兼容
effort: medium
context: inline
version: '1.0'
---
# File Storage · 统一存储抽象

> 本条只管「怎么屏蔽厂商差异」。前端直传见 [`presigned-url.md`](./presigned-url.md)；大文件分片见 [`multipart-upload.md`](./multipart-upload.md)。

## 规则

| 项 | 约定 |
|----|------|
| 依赖方向 | 业务只 import 自定义 `StorageService` 接口，**禁止**直接 import `OSSClient` / `MinioClient` / `S3Client` |
| 入参出参 | 用领域对象（`StorageObject` / `InputStream` / `byte[]`），不暴露厂商 SDK 类型 |
| 多实现 | 每个厂商一个 `@Service` 实现，靠 `@ConditionalOnProperty(storage.type)` 选其一 |
| 选 S3 兼容 | MinIO / OSS / 七牛多支持 S3 协议 → 用 AWS S3 SDK 一套打通，少维护多份实现 |
| 异常 | 厂商异常在实现层捕获，统一转自定义 `StorageException`，业务不感知 SDK 异常 |

## 正例：接口 + 多实现按配置切换

```java
public interface StorageService {
    String upload(String bucket, String key, InputStream in, String contentType);
    InputStream download(String bucket, String key);
    void delete(String bucket, String key);
}

@Service
@ConditionalOnProperty(name = "storage.type", havingValue = "minio")
public class MinioStorageService implements StorageService {
    private final MinioClient client;

    @Override
    public String upload(String bucket, String key, InputStream in, String type) {
        // 步骤 1：调厂商 SDK
        try {
            client.putObject(PutObjectArgs.builder()
                    .bucket(bucket).object(key).stream(in, -1, 10485760)
                    .contentType(type).build());
            // 步骤 2：返回业务用的访问路径，不返回 SDK 对象
            return bucket + "/" + key;
        } catch (Exception e) {
            // 步骤 3：厂商异常统一转自定义异常
            throw new StorageException("上传失败: " + key, e);
        }
    }
    // download / delete 同样在本层封装 SDK
}
```

## 反例

```java
// ❌ 业务直接依赖 OSSClient：换厂商要全局改 import 和调用
@Service
public class OrderService {
    @Autowired OSSClient ossClient;          // 业务被 SDK 绑死
    void saveProof(byte[] img) {
        ossClient.putObject("proof", "x.png", new ByteArrayInputStream(img));
    }
}

// ❌ 接口出参漏厂商类型：上层被迫 import com.aliyun.oss.model.OSSObject
OSSObject download(String key);
```

## 自检

- [ ] 业务代码只依赖 `StorageService` 接口，不 import 任何厂商 SDK 类？
- [ ] 接口入参/出参全是领域类型或 JDK 类型，不漏 SDK 类型？
- [ ] 厂商切换靠换实现 + 改配置完成，业务零改动？
- [ ] 厂商异常在实现层转成了统一 `StorageException`？
- [ ] 评估过用 S3 兼容协议一套实现覆盖多厂商？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`presigned-url.md`](./presigned-url.md)（接口里加生成预签名 URL 的方法）
- 兄弟：[`multipart-upload.md`](./multipart-upload.md)（分片上传也走统一接口）
