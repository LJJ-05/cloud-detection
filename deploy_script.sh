#!/bin/bash

# 云检测API自动部署脚本
# 使用方法: ./deploy_script.sh

set -e

echo "=== 云检测API部署脚本 ==="
echo "开始部署..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose未安装，请先安装docker-compose"
    exit 1
fi

# 检查模型文件是否存在
if [ ! -f "./models/best.pt" ]; then
    echo "❌ 模型文件 ./models/best.pt 不存在"
    echo "请确保模型文件在正确位置"
    exit 1
fi

# 停止现有容器（如果存在）
echo "📦 停止现有容器..."
docker-compose down 2>/dev/null || true

# 构建和启动服务
echo "🚀 构建和启动服务..."
docker-compose -f docker-compose.prod.yml up -d --build

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 健康检查
echo "🔍 执行健康检查..."
if curl -f http://localhost:5000/health &> /dev/null; then
    echo "✅ 部署成功！"
    echo "📊 服务状态："
    docker-compose -f docker-compose.prod.yml ps
    echo ""
    echo "🌐 API访问地址："
    echo "   健康检查: http://localhost:5000/health"
    echo "   检测接口: http://localhost:5000/detect"
    echo ""
    echo "📝 查看日志: docker-compose -f docker-compose.prod.yml logs -f"
else
    echo "❌ 健康检查失败"
    echo "📝 查看错误日志："
    docker-compose -f docker-compose.prod.yml logs
    exit 1
fi 