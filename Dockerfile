FROM python:3.11
ENV PYTHONUNBUFFERED 1

ADD . .

WORKDIR /server
EXPOSE 8000

RUN pip install -r /requirements.txt

RUN adduser --disabled-password core-user

USER core-user
