FROM python:3.10-alpine

# 1. 系统源替换
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

# 2. 安装核心编译工具
RUN apk add --no-cache build-base gcc musl-dev libffi-dev openssl-dev

# 3. 复制依赖定义
COPY requirements.txt constraints.txt ./

# 4. 设置清华源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 5. 精确安装
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -c constraints.txt -r requirements.txt

# 6. 清理缓存
RUN apk del build-base gcc musl-dev && \
    rm -rf /root/.cache/pip

# ... 后续代码复制和应用启动