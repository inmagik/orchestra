import inspect


class OperationRegister(object):
    """
    This class holds reference to operations
    """
    
    reg = {}
    meta = {}


    def register_operation(self, name, fun):

        if name in self.reg:
            raise KeyError("Key %s already present in register" % name)

        argspec = inspect.getargspec(fun.run)
        self.reg[name] = fun
        n = ["args", "varargs", "keywords", "defaults"]
        self.meta[name] = dict(zip(n,argspec))

    def get_function(self, name):
        return self.reg[name]

    



register = OperationRegister()