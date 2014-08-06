

def simple_celery_connector(to):
    def connect(a,b):
        b.partials = b.partials or {}
        b.partials[to] = {'backend' : 'celery', 'id' : a.oid}

    return connect
