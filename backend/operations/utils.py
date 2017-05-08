from orchestra_core import op_register, wf_register

from .models import Operation, Workflow


class ConnectedWorkflow(object):
    """
    This class is used only to get a worflow structure without saving anything to db
    """

    def __init__(self, name=None, create_function=None):
        self.name = name
        self.ops = create_function()

        self.ops_names = {}
        self.ops_keys = {}

    def get_meta(self):
        out = {}
        out['name'] = self.name
        out['operations'] = []


        for op in self.ops:
            if op.name not in self.ops_names:
                self.ops_names[op.name] = 0;
            self.ops_names[op.name] += 1;
            self.ops_keys[op.oid] = op.name + "_" + str(self.ops_names[op.name])

        for op in self.ops:
            op_key = self.ops_keys[op.oid]
            partials = op.partials or {}
            out_partials = {}
            for k in partials:
                p = partials[k]
                if type(p) == dict and 'backend' in p:
                    op_name = self.ops_keys[p['source']]
                    out_partials[k] = { "source" : op_name }
                else:
                    out_partials[k] = partials[k]

            meta = op_register.meta[op.name]
            op_data = {"name" : op.name, "oid": op_key, "meta" : meta, "partials" : out_partials }
            out['operations'].append(op_data)

        return out


def get_registered_op(name):
    meta = op_register.get_meta(name)
    return Operation(name=name)


def create_workflow(name, ops_list, links_list=[], owner=None):

    wf = Workflow(name=name, owner=owner)
    wf.save()

    oids_to_ops = {}
    for op in ops_list:
        op.workflow = wf
        oids_to_ops[op.oid] = op

    #must build partials...
    for link in links_list:

        if 'target_arg' not in link:
            raise ValueError("no target arg in link!", link)

        target_op = link['target_op']
        target_op.partials = target_op.partials or { }

        target_arg = link['target_arg']

        if 'value' in link:
            target_op.partials[target_arg] = link['value']


        if 'source_op' in link:
            target_op.partials[target_arg] = {
                'id' : link['source_op'].oid,
                'backend' : 'celery'
            }

    
    for op in ops_list:
        op.save()

    return wf


def create_registered_workflow(name, owner=None):
    wf_fun = wf_register.get_function(name)
    ops_list = wf_fun()
    return create_workflow(name, ops_list, owner=None)


def get_workflow_meta(name):
    wf_fun = wf_register.get_function(name)
    w = ConnectedWorkflow(name=name, create_function=wf_fun)
    return w.get_meta()
    
    
    




