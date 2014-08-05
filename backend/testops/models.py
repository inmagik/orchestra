from django.db import models
from core import register
from celery import task
from backend.celery import app
# Create your models here.


#TODO: these registrations should be placed elsewhere.
#django 1.7 should make it easy 

@app.task()
def add(a,b):
    return a+b

@app.task()
def mul(a,b):
    return a*b

register.register_operation('sum', add)
register.register_operation('multiply', mul)
