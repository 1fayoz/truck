FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY ./requirements/develop.txt /app/requirements/develop.txt
COPY ./requirements/base.txt /app/requirements/base.txt
COPY ./requirements/production.txt /app/requirements/production.txt

RUN pip install --upgrade pip
RUN pip install -r /app/requirements/production.txt
RUN pip install gunicorn

RUN apt-get update && \
    apt-get install -y redis-tools postgresql-client && \
    rm -rf /var/lib/apt/lists/*

RUN ln -sf /usr/share/zoneinfo/Asia/Tashkent /etc/localtime && \
    echo "Asia/Tashkent" > /etc/timezone

COPY . .

RUN chmod a+x /app/*

EXPOSE 8000

CMD ["gunicorn", "app:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
