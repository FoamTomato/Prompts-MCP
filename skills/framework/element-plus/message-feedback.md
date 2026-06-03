---
name: element-plus-message-feedback
description: "Element Plus 消息反馈选型:瞬时提示 ElMessage / 带标题通知 ElNotification / 返 Promise 确认 ElMessageBox。Use when 操作成败反馈 / 需带标题通知 / 删除前确认拦截 / Message 与 Notification 选谁。"
parent: ./index.md
paths:
- frontend/src/**/*.vue
- frontend/src/**/*.ts
triggers:
  keywords:
  - ElMessage
  - ElNotification
  - ElMessageBox
  - 瞬时提示
  - 确认对话框
  - 消息分组 grouping
effort: low
context: inline
version: '1.0'
---

# Element Plus · 消息反馈组件选型

## 规则

决策点:**按"持久度 + 是否需用户操作"选组件**。

| 场景 | 组件 | 形态 | 返回值 |
|------|------|------|--------|
| 操作结果瞬时反馈(成功/失败) | `ElMessage` | 顶部居中,自动消失 | 无 |
| 需标题+正文的通知(后台任务完成) | `ElNotification` | 右上角,可手动关 | 无 |
| 危险操作前确认拦截(删除) | `ElMessageBox.confirm` | 居中模态 | `Promise` |
| 阻断式提示(必须知晓) | `ElMessageBox.alert` | 居中模态 | `Promise` |
| 收集单个输入 | `ElMessageBox.prompt` | 居中模态带输入框 | `Promise<{value}>` |

坑:
- `ElMessageBox.*` 点取消/关闭会 **reject**(reason `'cancel'`/`'close'`),不 `catch` 会抛 unhandled rejection。
- `ElMessage` 默认相同内容会叠多条,高频提示用 `grouping: true` 合并计数。

### 反例:自己手写确认弹窗

```vue
<!-- 多写一个 dialog + 两个 ref + 两个回调,逻辑散落 -->
<el-dialog v-model="confirmVisible" title="提示">确定删除?
  <el-button @click="confirmVisible = false">取消</el-button>
  <el-button type="primary" @click="doDelete">确定</el-button>
</el-dialog>
```

### 正例:ElMessageBox.confirm 早返回 + Message 反馈

```ts
import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'

async function handleDelete(id: number): Promise<void> {
  // 1. 确认拦截:用户取消则 reject,catch 后早返回
  const confirmed = await ElMessageBox.confirm('删除后不可恢复,确定?', '警告', {
    type: 'warning',
    confirmButtonText: '删除',
    cancelButtonText: '取消',
  }).catch(() => false)
  if (!confirmed) return

  // 2. 执行删除(失败由调用方 try/catch,此处只示意流程)
  await deleteApi(id)

  // 3. 瞬时反馈成功,grouping 合并批量删除的重复提示
  ElMessage({ message: '删除成功', type: 'success', grouping: true })
}

function notifyTaskDone(name: string): void {
  // 后台任务完成:带标题的右上角通知,需用户主动感知
  ElNotification({ title: '导出完成', message: `${name} 已生成`, type: 'success' })
}
```

## 自检

- [ ] 瞬时结果用 `ElMessage`,带标题通知用 `ElNotification`,二选一不混用
- [ ] 确认/拦截统一走 `ElMessageBox.confirm`,没有手写 `el-dialog` 充当确认框
- [ ] 所有 `ElMessageBox.*` 调用都接了 `.catch`(或 `try/catch`)处理 reject
- [ ] 确认结果用早返回 `if (!confirmed) return`,后续逻辑平坦不嵌套
- [ ] 高频/批量同文案的 `ElMessage` 设了 `grouping: true`

## 相关

- [../antd/selection/feedback-selection.md](../antd/selection/feedback-selection.md) —— antd 同维度反馈选型对照
- [./index.md](./index.md) —— Element Plus 维度路由
