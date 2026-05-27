FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
# Копируем установленные библиотеки
COPY --from=builder /install /usr/local
# Копируем ВЕСЬ контекст (src, tests, __init__.py)
COPY . .

EXPOSE 5000
CMD ["python", "src/main.py"]
