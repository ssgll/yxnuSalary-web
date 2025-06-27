# 阶段1: 构建环境
FROM python:3.10-alpine AS builder

# 1. 替换为国内源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

# 2. 安装编译工具和依赖
RUN apk add --no-cache \
    build-base \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev;

# 3. 强制使用官方源安装 Alembic
RUN pip install --no-cache-dir --index-url https://pypi.org/simple alembic==1.16.2

# 4. 安装其他依赖（使用清华源）
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
COPY requirements.txt .
RUN pip install -r requirements.txt

# -------------------------------
# -------------------------------
# 阶段2: 生产环境
FROM python:3.10-alpine

# 先创建用户（避免COPY时权限错误）
RUN adduser -D myuser

# 复制Python包（只复制必要内容）
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# 设置工作目录和用户
WORKDIR /app
USER myuser

# 复制应用代码（带权限设置）
COPY --chown=myuser:myuser . .

# 正确配置环境变量（追加而非覆盖）
ENV PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.10/site-packages

# 暴露端口
EXPOSE 5000

# 启动命令（使用gunicorn）
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app:app"]