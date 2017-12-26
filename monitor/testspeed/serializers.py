from rest_framework import serializers
from .models import Client, Result


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('ip', 'lon', 'lat', 'isp', 'country')


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('client', 'download', 'upload', 'ping', 'server', 'timestamp', 'bytes_sent', 'bytes_received')
