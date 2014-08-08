from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.exceptions import APIException

from orchestra_core import op_register as register
from orchestra_core import wf_register

from operations.utils import get_workflow_meta, create_registered_workflow

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
        oid = request.DATA.get('oid')
        partials = request.DATA.get('partials')

        if not name:
            raise APIException("No name provided. You must provide an operation name")

        if name not in register.meta:
            raise APIException("The operation %s is unknown" % name)            

        op = Operation(name=name, owner=request.user, oid=oid, partials=partials)
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
        
        op.run(request.DATA)
        
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
    
    def post(self, request, pk=None, format=None):
        
        if not pk:
            id = request.DATA.get('id')
        else:
            id = pk

        try:
            req_data = request.DATA
        except:
            req_data = {}
        data = req_data.get('data', {})
        rerun = req_data.get('rerun', [])
        
        try:
            wf = Workflow.objects.get(pk=int(id))
        except Exception, e:
            raise APIException("No valid WorkFlow found")

        
        run_ops = wf.run(data, rerun=rerun)
        
        return Response(run_ops)


class ResetWorkflow (APIView):
    
    def post(self, request, pk=None, format=None):
        
        if not pk:
            id = request.DATA.get('id')
        else:
            id = pk
        
        try:
            wf = Workflow.objects.get(pk=int(id))
        except Exception, e:
            raise APIException("No valid WorkFlow found")

        wf.reset()
        
        return Response(WorkflowSerializer(wf).data)


class CreateWorkflow(APIView):
    
    def post(self, request, format=None):
        
        name = request.DATA.get('name')
        oid = request.DATA.get('oid')
        
        if not name:
            raise APIException("No name provided. You must provide a workflow name")

        if name not in wf_register.reg:
            raise APIException("The workflow %s is unknown" % name)            

        wf = create_registered_workflow(name=name, owner=request.user)
        
        return Response(WorkflowSerializer(wf).data)


class WorkflowStatus(APIView):

    def get(self, request, pk, format=None):
        try:
            op = Workflow.objects.get(pk=pk)
        except Workflow.DoesNotExist:
            raise APIException("Workflow not found")

        return  Response(WorkflowSerializer(op).data)




from rest_framework import viewsets


class WorkflowViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    permission_classes = (permissions.AllowAny,)


class OperationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    permission_classes = (permissions.AllowAny,)


