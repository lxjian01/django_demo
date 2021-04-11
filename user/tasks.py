from __future__ import absolute_import
from celery import shared_task
from django_demo.celery import app
from django_demo import logcelery
from utils.email_handler import django_send_email


@shared_task
def send_register_email(username,token,email):
    try:
        django_send_email(username, token, email)
        logcelery.info("Send email username={0},token={1},email={2}".format(username, token, email))
    except Exception as ex:
        logcelery.error("Send email username={0},token={1},email={2} error by".format(username,token,email,ex))

@app.task
def test_celery():
    logcelery.info("celery test")