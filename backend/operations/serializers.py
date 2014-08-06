from rest_framework import serializers
from .models import Operation
from orchestra_core import op_register as register
from orchestra_core.utils import get_async_result, get_async_state

class OperationSerializer(serializers.ModelSerializer):

    task_result = serializers.SerializerMethodField('get_task_result')
    task_state = serializers.SerializerMethodField('get_task_state')

    def get_task_result(self, obj):
        if not obj.task:
            return None
        return get_async_result(obj.task)
        
    def get_task_state(self, obj):
        if not obj.task:
            return None

        return get_async_state(obj.task)

    class Meta:
        model = Operation
        fields = ('id', 'name', 'task', 'owner', 'task_result', 'task_state', 'args', 'partials')