from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from .models import Client, Server, Result


class ClientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Client
        fields = ('id', 'ip', 'lon', 'lat', 'isp', 'country', 'owner')

    def get_id(obj):
        return serializers.get_pk_field()


class ServerSerializer(CountryFieldMixin, serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Server
        fields = '__all__'

    def get_id(obj):
        return serializers.get_pk_field()


class ResultSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Result
        fields = ('owner', 'client', 'download', 'upload', 'ping',
                  'server', 'timestamp', 'bytes_sent', 'bytes_received')

    def get_id(obj):
        return serializers.get_pk_field()
