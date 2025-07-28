# Railway部署指南（推荐新手）

Railway是一个现代化的部署平台，支持Docker，非常适合快速部署。

## 优点
- 免费额度：每月500小时运行时间
- 自动SSL证书
- 简单的域名配置
- 支持Docker部署
- 自动从Git仓库部署

## 部署步骤

### 1. 准备工作
- 注册Railway账号：https://railway.app
- 将项目上传到GitHub（公开仓库）

### 2. 创建railway.json配置

在项目根目录创建`railway.json`：
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "restartPolicyType": "ON_FAILURE",
    "sleepApplication": false
  }
}
```

### 3. 修改Dockerfile（Railway优化版）

创建`Dockerfile.railway`：
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements_pytorch.txt ./requirements.txt

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码和模型
COPY app_pytorch.py ./app.py
COPY models/ ./models/

# 设置环境变量
ENV MODEL_PATH=/app/models/best.pt
ENV PORT=5000

# 暴露端口
EXPOSE $PORT

# 启动命令
CMD gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app
```

### 4. 在Railway中部署

1. 访问 https://railway.app 并登录
2. 点击 "New Project" → "Deploy from GitHub repo"
3. 选择您的项目仓库
4. Railway会自动检测Dockerfile并开始构建
5. 部署完成后，Railway会提供一个公网URL

### 5. 环境变量配置（如果需要）

在Railway项目设置中添加环境变量：
- `MODEL_PATH`: `/app/models/best.pt`
- `FLASK_ENV`: `production`

## 成本
- 免费额度：500小时/月（约20天24小时运行）
- 付费计划：$5/月起

## 注意事项
- 模型文件会增加Docker镜像大小，可能影响构建时间
- 免费额度有时间限制，适合测试和小规模使用 