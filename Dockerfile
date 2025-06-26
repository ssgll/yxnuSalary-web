# 使用多阶段构建减小镜像体积
# 阶段1: 构建环境
FROM python:3.10-alpine AS builder

# 1. 替换为国内源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

# 2. 安装编译工具和运行时依赖
RUN apk add --no-cache \
    build-base \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev 
    # 常用库支持


# 3. 设置清华源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 4. 安装依赖
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# -------------------------------
# 阶段2: 生产环境
FROM python:3.10-alpine

# 从构建阶段复制已安装包
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/bin /usr/bin


# 设置工作目录和用户
WORKDIR /app
RUN adduser -D myuser
USER myuser

# 复制应用代码
COPY --chown=myuser:myuser . .

# 清理环境变量避免干扰
ENV PYTHONPATH=/usr/local/lib/python3.10/site-packages

# 暴露端口
EXPOSE 5000

# 启动命令（使用 gunicorn）
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app:app"]