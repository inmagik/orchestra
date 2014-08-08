from django.db import models
from orchestra_core import op_register, wf_register
from operations.connectors import simple_celery_connector
from celery import task
from backend.celery import app
import time
from operations.utils import get_registered_op
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



def sum_and_mul():

    s_op = get_registered_op('sum')
    s_op.partials = {'b' : 1, 'a' : 10}
    
    m_op = get_registered_op('mul')
    m_op.partials = {'b' : 2}
    

    m_op.connect_op(s_op, "a")

    
    m_op2 = get_registered_op('mul')
    m_op2.partials = {'a' : 5}

    m_op2.connect_op(m_op, 'a')
    

    return [s_op, m_op, m_op2]
    




def download_and_import():

    d_op = get_registered_op('download_file')
    i_op = get_registered_op('import_to_postgres')
    i_op.connect_op(d_op, 'filename')
    
    return [d_op, i_op]

    


wf_register.register_workflow('sum_and_mul', sum_and_mul)
wf_register.register_workflow('download_and_import', download_and_import)


