Flask Celery Redis Example
==========================

## Procedure

* Install redis

```
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
```

* Install redis python module

```
pip install redis
```
* Launch redis server

```
redis-server
```

* Inside the project directory start celery worker

```
celery -A app.celery worker&
```

* start the application:

```
python app.py&
```

* Go to 127.0.0.1/test and do some request !