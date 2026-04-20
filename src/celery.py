from celery import Celery

c_app = Celery()

c_app.config_from_object('src.config')


