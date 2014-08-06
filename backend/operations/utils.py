import json

from .models import Operation, Workflow
from orchestra_core import op_register, wf_register
from orchestra_core.utils import get_async_result, reset_async_result, generate_uuid
from rest_framework.exceptions import APIException



def run_operation(op, data):
    """
    runs an operation (stored in db)
    """
    #let's check arguments
    meta = op_register.meta[op.name]
    args = []
    args_not_found = []
    
    partials = op.partials or {}

    if(op.task):
        reset_async_result(op.task)

    for arg in meta['args']:
        if arg not in data:
            
            if arg in partials:
                try:
                    res = get_async_result(partials[arg])
                    args.append(res)
                except:
                    args_not_found.append(arg)

            else:
                args_not_found.append(arg)

        else:
            args.append(data[arg])

    

    if args_not_found:
        raise APIException("Missing arguments, %s" % ','.join(args_not_found))    

    task = op_register.reg[op.name]
    run_args = {'args' : args}

    
    res = task.apply_async(args, task_id = op.assigned_id)
    
    task_id = res.task_id
    op.task = task_id
    op.args = json.dumps(run_args)
    op.save()

    return op


class ConnectedWorkflow(object):

    def __init__(self, name=None, assigned_id=None):
        self.name = name
        self.assigned_id = assigned_id or generate_uuid()
        
        self.ops = []
        self.ops_ids = {}

    def get_operation(self, name):
        op_fun = op_register.get_function(name)
        op = Operation(name=name, assigned_id=generate_uuid())
        return op

    def add_operation(self, op):
        self.ops.append(op)
        #TODO: check assigned ids
        self.ops_ids[op.assigned_id] = True

    def connect(self, op1, op2, connector):
        connector(op1,op2)


    def save(self):
        """
        save all operations and the workflow
        """
        try:
            workflow = Workflow.objects.get(assigned_id=self.assigned_id)
        except Workflow.DoesNotExist:
            workflow = Workflow(name=self.name, assigned_id=self.assigned_id)
            workflow.save()

        for op in self.ops:
            op.workflow = workflow
            op.save()



    def load(self):
        wf = Workflow.objects.get(assigned_id=self.assigned_id)
        self.ops = wf.operation_set.all()
        self.name = wf.name



def create_workflow(name):
    """
    get workflow from register and created associated operations
    chaining them via partial args
    """

    wf_fun = wf_register.get_function(name)
    w = ConnectedWorkflow(name=name)
    wf_fun(w)
    w.save()
    return w.assigned_id



def load_workflow(wf_id):
    """
   
    """
    w = ConnectedWorkflow(assigned_id=wf_id)
    w.load()
    return w

    






    

