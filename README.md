# 🌤️ 云检测AI模型API服务

这是一个基于**YOLO PyTorch模型**的智能云层检测API服务，使用Flask + Docker构建，支持云端部署。

## ✨ 功能特性

- 🔍 **智能检测**：基于YOLOv8的云层识别
- 📤 **多种输入**：支持文件上传和Base64编码
- 🌐 **Web界面**：精美的在线演示页面
- 🐳 **容器化**：Docker一键部署
- ☁️ **云端部署**：支持Railway、Render等平台
- 📊 **健康检查**：实时服务状态监控

## 🏗️ 项目结构

```
Cloud_detection/
├── app_pytorch.py           # Flask API主应用
├── static/index.html        # 网页演示界面
├── models/best.pt          # YOLO PyTorch模型
├── requirements_optimized.txt # 云端优化依赖
├── Dockerfile.railway       # Railway平台配置
├── render.yaml             # Render平台配置
├── railway.json            # Railway部署配置
└── 部署指南_*.md           # 各平台部署指南
```

## 🚀 快速开始

### 本地运行

```bash
# 1. 克隆项目
git clone https://github.com/LJJ-05/cloud-detection.git
cd cloud-detection

# 2. 安装依赖
pip install -r requirements_optimized.txt

# 3. 启动服务
python app_pytorch.py

# 4. 访问网页界面
# http://localhost:5000
```

### Docker部署

```bash
# 构建并运行
docker build -f Dockerfile.railway -t cloud-detection .
docker run -p 5000:5000 cloud-detection

# 或使用docker-compose
docker-compose up -d
```

## ☁️ 云端部署

### 🌟 Render平台 (推荐免费)

1. 访问 [render.com](https://render.com)
2. 连接GitHub仓库：`LJJ-05/cloud-detection`
3. 选择Web Service，自动部署
4. 获得公网URL：`https://cloud-detection.onrender.com`

### 🚂 Railway平台

1. 访问 [railway.app](https://railway.app)
2. 从GitHub部署此仓库
3. 自动检测配置并构建

详细部署指南请查看：`部署指南_*.md` 文件

## 🔗 API接口

### 健康检查
```bash
GET /health
```

### 图像检测
```bash
POST /detect
Content-Type: multipart/form-data

参数:
- image: 图像文件
- conf_threshold: 置信度阈值 (默认0.5)
- nms_threshold: NMS阈值 (默认0.4)
```

### 响应格式
```json
{
  "success": true,
  "total_detections": 2,
  "predictions": [
    {
      "bbox": [100, 50, 200, 150],
      "confidence": 0.85,
      "class_id": 0,
      "class_name": "cloud"
    }
  ],
  "timestamp": "2024-01-01T12:00:00"
}
```

## 🖥️ 网页演示

访问根路径 `/` 即可使用精美的网页界面：
- 📸 拖拽上传图片
- ⚙️ 调整检测参数
- 📊 可视化结果展示
- 📱 支持移动端访问

## 🛠️ 技术栈

- **AI框架**：PyTorch + Ultralytics YOLOv8
- **Web框架**：Flask + Gunicorn
- **前端**：原生HTML/CSS/JavaScript
- **容器化**：Docker
- **云平台**：Railway, Render, 阿里云, 腾讯云

## 📊 性能优化

- 🏃‍♂️ **轻量化模型**：优化的PyTorch模型
- 🔄 **智能缓存**：pip缓存清理
- 👤 **安全运行**：非root用户
- 📦 **多阶段构建**：减小镜像大小

## 🤝 使用示例

### Python调用
```python
import requests

url = "https://your-app.onrender.com/detect"
files = {'image': open('test.jpg', 'rb')}
response = requests.post(url, files=files)
print(response.json())
```

### JavaScript调用
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);

fetch('/detect', {
    method: 'POST',
    body: formData
}).then(response => response.json())
  .then(data => console.log(data));
```

## 📄 许可证

MIT License

## 🌟 特性预览

部署成功后，您将拥有：
- 🌐 **公网访问**：任何人都可以使用的AI服务
- 📱 **移动友好**：响应式设计，支持手机访问  
- 🔒 **安全可靠**：HTTPS加密，健康检查
- 💡 **易于集成**：标准REST API，支持各种编程语言

---

**�� 让您的AI模型为全世界服务！** 