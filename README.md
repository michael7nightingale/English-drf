# ENGLISH TRAINER (in development)

### Running

.env file (fill with your ones):
```text
DB_NAME=...
DB_HOST=...
DB_POST=...
DB_USER=...
DB_PASSWORD=...
OPENAI_KEY=..
```

Install python requirements:

```commandline
pip install -r requirements.txt
```

Run django`s test server:

```commandline
cd English
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
