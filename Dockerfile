# 使用轻量级的 Python 3.10 基础镜像
FROM python:3.10-slim AS python-build

# 设置工作目录
WORKDIR /app

# 复制 Python 依赖文件
COPY requirements.txt /app/

# 安装 Python 依赖
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

# 安装 cron
RUN apt-get update && apt-get install -y cron

# 复制项目文件
COPY . /app

# 复制 crontab 文件并设置权限
COPY crontab /etc/cron.d/ssq-cron
RUN chmod 0644 /etc/cron.d/ssq-cron && \
    crontab /etc/cron.d/ssq-cron

# 使用轻量级的 Nginx 镜像
FROM nginx:alpine AS final-stage

# 复制前端构建文件到Nginx默认目录
COPY web/ssq /usr/share/nginx/html

# 从Python构建阶段复制Python依赖和代码
COPY --from=python-build /app /app

# 安装必要的依赖
RUN apk add --no-cache python3 py3-pip bash

# 安装 crond 并启动服务
RUN apk add --no-cache dcron

# 创建Python虚拟环境并安装依赖
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir --upgrade pip setuptools && \
    /app/venv/bin/pip install -r /app/requirements.txt

# 暴露端口
EXPOSE 11020

# 启动crond服务、FastAPI应用和Nginx
CMD ["sh", "-c", "crond -f && /app/venv/bin/python /app/main.py & nginx -g 'daemon off;'"]