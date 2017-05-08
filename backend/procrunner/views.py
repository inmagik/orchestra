from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import UserSerializer, GroupSerializer
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CurrentUserView(APIView):
    """
    Get my personal account
    """
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
