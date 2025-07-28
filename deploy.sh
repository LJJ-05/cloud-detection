#!/bin/bash

# YOLO检测API快速部署脚本

echo "=== YOLO检测API部署脚本 ==="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 创建models目录
echo "1. 创建models目录..."
mkdir -p models

# 检查模型文件是否存在
if [ ! -f "models/best.onnx" ]; then
    echo "警告: models/best.onnx 文件不存在"
    echo "请将您的best.onnx模型文件复制到models/目录下"
    echo "然后重新运行此脚本"
    exit 1
fi

echo "✓ 模型文件检查通过"

# 构建并启动服务
echo ""
echo "2. 构建并启动Docker服务..."
docker-compose up -d --build

# 等待服务启动
echo ""
echo "3. 等待服务启动..."
sleep 10

# 检查服务状态
echo ""
echo "4. 检查服务状态..."
if docker-compose ps | grep -q "Up"; then
    echo "✓ 服务启动成功"
else
    echo "✗ 服务启动失败"
    echo "查看日志:"
    docker-compose logs
    exit 1
fi

# 测试健康检查
echo ""
echo "5. 测试API健康检查..."
if curl -s http://localhost:5000/health > /dev/null; then
    echo "✓ API健康检查通过"
else
    echo "✗ API健康检查失败"
    echo "请检查服务日志: docker-compose logs"
    exit 1
fi

echo ""
echo "=== 部署完成 ==="
echo "API服务地址: http://localhost:5000"
echo ""
echo "可用接口:"
echo "- 健康检查: GET http://localhost:5000/health"
echo "- 单张检测: POST http://localhost:5000/detect"
echo "- 批量检测: POST http://localhost:5000/detect_batch"
echo ""
echo "管理命令:"
echo "- 查看日志: docker-compose logs -f"
echo "- 停止服务: docker-compose down"
echo "- 重启服务: docker-compose restart"
echo ""
echo "运行测试: python test_api.py" 