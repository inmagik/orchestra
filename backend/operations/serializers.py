from orchestra_core import op_register as register
from orchestra_core.utils import get_async_result, get_async_state

from rest_framework import serializers
from .models import Operation, Workflow


class OperationSerializer(serializers.ModelSerializer):
    task_result = serializers.SerializerMethodField('get_task_result')
    task_state = serializers.SerializerMethodField('get_task_state')
    meta = serializers.SerializerMethodField('get_op_meta')
    args_missing = serializers.Field(source='args_missing')

    def get_task_result(self, obj):
        if not obj.task:
            return None
        try:
            return get_async_result(obj.task)
        except:
            return None

    def get_task_state(self, obj):
        if not obj.task:
            return None
        try:
            return get_async_state(obj.task)
        except:
            return None

    def get_op_meta(self, obj):

        return register.meta[obj.name]

    class Meta:
        model = Operation
        fields = ('id', 'name', 'task', 'owner', 'task_result', 'task_state', 'args', 'meta', 'partials', 'oid',
                  'last_run', 'last_run_ok', 'last_exception', 'args_missing')


class WorkflowSerializer(serializers.ModelSerializer):
    operations = OperationSerializer(many=True)
    pending_operations = serializers.SerializerMethodField('get_pending_operations')

    def get_pending_operations(self, obj):
        ops = obj.operations.all()
        return [x.oid for x in ops if not x.task]

    class Meta:
        model = Workflow
