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
    else
        echo "错误: .env.example文件不存在"
        exit 1
    fi
fi

# 提示用户修改.env文件
echo "请确认已正确配置.env文件中的环境变量，特别是SECRET_KEY和数据库连接信息"
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