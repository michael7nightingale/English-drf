# ENGLISH API (DRF)
My project is the RESTFul API for training English language. It allows to chat with ChatGPT to upgrade your skills.

## Stack
 - django[drf];
 - redis;
 - celery;
 - django-channels;

## Running

### 1) Environment variables
Fill .env file variables (fill with your ones).
Note: if you use `SQLite3`, fill in only DB_NAME, otherwise fill everything.
All variables are important,  without them server would not start.


### 2) Application startup
Run application using `Docker`.
```commandline
docker-compose up
```

### 3) Tests and linters
I use `flake8` as a liner.
```commandline
flake8
```
