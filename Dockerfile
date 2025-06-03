FROM python:3.11-slim

# Instalar dependencias del sistema para pyzbar, locales y mysqlclient
RUN apt-get update && apt-get install -y \
    libzbar0 \
    locales \
    default-libmysqlclient-dev \
    gcc \
    build-essential \
    pkg-config \
    && locale-gen es_ES.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=es_ES.UTF-8
ENV LC_ALL=es_ES.UTF-8

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 10000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
