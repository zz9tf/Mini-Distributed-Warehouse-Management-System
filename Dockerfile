# 使用Python 3.11官方镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && pip install grpcio-tools

# 复制源代码
COPY . .

# 暴露端口
EXPOSE 50050 50051 50052 50053 50054

# 设置启动命令
CMD ["python", "api_gateway.py"]
