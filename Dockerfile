# 使用官方Python镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将当前目录内容复制到容器的/app目录下
COPY . /app

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 5000

# 定义环境变量（如果需要，例如设置FLASK_APP）
# ENV FLASK_APP=app.py

# 运行应用
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "app:app"]