import uuid

from celery.result import AsyncResult
from celery.task.control import revoke

def generate_uuid():
    return str(uuid.uuid1())


def reset_async_result(id, backend="celery"):
    if backend == 'celery':
        res = AsyncResult(id)
        if res:
            res.forget()


def revoke_if_running(task_id):
    return
    res = AsyncResult(task_id)
    if res.ready():
        return

    try:
        a = revoke(task_id, terminate=True)
        print "task id revoked", a
    except:
        pass



def get_async_result(id, backend="celery"):
    if backend == 'celery':
        res = AsyncResult(id)
        if res.ready():
            return res.get()

    raise ValueError("no result")
    

def get_async_state(id, backend="celery"):
    if backend == 'celery':
        res = AsyncResult(id)
        return res.state

    return None    


