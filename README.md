# YOLO能效标识检测API服务

这是一个基于YOLO模型的能效标识检测API服务，使用Flask和ONNX Runtime构建。

## 功能特性

- 支持单张图片检测
- 支持批量图片检测
- 支持文件上传和Base64编码两种输入方式
- 提供健康检查接口
- Docker容器化部署

## 项目结构

```
Cloud_detection/
├── app.py                 # Flask应用主文件
├── requirements.txt       # Python依赖
├── Dockerfile            # Docker镜像构建文件
├── docker-compose.yml    # Docker Compose配置
├── .dockerignore         # Docker忽略文件
├── README.md             # 项目说明
└── models/               # 模型文件目录
    └── best.onnx         # YOLO模型文件
```

## 部署步骤

### 1. 准备模型文件

将您的`best.onnx`模型文件放到`models/`目录下：

```bash
mkdir models
cp /path/to/your/best.onnx models/
```

### 2. 本地Docker部署

#### 方法一：使用Docker Compose（推荐）

```bash
# 构建并启动服务
docker-compose up --build

# 后台运行
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

#### 方法二：使用Docker命令

```bash
# 构建镜像
docker build -t yolo-detection-api .

# 运行容器
docker run -d \
  --name yolo-detection \
  -p 5000:5000 \
  -v $(pwd)/models:/app/models \
  yolo-detection-api

# 查看日志
docker logs -f yolo-detection

# 停止容器
docker stop yolo-detection
docker rm yolo-detection
```

### 3. 云端部署

#### 部署到云服务器

1. **上传代码到服务器**
```bash
# 使用scp或git上传代码
scp -r . user@your-server:/path/to/project/
```

2. **在服务器上部署**
```bash
cd /path/to/project
docker-compose up -d --build
```

#### 部署到云平台

**阿里云/腾讯云/华为云等：**

1. 在云平台创建ECS实例
2. 安装Docker和Docker Compose
3. 上传代码并运行上述Docker命令

**使用云容器服务：**

1. 将代码推送到Git仓库
2. 在云平台创建容器服务
3. 配置构建规则和部署参数

## API接口说明

### 1. 健康检查

```bash
GET http://localhost:5000/health
```

响应示例：
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "model_loaded": true
}
```

### 2. 单张图片检测

#### 文件上传方式

```bash
curl -X POST http://localhost:5000/detect \
  -F "image=@/path/to/image.jpg"
```

#### Base64编码方式

```bash
curl -X POST http://localhost:5000/detect \
  -H "Content-Type: application/json" \
  -d '{
    "image_base64": "base64_encoded_image_string",
    "conf_threshold": 0.5,
    "nms_threshold": 0.4
  }'
```

响应示例：
```json
{
  "success": true,
  "predictions": [
    {
      "bbox": [100, 200, 300, 400],
      "confidence": 0.95,
      "class_id": 0,
      "class_name": "energy_label_0"
    }
  ],
  "total_detections": 1,
  "timestamp": "2024-01-01T12:00:00"
}
```

### 3. 批量检测

```bash
curl -X POST http://localhost:5000/detect_batch \
  -H "Content-Type: application/json" \
  -d '{
    "images": ["base64_image_1", "base64_image_2"],
    "conf_threshold": 0.5,
    "nms_threshold": 0.4
  }'
```

## 环境变量配置

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| MODEL_PATH | /app/models/best.onnx | 模型文件路径 |
| FLASK_ENV | production | Flask环境 |
| FLASK_APP | app.py | Flask应用文件 |

## 性能优化建议

1. **GPU加速**：如果有GPU，可以修改Dockerfile使用GPU版本的ONNX Runtime
2. **多进程**：调整gunicorn的worker数量
3. **缓存**：添加Redis缓存层
4. **负载均衡**：使用Nginx做反向代理

## 故障排除

### 常见问题

1. **模型加载失败**
   - 检查模型文件路径是否正确
   - 确认模型文件格式为ONNX

2. **内存不足**
   - 减少gunicorn worker数量
   - 增加服务器内存

3. **端口被占用**
   - 修改docker-compose.yml中的端口映射
   - 检查是否有其他服务占用5000端口

### 日志查看

```bash
# Docker Compose日志
docker-compose logs -f

# Docker容器日志
docker logs -f container_name

# 应用日志
docker exec -it container_name tail -f /app/app.log
```

## 安全建议

1. 添加API认证机制
2. 限制文件上传大小
3. 添加请求频率限制
4. 使用HTTPS
5. 定期更新依赖包

## 监控和维护

1. 设置健康检查
2. 配置日志收集
3. 设置自动重启策略
4. 监控资源使用情况 