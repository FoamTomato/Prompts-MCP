---
name: spring-security-password-encoding
description: Spring Security 密码加密 — BCryptPasswordEncoder 自带盐的单向哈希存储与校验，禁明文/MD5/SHA。Use when 存用户密码 / 选密码编码器 / 校验登录密码时。
parent: ./index.md
paths:
- '*.java'
triggers:
  keywords:
  - 密码加密
  - 加盐哈希
  - BCryptPasswordEncoder
  - PasswordEncoder
  - matches 校验
effort: medium
context: inline
version: '1.0'
---
# Spring Security · 密码加密

> 本条只管「用户密码怎么存、怎么校验」。鉴权流程见 [`jwt-stateless.md`](./jwt-stateless.md)。

## 规则

| 维度 | 约定 |
|------|------|
| 算法 | `BCryptPasswordEncoder`：自适应、每次自带随机盐，**禁明文 / MD5 / SHA-256 等快速哈希** |
| 注册成 Bean | `@Bean PasswordEncoder` 暴露，业务统一注入，别 `new` 散落各处 |
| 存储 | 只存 `encode(raw)` 的哈希串；数据库**绝不存明文**，日志也不打印 |
| 校验 | 用 `matches(raw, encoded)`，**不要**自己 `encode` 后字符串比较（盐随机，每次结果不同） |
| 强度 | 默认 strength 10，可调高换更慢的哈希；多算法共存用 `DelegatingPasswordEncoder`（`{bcrypt}` 前缀） |

## 正例

```java
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder();   // 默认 strength 10，自带盐
}

@Service
@RequiredArgsConstructor
public class UserService {
    private final PasswordEncoder passwordEncoder;

    public void register(String username, String rawPassword) {
        // 存哈希，不存明文
        final String hash = passwordEncoder.encode(rawPassword);
        userMapper.insert(new UserDO(username, hash));
    }

    public boolean login(String rawPassword, String storedHash) {
        // 用 matches 校验，不自己 encode 后比较
        return passwordEncoder.matches(rawPassword, storedHash);
    }
}
```

## 反例

```java
// ❌ MD5 / 明文存储：MD5 无盐、可彩虹表反查，明文一旦库泄露全军覆没
String hash = DigestUtils.md5Hex(rawPassword);
userMapper.insert(new UserDO(username, hash));

// ❌ 校验时自己 encode 再比较：BCrypt 每次盐随机，两次结果必然不等，永远登录失败
boolean ok = passwordEncoder.encode(rawPassword).equals(storedHash);  // 永远 false
```

## 自检

- [ ] 用 `BCryptPasswordEncoder`，没用明文 / MD5 / SHA？
- [ ] `PasswordEncoder` 注册成 Bean 统一注入？
- [ ] 数据库与日志都不出现明文密码？
- [ ] 校验用 `matches(raw, encoded)`，没自己 `encode` 后字符串比较？

## 相关

- 父：[`./index.md`](./index.md)
- 兄弟：[`jwt-stateless.md`](./jwt-stateless.md)（校验通过后签发 token）
- 兄弟：[`filter-chain.md`](./filter-chain.md)（`PasswordEncoder` Bean 供 `AuthenticationManager` 使用）
