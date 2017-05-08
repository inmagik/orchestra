import datetime
import json

from backend.celery import app
from orchestra_core import op_register
from orchestra_core.utils import generate_uuid, resolve_partial, reset_async_result

from celery.result import AsyncResult
from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField
from .managers import WorkflowManager


class Workflow(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=200)
    oid = models.CharField(max_length=200, null=True, blank=True, default=generate_uuid)

    objects = WorkflowManager()

    def reset(self):
        for op in self.operations.all():
            op.reset()

    # TODO: not used
    def get_meta(self):
        out = {}
        out['name'] = self.name
        out['ops'] = []

        for op in self.operations:
            oid = op.oid
            partials = op.partials or {}
            out_partials = {}
            for k in partials:
                p = partials[k]
                if type(p) == dict and 'backend' in p:
                    out_partials[k] = {"source": p['id']}
                else:
                    out_partials[k] = partials[k]

            meta = op_register.meta[op.name]
            op_data = {"name": op.name, "oid": oid, "meta": meta, "partials": out_partials}
            out['ops'].append(op_data)

        return out

    def get_runnable_ops(self, data={}, rerun=[]):
        out = []
        missing = {}
        for op in self.operations.all():
            # filtering run operations

            if op.task and op.oid not in rerun:
                continue

            if op.oid in data:
                op_data = data[op.oid]
            else:
                op_data = {}

            op_args = op.get_args()
            op_args.update(op_data)
            x = op.check_missing_args(op_args)

            if not x:
                out.append(op)
            else:
                missing[op.oid] = x

        return out, missing

    def run(self, data={}, rerun=[]):

        ops = self.operations.all()
        rops, missing = self.get_runnable_ops(data=data, rerun=rerun)

        xops = [x.oid for x in ops if x.task and x.oid not in rerun]

        run_ops = []
        if rops:
            for r in rops:
                op_data = data.get(r.oid, {})
                r.run(op_data)
                run_ops.append(r.oid)

        return {"just_run": run_ops, "missing_args": missing, "previously_run": xops}


class Operation(models.Model):
    """
    A model to represent a single Operation
    """
    owner = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=200)

    # current task
    task = models.CharField(max_length=200, null=True, blank=True)
    args = JSONField(null=True, blank=True)

    partials = JSONField(null=True, blank=True)
    oid = models.CharField(max_length=200, null=True, blank=True, default=generate_uuid)

    workflow = models.ForeignKey(Workflow, null=True, blank=True, related_name="operations")

    # execution data
    last_run = models.DateTimeField(null=True, blank=True)
    last_end = models.DateTimeField(null=True, blank=True)

    last_run_ok = models.NullBooleanField(null=True, blank=True)
    last_exception = models.TextField(null=True, blank=True)

    def connect_op(self, op, argname):
        self.partials = self.partials or {}
        self.partials[argname] = {
            "source": op.oid,
            "backend": 'celery'
        }

    def connect_value(self, value, argname):
        self.partials = self.partials or {}
        self.partials[argname] = value

    def get_meta(self):
        return op_register.get_meta(self.name)

    def get_task(self):
        return op_register.get_task(self.name)

    def get_partial(self, name):
        try:
            partial = self.partials[name]
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

    @property
    def args_missing(self):
        args = self.get_args()
        args_missing = self.check_missing_args(args)
        return args_missing

    def run(self, run_args={}):

        args = self.get_args()
        args.update(run_args)

        args_missing = self.check_missing_args(args)
        if len(args_missing):
            raise

        task = self.get_task()

        if (self.task):
            # revoke_if_running(op.task)
            reset_async_result(op.task)

        run_args = self.prepare_args(args)

        res = task.apply_async(run_args, task_id=self.oid,
                               link=notify_success.s(self.oid),
                               link_error=notify_exception.s(self.oid))

        self.task = res.task_id
        self.last_run = datetime.datetime.now()

        self.args = json.dumps(run_args)
        self.save()

    def reset(self):
        if self.task:
            res = AsyncResult(self.task)
            if res.state != 'PENDING':
                res.forget()
                self.task = None

        self.save()


# NOTIFICATION TASKS FOR CELERY


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
