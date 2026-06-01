# 留学工具箱 (Study Abroad Toolkit)

一站式留学生实用工具网站，面向中亚及一带一路国家留学生。

## 工具列表

- 🪙 汇率换算器 — 人民币 ↔ 坚戈/卢布/美元/欧元
- 📊 生活成本计算器 — 估算目标城市月花费
- 🕐 时区转换器 — 跨国时间对照 + 课程表规划
- 🎒 行李清单生成器 — 按目的地/季节自动生成清单

## 技术栈

- 前端：HTML + CSS + Vanilla JS（托管于 GitHub Pages）
- 后端：Python FastAPI（托管于 Vercel）
- 数据：exchangerate-api.com（汇率）

## 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 启动后端
cd backend
uvicorn main:app --reload --port 8000

# 前端直接用浏览器打开 frontend/index.html
```
