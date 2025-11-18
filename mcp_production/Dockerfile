# Dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# 安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 把所有 .py 拷進去
COPY . .

# 預設入口給 gateway，用 docker-compose 的 command 覆蓋
CMD ["python", "gateway.py"]

