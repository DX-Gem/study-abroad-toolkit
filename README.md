# 留学工具箱 (Study Abroad Toolkit)

一站式留学生实用工具 PWA App，面向中亚及一带一路国家留学生。

## 工具列表

- 🪙 汇率换算器 — 人民币 ↔ 坚戈/卢布/美元/欧元 实时换算
- 🆘 应急短语手册 — 俄语+哈语常用短句 · 翻译 · 离线朗读
- 💰 多币种记账本 — 坚戈/卢布/人民币 多币种记账 · 自动换算 · 预算预警
- 🕐 时区转换器 — 三时钟对照 + 课程表规划 + 12城市速查
- ✅ 出发倒计时 — 留学时间线待办 · 从准备到抵达全流程

## 特性

- 📱 PWA — 手机桌面图标 + 全屏运行 + 离线可用
- 🌐 俄语/哈语短语离线朗读（Web Speech API）
- 💱 实时汇率（exchangerate-api.com）
- 🔤 免费翻译（MyMemory API）
- 💾 记账/待办本地存储，断网不丢数据

## 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 启动后端
cd backend
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 前端直接用浏览器打开 frontend/index.html
```

## 技术栈

- 前端：HTML + CSS + Vanilla JS + PWA (Service Worker)
- 后端：Python FastAPI + httpx
- 数据：exchangerate-api.com（汇率）、MyMemory（翻译）
