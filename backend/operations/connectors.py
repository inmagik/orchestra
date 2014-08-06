

def simple_connector(to):
    def connect(a,b):
        a.partials = a.partials or {}
        a.partials[to] = b.assigned_id

    return connect
