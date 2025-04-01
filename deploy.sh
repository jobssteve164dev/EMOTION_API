#!/bin/bash

echo "========== 情感分析引擎部署脚本 =========="
echo "正在准备部署环境..."

# 检查Docker和Docker Compose是否已安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker未安装，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 检查环境变量文件
if [ ! -f .env ]; then
    echo "环境变量文件不存在，正在从示例文件创建..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "已创建.env文件，请根据需要修改其中的配置"
        
        # 自动生成随机密码
        SECRET_KEY=$(openssl rand -base64 24 2>/dev/null || head -c 24 /dev/urandom | base64)
        MONGO_ROOT_PWD=$(openssl rand -base64 16 2>/dev/null || head -c 16 /dev/urandom | base64)
        MONGO_USER_PWD=$(openssl rand -base64 16 2>/dev/null || head -c 16 /dev/urandom | base64)
        
        # 替换.env文件中的默认密码
        sed -i'.bak' "s|SECRET_KEY=.*|SECRET_KEY=$SECRET_KEY|g" .env 2>/dev/null || sed -i "s|SECRET_KEY=.*|SECRET_KEY=$SECRET_KEY|g" .env
        sed -i'.bak' "s|MONGODB_ROOT_PASSWORD=.*|MONGODB_ROOT_PASSWORD=$MONGO_ROOT_PWD|g" .env 2>/dev/null || sed -i "s|MONGODB_ROOT_PASSWORD=.*|MONGODB_ROOT_PASSWORD=$MONGO_ROOT_PWD|g" .env
        sed -i'.bak' "s|MONGODB_PASSWORD=.*|MONGODB_PASSWORD=$MONGO_USER_PWD|g" .env 2>/dev/null || sed -i "s|MONGODB_PASSWORD=.*|MONGODB_PASSWORD=$MONGO_USER_PWD|g" .env
        
        # 删除备份文件
        rm -f .env.bak 2>/dev/null

        echo "已自动生成安全的随机密码"
    else
        echo "错误: .env.example文件不存在"
        exit 1
    fi
fi

# 提示用户检查环境变量
echo ""
echo "请确认已正确配置.env文件中的环境变量，特别注意以下安全相关设置:"
echo "- SECRET_KEY: JWT认证密钥"
echo "- MONGODB_ROOT_PASSWORD: MongoDB根用户密码"
echo "- MONGODB_PASSWORD: 应用数据库用户密码"
echo ""
echo "在生产环境中，请确保这些密码是强密码且保密存储"
read -p "按回车键继续..." continue

# 构建和启动服务
echo "正在构建和启动服务..."
docker-compose build
docker-compose up -d

# 检查服务是否启动成功
echo "检查服务状态..."
sleep 5
docker-compose ps

echo "========== 部署完成 =========="
echo "API文档: http://localhost:8000/api/docs"
echo "健康检查: http://localhost:8000/health"
echo ""
echo "以下命令可能有用:"
echo "- 查看API服务日志: docker-compose logs -f api"
echo "- 停止所有服务: docker-compose down"
echo "- 重启所有服务: docker-compose restart"
echo ""
echo "默认管理员账号: admin"
echo "默认管理员密码: admin123"
echo "请在首次登录后修改默认密码!" 