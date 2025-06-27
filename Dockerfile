# 阶段1: 构建环境
FROM python:3.10-alpine AS builder

# 1. 替换为国内源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

# 2. 安装编译工具和运行时依赖（注意分号和续行）
RUN apk add --no-cache \
    build-base \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    # 常用库支持
    python3-dev;

# 3. 设置清华源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 4. 安装依赖（先确认文件存在）
COPY requirements.txt .
RUN ls -la requirements.txt && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

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