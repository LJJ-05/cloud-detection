# 阿里云ECS部署指南

## 1. 购买阿里云ECS实例

### 推荐配置：
- **CPU**: 2核心或以上
- **内存**: 4GB或以上
- **系统盘**: 40GB SSD
- **带宽**: 1Mbps或以上
- **操作系统**: Ubuntu 20.04 LTS

### 安全组设置：
- 开放端口5000（用于API访问）
- 开放端口22（SSH访问）

## 2. 连接服务器并安装Docker

```bash
# 连接到服务器
ssh root@your_server_ip

# 更新系统
apt update && apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 安装docker-compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 启动Docker服务
systemctl start docker
systemctl enable docker
```

## 3. 部署应用

```bash
# 创建项目目录
mkdir -p /home/cloud-detection
cd /home/cloud-detection

# 上传项目文件（或使用git克隆）
# 可以使用scp命令上传文件，或者git clone

# 构建并启动服务
docker-compose up -d

# 查看运行状态
docker-compose ps
docker-compose logs -f
```

## 4. 配置域名和SSL（可选）

如果您有域名，可以配置Nginx反向代理和SSL证书：

```bash
# 安装Nginx
apt install nginx -y

# 创建Nginx配置
cat > /etc/nginx/sites-available/cloud-detection << 'EOF'
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 10M;
    }
}
EOF

# 启用配置
ln -s /etc/nginx/sites-available/cloud-detection /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

## 5. 访问测试

```bash
# 健康检查
curl http://your_server_ip:5000/health

# 如果配置了域名
curl http://your-domain.com/health
```

## 成本估算
- ECS实例：约50-100元/月
- 带宽费用：根据流量计费
- 总计：约60-120元/月 