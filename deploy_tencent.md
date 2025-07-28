# 腾讯云CVM部署指南

## 1. 购买腾讯云CVM实例

### 推荐配置：
- **CPU**: 2核心
- **内存**: 4GB
- **系统盘**: 50GB SSD
- **带宽**: 1Mbps
- **操作系统**: Ubuntu Server 20.04 LTS

### 安全组配置：
- 入站规则：开放TCP 5000端口
- 入站规则：开放TCP 22端口（SSH）

## 2. 部署步骤

```bash
# SSH连接服务器
ssh ubuntu@your_server_ip

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 安装docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 重新登录以应用docker组权限
exit
ssh ubuntu@your_server_ip

# 上传项目文件并启动
git clone your_project_url  # 或手动上传文件
cd Cloud_detection
docker-compose up -d
```

## 3. 域名解析（可选）

如果您有域名：
1. 在腾讯云DNS解析中添加A记录
2. 指向您的CVM公网IP
3. 配置SSL证书（推荐使用Let's Encrypt）

## 成本估算
- 标准型CVM：约40-80元/月
- 带宽费用：约20-50元/月  
- 总计：约60-130元/月 