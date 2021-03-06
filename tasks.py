from celery import Celery
from flask import Flask
from flask_mail import Message
import config
from externs import mail

app = Flask(__name__)
app.config.from_object(config)
mail.init_app(app)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)


@celery.task
def send_mail(subject, recipients, body):
    message = Message(subject=subject, recipients=recipients, body=body)
    mail.send(message)


#celery -A tasks.celery worker --loglevel=info

