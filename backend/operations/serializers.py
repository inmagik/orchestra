from rest_framework import serializers
from .models import Operation
from core import register

class OperationSerializer(serializers.ModelSerializer):

    task_result = serializers.SerializerMethodField('get_task_result')
    task_state = serializers.SerializerMethodField('get_task_state')

    def get_task_result(self, obj):
        if not obj.task:
            return None
        task_cls = register.reg[obj.name]

        as_res =  task_cls.AsyncResult(obj.task)
        return as_res.get()

    def get_task_state(self, obj):
        if not obj.task:
            return None
        task_cls = register.reg[obj.name]

        as_res =  task_cls.AsyncResult(obj.task)
        return as_res.state
        
    class Meta:
        model = Operation
        fields = ('id', 'name', 'task', 'owner', 'task_result', 'task_state', 'args')