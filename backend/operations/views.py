from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.exceptions import APIException

from core import register
from .serializers import OperationSerializer
from .models import Operation
import json

class ListOperations(APIView):
    """
    Lists all available ops
    """
    #authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        """
        Return a list of all registered operations.
        """
        operations = register.meta
        return Response(operations)


class CreateOperation(APIView):
    
    def post(self, request, format=None):
        
        name = request.DATA.get('name')
        if not name:
            raise APIException("No name provided. You must provide an operation name")

        if name not in register.meta:
            raise APIException("The operation %s is unknown" % name)            

        op = Operation(name=name, owner=request.user)
        op.save()
        
        return Response(OperationSerializer(op).data)


class RunOperation(APIView):
    
    def post(self, request, format=None):
        
        id = request.DATA.get('id')
        force = request.DATA.get('force', False)
        
        try:
            op = Operation.objects.get(pk=int(id))
        except Exception, e:
            raise APIException("No valid operation found")

        if op.task and not force:
            raise APIException("This operation has already run")
        
        #let's check arguments
        meta = register.meta[op.name]
        args = []
        args_not_found = []
        for arg in meta['args']:
            if arg not in request.DATA:
                args_not_found.append(arg)
            else:
                args.append(request.DATA[arg])

        if args_not_found:
            raise APIException("Missing arguments, %s" % ','.join(args_not_found))    

        task = register.reg[op.name]
        run_args = {'args' : args}
        res = task.apply_async(args)
        task_id = res.task_id
        op.task = task_id
        op.args = json.dumps(run_args)
        op.save()
        
        return Response(OperationSerializer(op).data)


class OperationStatus(APIView):

    def get(self, request, pk, format=None):
        try:
            op = Operation.objects.get(pk=pk)
        except:
            raise APIException("Operation not found")

        return  Response(OperationSerializer(op).data)
