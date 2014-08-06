from django.db import models
from orchestra_core import op_register, wf_register
from operations.connectors import simple_connector
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

op_register.register_operation('sum', add)
op_register.register_operation('mul', mul)



def sum_and_mul(w):

    s_op = w.get_operation('sum')
    w.add_operation(s_op)

    m_op = w.get_operation('mul')
    w.add_operation(m_op)

    
    conn1 = simple_connector("a")
    w.connect(s_op, m_op, conn1)
    print "doing fine"



wf_register.register_workflow('sum_and_mul', sum_and_mul)


