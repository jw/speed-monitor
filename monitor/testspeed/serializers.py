from rest_framework import serializers
from .models import Client, Server, Result
from django_countries.serializers import CountryFieldMixin

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('ip', 'lon', 'lat', 'isp', 'country')


class ServerSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Server
        exclude = ('identifier',)


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('client', 'download', 'upload', 'ping', 'server', 'timestamp', 'bytes_sent', 'bytes_received')
