import uuid

from celery.result import AsyncResult

def generate_uuid():
    return str(uuid.uuid1())


def reset_async_result(id, backend="celery"):
    if backend == 'celery':
        res = AsyncResult(id)
        if res:
            res.forget()
        


def get_async_result(id, backend="celery"):
    if backend == 'celery':
        res = AsyncResult(id)
        return res.get()

    return None


def get_async_state(id, backend="celery"):
    if backend == 'celery':
        res = AsyncResult(id)
        return res.state

    return None    


