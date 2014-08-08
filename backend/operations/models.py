import json
from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField
from orchestra_core.utils import generate_uuid, resolve_partial, reset_async_result
#from .tasks import notify_success, notify_exception
from orchestra_core import op_register, wf_register

class Workflow(models.Model):
    
    owner = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=200)
    oid = models.CharField(max_length=200, null=True, blank=True, default=generate_uuid)


    def reset(self):
        pass


class Operation(models.Model):
    """
    A model to represent a single Operation
    """
    owner = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=200)
    
    #current task
    task = models.CharField(max_length=200, null=True, blank=True)
    args = JSONField(null=True, blank=True)


    partials = JSONField(null=True, blank=True)
    oid = models.CharField(max_length=200, null=True, blank=True)

    workflow = models.ForeignKey(Workflow, null=True, blank=True, related_name="operations")

    #execution data
    last_run = models.DateTimeField(null=True, blank=True)
    last_end = models.DateTimeField(null=True, blank=True)

    last_run_ok = models.NullBooleanField(null=True, blank=True)
    last_exception = models.TextField(null=True, blank=True)


    def get_meta(self):
        return op_register.get_meta(self.name)

    def get_task(self):
        return op_register.get_task(self.name)


    def get_partial(self, name):
        try:
            partial = self.partials[name]
            print "oo", partial
            value = resolve_partial(partial)
            return value

        except:
            raise ValueError


    def get_args(self):
        out = {}
        meta = self.get_meta()
        for arg in meta['args']:
            try:
                value = self.get_partial(arg)
                out[arg] = value
            except ValueError:
                pass
        return out


    def check_missing_args(self, args):
        meta = self.get_meta()
        return [x for x in meta['args'] if x not in args.keys()]
        


    def prepare_args(self, args):
        meta = self.get_meta()
        out = []
        for x in meta['args']:
            out.append(args[x])
        return out


    def run(self, run_args={}):
        
        args = self.get_args()
        args.update(run_args)

        args_missing = self.check_missing_args(args)
        if len(args_missing):
            raise

        task = self.get_task()

        if(self.task):
            #revoke_if_running(op.task)
            reset_async_result(op.task)

        run_args = self.prepare_args(args)
    
        res = task.apply_async(run_args, task_id=self.oid, 
            link=notify_success.s(self.oid),
            link_error= notify_exception.s(self.oid))

        self.task = res.task_id
        self.last_run = datetime.datetime.now()
        
        self.args = json.dumps(run_args)
        self.save()





    def reset(self):
        pass






from celery import task
from backend.celery import app
import datetime
from celery.result import AsyncResult

@app.task()
def notify_success(result, op_oid):
    
    op = Operation.objects.get(oid=op_oid)
    op.last_end = datetime.datetime.now()
    op.last_run_ok = True
    op.last_exception = None
    
    op.save()
    print op


@app.task()
def notify_exception(uuid, op_oid):
    result = AsyncResult(uuid)
    op = Operation.objects.get(oid=op_oid)
    op.last_end = datetime.datetime.now()
    op.last_run_ok = False
    op.last_exception = result.traceback
    op.save()
    