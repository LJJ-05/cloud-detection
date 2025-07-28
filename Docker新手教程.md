# 🐳 Docker新手完全教程

## 什么是Docker？

想象一下，Docker就像是一个"标准化的集装箱"：

🏠 **传统方式**：每个程序都需要在自己的"房子"里运行，需要安装不同的环境
📦 **Docker方式**：所有程序都放在标准的"集装箱"里，可以轻松搬运和部署

## 第一步：安装Docker Desktop

### Windows系统安装

1. **检查系统要求**
   - Windows 10 64位专业版/企业版/教育版
   - 或者 Windows 11
   - 至少4GB内存

2. **下载Docker Desktop**
   - 访问：https://www.docker.com/products/docker-desktop
   - 点击"Download for Windows"
   - 下载完成后双击安装包

3. **安装过程**
   ```
   1. 双击安装包
   2. 点击"OK"开始安装
   3. 等待安装完成
   4. 重启电脑
   ```

4. **验证安装**
   - 打开命令提示符（按Win+R，输入cmd）
   - 输入以下命令：
   ```bash
   docker --version
   ```
   - 如果显示版本号，说明安装成功

### 常见安装问题

**问题1：提示需要WSL2**
```powershell
# 以管理员身份打开PowerShell，运行：
wsl --install
# 重启电脑
```

**问题2：提示需要Hyper-V**
- 打开"控制面板" → "程序" → "启用或关闭Windows功能"
- 勾选"Hyper-V"和"Windows Subsystem for Linux"
- 重启电脑

**问题3：Docker Desktop启动失败**
- 检查Windows Defender是否阻止
- 检查防火墙设置
- 尝试以管理员身份运行

## 第二步：Docker基本概念

### 三个重要概念

1. **镜像(Image)** 📸
   - 就像是一个"模板"或"蓝图"
   - 包含了运行程序需要的所有文件
   - 例如：Python环境 + 您的代码 + 依赖包

2. **容器(Container)** 📦
   - 根据镜像创建出来的"运行实例"
   - 就像根据蓝图建造的房子
   - 可以启动、停止、删除

3. **Dockerfile** 📝
   - 制作镜像的"说明书"
   - 告诉Docker如何构建镜像

### 简单类比
```
Dockerfile = 建筑图纸
Image = 房屋模板
Container = 实际建造的房子
```

## 第三步：Docker基本命令

### 查看Docker信息
```bash
# 查看Docker版本
docker --version

# 查看Docker系统信息
docker info

# 查看运行中的容器
docker ps

# 查看所有容器（包括停止的）
docker ps -a
```

### 镜像操作
```bash
# 查看本地镜像
docker images

# 拉取镜像（从网络下载）
docker pull python:3.9

# 删除镜像
docker rmi 镜像名称
```

### 容器操作
```bash
# 运行容器
docker run 镜像名称

# 后台运行容器
docker run -d 镜像名称

# 停止容器
docker stop 容器ID

# 启动已停止的容器
docker start 容器ID

# 删除容器
docker rm 容器ID
```

## 第四步：部署您的YOLO项目

### 1. 准备文件结构
确保您的项目文件夹包含以下文件：
```
Cloud_detection/
├── app.py              # Flask应用
├── requirements.txt    # Python依赖
├── Dockerfile         # Docker构建文件
├── docker-compose.yml # Docker Compose配置
└── models/            # 模型文件夹
    └── best.onnx      # 您的模型文件
```

### 2. 创建models文件夹
```bash
# 在项目根目录下创建models文件夹
mkdir models

# 将您的best.onnx文件复制到models文件夹
# 可以使用文件管理器直接拖拽，或使用命令：
copy "您的模型文件路径" models\best.onnx
```

### 3. 使用Docker Compose部署（推荐）

**方法一：使用批处理脚本（最简单）**
```bash
# 双击运行deploy.bat文件
# 或者在命令提示符中运行：
deploy.bat
```

**方法二：手动执行命令**
```bash
# 1. 构建并启动服务
docker-compose up -d --build

# 2. 查看服务状态
docker-compose ps

# 3. 查看日志
docker-compose logs -f
```

### 4. 验证部署
```bash
# 测试健康检查接口
curl http://localhost:5000/health

# 或者用浏览器访问：
# http://localhost:5000/health
```

## 第五步：常用管理命令

### 查看服务状态
```bash
# 查看运行中的容器
docker-compose ps

# 查看所有容器
docker-compose ps -a
```

### 查看日志
```bash
# 查看实时日志
docker-compose logs -f

# 查看最近100行日志
docker-compose logs --tail=100
```

### 停止和重启
```bash
# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 重新构建并启动
docker-compose up -d --build
```

### 清理资源
```bash
# 停止并删除容器
docker-compose down

# 删除镜像
docker rmi yolo-detection-api

# 清理未使用的资源
docker system prune
```

## 第六步：故障排除

### 常见问题及解决方案

**问题1：端口被占用**
```bash
# 查看端口占用
netstat -ano | findstr :5000

# 修改docker-compose.yml中的端口映射
# 将 "5000:5000" 改为 "8080:5000"
```

**问题2：模型文件找不到**
```bash
# 检查模型文件是否存在
dir models\best.onnx

# 确保文件路径正确
# 模型文件应该在 models/best.onnx
```

**问题3：内存不足**
```bash
# 减少Docker内存使用
# 在Docker Desktop设置中调整内存限制
# 或者减少gunicorn worker数量
```

**问题4：构建失败**
```bash
# 查看详细错误信息
docker-compose build --no-cache

# 检查网络连接
docker pull python:3.9
```

### 查看详细日志
```bash
# 查看构建日志
docker-compose build --no-cache

# 查看运行日志
docker-compose logs -f yolo-detection-api

# 进入容器内部调试
docker-compose exec yolo-detection-api bash
```

## 第七步：测试API

### 使用测试脚本
```bash
# 运行API测试
python test_api.py

# 运行客户端示例
python client_example.py
```

### 手动测试
```bash
# 健康检查
curl http://localhost:5000/health

# 文件上传检测
curl -X POST http://localhost:5000/detect \
  -F "image=@test_image.jpg"
```

## 第八步：云端部署

### 部署到云服务器
1. **上传代码到服务器**
   ```bash
   # 使用scp上传
   scp -r . user@your-server:/path/to/project/
   
   # 或使用Git
   git push origin main
   ```

2. **在服务器上部署**
   ```bash
   cd /path/to/project
   chmod +x deploy.sh
   ./deploy.sh
   ```

### 部署到云平台
1. **阿里云/腾讯云容器服务**
   - 创建容器服务实例
   - 上传代码或连接Git仓库
   - 配置构建规则

2. **使用云函数**
   - 将代码打包为容器镜像
   - 上传到云函数平台
   - 配置触发器

## 总结

通过这个教程，您应该能够：
✅ 安装Docker Desktop
✅ 理解Docker基本概念
✅ 使用Docker部署您的YOLO项目
✅ 管理Docker容器和服务
✅ 排查常见问题
✅ 部署到云端

记住：Docker是一个强大的工具，刚开始可能会觉得复杂，但一旦掌握，会让您的开发和部署变得非常简单！

## 下一步学习

1. **Docker网络**：了解容器间通信
2. **Docker数据卷**：持久化数据存储
3. **Docker Swarm**：容器编排
4. **Kubernetes**：大规模容器管理

祝您Docker学习愉快！🚀 