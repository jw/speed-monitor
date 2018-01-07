from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from .models import Result, Client, Server
from .serializers import ResultSerializer, ClientSerializer, ServerSerializer


class ClientViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('ip', 'isp')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ServerViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ServerSerializer
    queryset = Server.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('host',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ResultViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ResultSerializer
    queryset = Result.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
