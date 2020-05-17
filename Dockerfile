FROM python:3.8-alpine

RUN apk add --no-cache --virtual \
        .build-deps \
        gcc \
        python3-dev \
        musl-dev \
        build-base

RUN apk add --no-cache --update postgresql postgresql-dev

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt \
    && apk del .build-deps
