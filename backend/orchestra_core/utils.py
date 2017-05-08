import uuid

from celery.task.control import revoke

from celery.result import AsyncResult


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


def resolve_partial(partial):
    if type(partial) == dict:

        if 'backend' not in partial:
            raise ValueError('Backend not specified in partial')
        if partial['backend'] == 'celery':
            return get_async_result(partial['source'])

    return partial
