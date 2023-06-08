# ENGLISH TRAINER (in development)

## Running

### 1) Environment variables.
Fill .env file variables (fill with your ones).
Note: if you use SQLite3, fill in only DB_NAME, otherwise fill everything.
All variables are important,  without them server would not start.
```text
DB_NAME=...
DB_HOST=...
DB_PORT=...
DB_USER=...
DB_PASSWORD=...
OPENAI_KEY=...
JWT_SECRET_KEY=...
DJANGO_SECRET_KEY
```

Settings for SQLite3 (example):
```text
DB_NAME=database.sqlite3
OPENAI_KEY=...
JWT_SECRET_KEY=93kofai3-iiqpwr-9fqowqri1kdqiurnr
DJANGO_SECRET_KEY=django-insecure-jby(=b#pmykw!2!f(4*!!w6-asd=8dzb6v8aikos4!k^r-@z%^t8$7##0
```

Settings for PostgreSQL (example):
```text
DB_NAME=english
DB_HOST=locahost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=password
OPENAI_KEY=...
JWT_SECRET_KEY=93kofai3-iiqpwr-9fqowqri1kdqiurnr
DJANGO_SECRET_KEY=django-insecure-jby(=b#pmykw!2!f(4*!!w6-asd=8dzb6v8aikos4!k^r-@z%^t8$7##0
```

### 2) Python requirements.
Personally I use Python 3.11.

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

