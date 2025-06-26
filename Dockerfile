# 国内稳定可用的镜像源（三选一）
# 1. 腾讯云镜像源
FROM python:3.10-slim-bullseye

# 2. 或者使用华为云镜像源
# FROM swr.cn-east-2.myhuaweicloud.com/library/python:3.10-slim-bullseye

# 3. 或者直接使用官方镜像（配镜像加速器）
# FROM anolis-registry.cn-zhangjiakou.cr.aliyuncs.com/openanolis/python:3.10.13-23

# ---- 以下配置保持不变 ----
WORKDIR /app

# 替换系统源（Debian）
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list

# 配置pip源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set install.trusted-host tuna.tsinghua.edu.cn

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 复制应用
COPY . .

EXPOSE 5000
CMD ["gunicorn","--workers", "4", "--bind", "0.0.0.0:5000", "app:app"]