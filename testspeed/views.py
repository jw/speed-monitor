from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from .models import Result, Client, Server
from .serializers import ResultSerializer, ClientSerializer, ServerSerializer


class ClientViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('ip', 'isp')


class ServerViewSet(ModelViewSet):
    serializer_class = ServerSerializer
    queryset = Server.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('url',)


class ResultViewSet(ModelViewSet):
    serializer_class = ResultSerializer
    queryset = Result.objects.all()
