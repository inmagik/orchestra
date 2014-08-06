from django.db import models
from orchestra_core import op_register, wf_register
from operations.connectors import simple_celery_connector
from celery import task
from backend.celery import app
import time
# Create your models here.


#TODO: these registrations should be placed elsewhere.
#django 1.7 should make it easy 

@app.task()
def add(a,b):
    time.sleep(10)
    return a+b

@app.task()
def mul(a,b):
    time.sleep(10)
    return a*b

op_register.register_operation('sum', add)
op_register.register_operation('mul', mul)



def sum_and_mul(w):

    s_op = w.get_operation('sum')
    s_op.partials = {"b" : 1, "a" : 10}
    w.add_operation(s_op)

    m_op = w.get_operation('mul')
    m_op.partials = {"b" : 2}
    w.add_operation(m_op)
    
    conn1 = simple_celery_connector("a")
    w.connect(s_op, m_op, conn1)
    


wf_register.register_workflow('sum_and_mul', sum_and_mul)


