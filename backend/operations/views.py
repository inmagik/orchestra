from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.exceptions import APIException

from orchestra_core import op_register as register
from orchestra_core import wf_register

from operations.utils import run_operation, run_workflow, get_workflow_meta, create_workflow

from .serializers import OperationSerializer, WorkflowSerializer
from .models import Operation, Workflow
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
        assigned_id = request.DATA.get('assigned_id')
        partials = request.DATA.get('partials')

        if not name:
            raise APIException("No name provided. You must provide an operation name")

        if name not in register.meta:
            raise APIException("The operation %s is unknown" % name)            

        op = Operation(name=name, owner=request.user, assigned_id=assigned_id, partials=partials)
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
        
        run_operation(op, request.DATA)
        
        return Response(OperationSerializer(op).data)


class OperationStatus(APIView):

    def get(self, request, pk, format=None):
        try:
            op = Operation.objects.get(pk=pk)
        except:
            raise APIException("Operation not found")

        return  Response(OperationSerializer(op).data)





class ListWorkflows(APIView):
    """
    Lists all available wf
    """
    #authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        """
        Return a list of all registered operations.
        """
        wfs = wf_register.reg.keys()
        out = []
        for w in wfs:
            out.append(get_workflow_meta(w))
        return Response(out)



class RunWorkflow (APIView):
    
    def post(self, request, format=None):
        
        id = request.DATA.get('id')
        data = request.DATA.get('data', {})
        rerun = request.DATA.get('rerun', [])
        
        try:
            wf = Workflow.objects.get(pk=int(id))
        except Exception, e:
            raise APIException("No valid WorkFlow found")

        
        run_ops = run_workflow(wf.assigned_id, data, rerun=rerun)
        
        return Response(run_ops)


class CreateWorkflow(APIView):
    
    def post(self, request, format=None):
        
        name = request.DATA.get('name')
        assigned_id = request.DATA.get('assigned_id')
        
        if not name:
            raise APIException("No name provided. You must provide a workflow name")

        if name not in wf_register.reg:
            raise APIException("The workflow %s is unknown" % name)            

        wf = create_workflow(name=name, owner=request.user)
        
        return Response(WorkflowSerializer(wf).data)


class WorkflowStatus(APIView):

    def get(self, request, pk, format=None):
        try:
            op = Workflow.objects.get(pk=pk)
        except Workflow.DoesNotExist:
            raise APIException("Workflow not found")

        return  Response(WorkflowSerializer(op).data)
