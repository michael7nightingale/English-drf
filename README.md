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
```

### 2) Python requirements.
Personally I use `Python 3.11`.

Install python requirements using the terminal:

```commandline
pip install -r requirements.txt
```

Run django`s test server:

### 3) Django server.

```commandline
cd English
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

These commands may be useful:
```commandline
python manage.py createsuperuser
Username: ...admin...
Email: ...Enter...
Password: ...password...
Password (Again): ...password...
```

### 4) Tests and linters
I use `flake8` as a liner.
```commandline
flake8
```
