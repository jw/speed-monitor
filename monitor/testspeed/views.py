from rest_framework.viewsets import ModelViewSet
from testspeed.models import Result, Client, Server
from testspeed.serializers import ResultSerializer, ClientSerializer, ServerSerializer


class ClientViewSet(ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class ServerViewSet(ModelViewSet):
    serializer_class = ServerSerializer
    queryset = Server.objects.all()


class ResultViewSet(ModelViewSet):
    serializer_class = ResultSerializer
    queryset = Result.objects.all()
