FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /src

ADD . .

RUN pip install -r requirements.txt
