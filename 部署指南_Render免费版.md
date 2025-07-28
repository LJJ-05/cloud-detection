# Render平台免费部署指南

## 🌟 Render优势
- **免费额度**：每月750小时（足够24/7运行）
- **无需信用卡**：真正的免费服务
- **支持Docker**：可以使用我们的配置
- **稳定性好**：比Railway更可靠

## 🚀 部署步骤

### 1. 注册Render账号
- 访问：https://render.com
- 点击 "Get Started for Free"
- 使用GitHub账号注册

### 2. 创建Web Service
1. 登录后点击 "New +"
2. 选择 "Web Service"
3. 连接GitHub仓库：`LJJ-05/cloud-detection`
4. 配置设置：
   - **Name**: `cloud-detection`
   - **Environment**: `Docker`
   - **Branch**: `main`
   - **Docker Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app`

### 3. 环境变量设置
添加环境变量：
- `MODEL_PATH`: `/app/models/best.pt`
- `PORT`: `10000` (Render默认端口)

### 4. 启动部署
- 点击 "Create Web Service"
- 等待构建完成（约10-15分钟）
- 获取您的应用URL

## 💰 免费限制
- **内存**: 512MB
- **CPU**: 共享
- **存储**: 足够使用
- **运行时间**: 750小时/月
- **休眠**: 15分钟无活动会休眠

## 🔗 成功后访问
- 您的应用URL：`https://cloud-detection.onrender.com`
- 网页界面和API都可以正常使用 