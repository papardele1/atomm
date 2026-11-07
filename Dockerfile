FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir playwright==1.48.0 \
 && playwright install --with-deps chromium \
 && rm -rf /var/lib/apt/lists/*
COPY app ./app
COPY site ./site
ENV ATOMM_SITE=/app/site ATOMM_CATALOG=/www/catalog.json ATOMM_DB=/data/orders.db PYTHONUNBUFFERED=1
EXPOSE 8080
CMD ["uvicorn", "api:app", "--app-dir", "/app/app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers", "--forwarded-allow-ips", "*"]
