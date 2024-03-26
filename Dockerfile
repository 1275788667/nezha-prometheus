# 使用官方Python镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将当前目录下的所有文件复制到容器的工作目录中
COPY . /app

# 安装Python依赖
RUN pip install Flask requests

# 声明容器运行时监听的端口
EXPOSE 9091

# 定义环境变量，用于传递参数
ENV NEZHA_URL=http://nezha_url/api/v1/server/details
ENV NEZHA_TOKEN=nezha_token

# 运行Python应用
ENTRYPOINT [ "python" ]
CMD [ "app.py", "${NEZHA_URL}", "${NEZHA_TOKEN}" ]
