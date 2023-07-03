# ENGLISH TRAINER (in development)

## Running

### 1) Environment variables.
Fill .env file variables (fill with your ones).
Note: if you use `SQLite3`, fill in only DB_NAME, otherwise fill everything.
All variables are important,  without them server would not start.
```text
# database settings
DB_NAME=db.sqlite3
DB_HOST=localhost
DB_PORT=5432
DB_USER=admin
DB_PASSWORD=password

# services settings
OPENAI_KEY=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

# django settings
DJANGO_SECRET_KEY=django-insecure-jby(=b#pmykw!2!f(4*!!w6-r#8dzb6v84!k^r-@z%^t8$7##0
JWT_SECRET_KEY=asquwru1rpkq0-p2jdiwnjhwe

# redis settings
REDIS_HOST=localhost
REDIS_PORT=6379

# Emailing settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_FROM=suslanchikm1opl123@gmail.com
EMAIL_HOST_USER=suslan1chikmopl123@gmail.com
EMAIL_HOST_PASSWORD=pbkkplplrkhpyimz
EMAIL_PORT=587
EMAIL_USE_TLS=True

PASSWORD_RESET_TIMEOUT=14400
```

### 2) Python requirements.
Personally I use `Python 3.11`.

Install python requirements using the terminal:

```commandline
pip install -r requirements.txt
```


### 3) Redis and celery.

Run `redis` in terminal with docker.
```commandline
docker run -d -p 6379:6379 redis:5
```

Run `celery` in terminal with python (command is specialized for `Windows`).
```commandline
python -m celery --app core worker -l info -P solo
```

### 4) Django server.
Run django test server:
```commandline
cd English
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 5) Tests and linters
I use `flake8` as a liner.
```commandline
flake8
```
