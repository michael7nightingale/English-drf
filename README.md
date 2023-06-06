# ENGLISH TRAINER (in development)

### Running

.env file (fill with your ones):
```text
DB_NAME=db-name
DB_HOST=db-host
DB_POST=db-port
DB_USER=db-user
DB_PASSWORD=db-password
```

Install python requirements:

```commandline
pip install -r requirements.txt
```

Run django test server:

```commandline
cd English
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```


