FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /shop_app

COPY requirements.txt /shop_app/requirements.txt

RUN pip install -r /shop_app/requirements.txt

COPY . .