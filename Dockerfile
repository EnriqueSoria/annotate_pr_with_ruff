# syntax=docker/dockerfile:1

FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apk add github-cli

COPY . .

ENTRYPOINT ["python", "/app/entrypoint.py"]