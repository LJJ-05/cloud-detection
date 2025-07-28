# Fly.io部署指南 - 云检测项目专用

## 🌟 为什么选择Fly.io？

### 针对您的云检测项目优势：
- 🧠 **1GB内存**：足够运行PyTorch YOLO模型
- 🐳 **Docker原生**：直接使用您的Dockerfile.minimal
- 💰 **真正免费**：个人项目完全免费
- ⚡ **全球CDN**：东京节点，国内访问快
- 🔄 **自动休眠**：不用时自动关闭，节省资源

## 🚀 快速部署步骤

### 第1步：安装Fly CLI工具

#### Windows用户：
```powershell
# 使用PowerShell安装
irm https://fly.io/install.ps1 | iex
```

#### 或下载安装包：
- 访问：https://fly.io/docs/hands-on/install-flyctl/
- 下载Windows安装包

### 第2步：注册并登录

```bash
# 注册Fly.io账号（需要信用卡验证，但不扣费）
fly auth signup

# 或如果已有账号
fly auth login
```

### 第3步：初始化项目

在您的项目目录运行：
```bash
cd /d/pycharmproject/Cloud_detection

# 初始化Fly应用
fly launch --no-deploy

# 选择配置：
# - App name: cloud-detection-你的用户名
# - Region: nrt (Tokyo) 或 hkg (Hong Kong)
# - 不要立即部署：选择 No
```

### 第4步：配置fly.toml

系统会生成`fly.toml`文件，替换为以下内容：

```toml
app = "cloud-detection-你的用户名"
primary_region = "nrt"

[build]
  dockerfile = "Dockerfile.minimal"

[env]
  MODEL_PATH = "/app/models/best.pt"
  PYTHONUNBUFFERED = "1"

[http_service]
  internal_port = 5000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

  [[http_service.checks]]
    grace_period = "90s"
    interval = "30s"
    method = "GET"
    path = "/health"
    timeout = "15s"

[[vm]]
  memory = "1gb"
  cpu_kind = "shared"
  cpus = 1
```

### 第5步：部署应用

```bash
# 部署到Fly.io
fly deploy

# 查看状态
fly status

# 查看日志
fly logs
```

### 第6步：获取访问URL

```bash
# 查看应用信息
fly info

# 您的应用URL会是：
# https://cloud-detection-你的用户名.fly.dev
```

## 🔧 部署后测试

### 测试接口：
```bash
# 健康检查
curl https://your-app.fly.dev/health

# 调试信息
curl https://your-app.fly.dev/debug

# 网页界面
访问: https://your-app.fly.dev
```

## 💰 成本分析

### 免费额度（对您项目足够）：
- ✅ **1GB内存** - 您的模型约需600-800MB
- ✅ **1个CPU核心** - 检测任务足够
- ✅ **3GB存储** - 您的项目只有18MB
- ✅ **160GB带宽/月** - 个人使用绰绰有余

### 如果超出免费额度：
- 💰 **内存**: $0.0000022/MB/秒 (约$5/月/GB)
- 💰 **CPU**: $0.000022/CPU/秒 (约$56/月/CPU)
- 💰 **实际成本**: 个人项目通常每月$0-3

## 🛠️ 常见问题

### Q: 为什么需要信用卡？
A: 防滥用，但个人项目在免费额度内不会扣费

### Q: 如果模型还是加载失败？
A: 1GB内存应该够用，如果还失败可以：
```bash
# 升级到2GB内存
fly scale memory 2048
```

### Q: 如何更新代码？
A: 推送到GitHub后运行：
```bash
fly deploy
```

### Q: 如何查看详细日志？
A: 
```bash
fly logs --follow
```

## 🎯 预期结果

部署成功后：
- 🌐 **公网URL**: `https://your-app.fly.dev`
- 📱 **网页界面**: 可拖拽上传图片
- 🔗 **API服务**: 支持编程调用
- 💰 **完全免费**: 个人使用无需付费

---

**Fly.io的1GB内存应该能完美运行您的云检测模型！** 🚀 