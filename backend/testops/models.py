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


@app.task()
def download_file(filename):
    time.sleep(100)
    return filename

@app.task()
def import_to_postgres(filename):
    time.sleep(100)
    return filename


op_register.register_operation('sum', add)
op_register.register_operation('mul', mul)
op_register.register_operation('download_file', download_file)
op_register.register_operation('import_to_postgres', import_to_postgres)



def sum_and_mul(w):

    s_op = w.get_operation('sum')
    s_op.partials = {"b" : 1, "a" : 10}
    w.add_operation(s_op)

    m_op = w.get_operation('mul')
    m_op.partials = {"b" : 2}
    w.add_operation(m_op)

    conn = simple_celery_connector("a")
    w.connect(s_op, m_op, conn)

    m_op2 = w.get_operation('mul')
    m_op2.partials = {"b" : 5}
    w.add_operation(m_op2)

    conn2 = simple_celery_connector("a")
    w.connect(m_op, m_op2, conn)
    
    




def download_and_import(w):

    d_op = w.get_operation('download_file')
    w.add_operation(d_op)

    i_op = w.get_operation('import_to_postgres')
    w.add_operation(i_op)
    
    conn = simple_celery_connector("filename")
    w.connect(d_op, i_op, conn)


    


wf_register.register_workflow('sum_and_mul', sum_and_mul)
wf_register.register_workflow('download_and_import', download_and_import)


