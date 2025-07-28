# Railway免费版部署指南

## 🚀 快速部署步骤

### 1. 准备GitHub仓库

#### 上传项目到GitHub：
```bash
# 初始化git仓库（如果还没有）
git init

# 添加文件
git add .
git commit -m "Initial commit for Railway deployment"

# 连接到GitHub仓库
git remote add origin https://github.com/your_username/cloud-detection.git
git branch -M main
git push -u origin main
```

#### 确保这些文件在仓库中：
- ✅ `app_pytorch.py`
- ✅ `models/best.pt`
- ✅ `requirements_optimized.txt`
- ✅ `Dockerfile.railway`
- ✅ `railway.json`
- ✅ `.railwayignore`

### 2. 在Railway平台部署

#### 步骤1：注册并登录
1. 访问 https://railway.app
2. 使用GitHub账号登录
3. 授权Railway访问您的仓库

#### 步骤2：创建新项目
1. 点击 "New Project"
2. 选择 "Deploy from GitHub repo"
3. 选择您的 `cloud-detection` 仓库
4. Railway会自动检测到 `railway.json` 配置

#### 步骤3：等待部署
- Railway会自动使用 `Dockerfile.railway` 构建
- 构建时间约5-10分钟
- 可以在 "Deployments" 页面查看进度

#### 步骤4：获取URL
- 部署成功后，在 "Settings" → "Domains" 中
- 会显示类似：`https://your-app-name.railway.app`

### 3. 测试部署

#### 健康检查：
```bash
curl https://your-app-name.railway.app/health
```

#### 测试检测接口：
```python
import requests

url = "https://your-app-name.railway.app/detect"
files = {'image': open('test_image.jpg', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

## ⚠️ 重要提醒

### 免费版限制：
- **运行时间**: 500小时/月（约20天）
- **内存**: 512MB
- **存储**: 1GB
- **带宽**: 100GB/月

### 监控使用情况：
1. 在Railway控制台查看 "Usage" 页面
2. 关注内存和运行时间使用情况
3. 接近限制时服务会暂停

### 优化建议：
- 如果内存不足，可以减少 `--workers` 参数
- 定期检查服务状态
- 考虑在低峰期暂停服务节省时间

## 🔧 故障排除

### 常见问题：

#### 1. 构建失败
- 检查 `requirements_optimized.txt` 格式
- 确保模型文件 `models/best.pt` 存在

#### 2. 内存不足
- 修改 `Dockerfile.railway` 中的 workers 数量：
```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", ...]
```

#### 3. 服务超时
- 增加 timeout 设置：
```dockerfile
CMD ["gunicorn", ..., "--timeout", "180", ...]
```

## 📊 预期效果

成功部署后，您将获得：
- 🌐 公网可访问的API地址
- 🔒 自动SSL证书（HTTPS）
- 📱 支持移动端和网页调用
- 🔄 自动重启和健康检查

部署成功后，任何人都可以通过您的Railway URL调用您的云检测API！ 