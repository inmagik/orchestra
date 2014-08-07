from celery import task
from backend.celery import app
from operations.models import Operation
import datetime
from celery.result import AsyncResult

@app.task()
def notify_success(result, op_oid):
    
    op = Operation.objects.get(oid=op_oid)
    op.last_run = datetime.datetime.now()
    op.last_run_ok = True
    op.last_exception = None
    
    op.save()
    print op


@app.task()
def notify_exception(uuid, op_oid):
    result = AsyncResult(uuid)
    op = Operation.objects.get(oid=op_oid)
    op.last_run = datetime.datetime.now()
    op.last_run_ok = False
    op.last_exception = result.traceback
    op.save()
    
          