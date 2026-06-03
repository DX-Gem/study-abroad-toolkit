# 社交功能（朋友圈+好友）实现计划

> **Goal:** 基于 Firebase 为留学工具箱添加社交模块：邮箱注册登录、朋友圈动态、点赞评论、好友系统

**Architecture:** Firebase Auth 管理用户认证，Firestore 存储用户/动态/评论/点赞/好友关系。前端新增 community、friends、post 三个页面，社区 Tab 入口集成到所有页面

**Tech Stack:** Firebase JS SDK (CDN) + Firestore + Firebase Auth + Vanilla JS

---

## 文件结构

| 文件 | 职责 |
|------|------|
| `frontend/firebase-config.js` (新建) | Firebase 初始化 + Auth/Firestore 实例导出 |
| `frontend/community.html` (新建) | 朋友圈动态流 + 发布入口 |
| `frontend/friends.html` (新建) | 好友列表/搜索/请求管理/扫码 |
| `frontend/post.html` (新建) | 发动态页：文字+图片+话题标签 |
| `frontend/index.html` (修改) | Tab 栏加入社区 |
| `frontend/*.html` (修改12个) | 全部 Tab 栏加社区入口 |
| `frontend/sw.js` (修改) | 缓存新页面 |

## 数据模型 (Firestore)

```
users/{uid}
  - name, email, avatar, school, bio, createdAt

posts/{postId}
  - userId, userName, userAvatar, text, images[], topic, createdAt
  - likesCount, commentsCount

comments/{postId}/items/{commentId}
  - userId, userName, text, createdAt

likes/{postId}/items/{likeId}
  - userId, createdAt

friends/{userId}/items/{friendId}
  - friendId, friendName, friendAvatar, status(pending/accepted), createdAt
```

## 任务列表

### Task 1: Firebase 配置文件
**创建:** `frontend/firebase-config.js`
- Firebase 项目初始化配置
- Auth 和 Firestore 实例导出
- 用户状态监听

### Task 2: 登录注册页
**创建:** `frontend/login.html`
- 邮箱注册/登录切换
- Firebase Auth 集成
- 登录后跳转首页

### Task 3: 朋友圈动态广场
**创建:** `frontend/community.html`
- 动态列表流（文字+图片+作者信息）
- 点赞/评论按钮
- 发表新动态入口（跳转 post.html）
- 下拉刷新（可选）

### Task 4: 发动态页
**创建:** `frontend/post.html`
- 文字输入（最多500字）
- 图片上传（Firebase Storage，最多9张）
- 话题标签选择（#晒生活 #找室友 #二手 #求助 #美食 #旅行）
- 发布按钮

### Task 5: 好友系统
**创建:** `frontend/friends.html`
- 好友列表（已添加/待处理）
- 搜索用户（按邮箱/用户名）
- 发送好友请求
- 处理好友请求（接受/拒绝）

### Task 6: Tab 栏全局更新
**修改:** 所有工具页面
- 12个页面 Tab 栏新增 `👥 社区` 

### Task 7: SW 缓存 & APK 构建
- 更新 sw.js
- 构建 APK
- 推送到 Gitee
