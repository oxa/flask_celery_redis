from os import path, environ
from flask import Flask, jsonify, request
import celery_settings.py
from celery import Celery
import time

app = Flask(__name__)
app.config.from_object(celery_settings)

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task(name="tasks.asynctask1")
def asynctask1(x, y):
    time.sleep(10)
    print "I waited 10 sec"
    y = asynctask2()
    return "Result is", x + y

@celery.task(name="tasks.asynctask2")
def asynctask2():
    time.sleep(2)
    return 7

@app.route("/test")
def hello_world():
    asynctask1.apply_async((3, 4))
    return "Hello World"


if __name__ == "__main__":
    app.run(debug=True)
