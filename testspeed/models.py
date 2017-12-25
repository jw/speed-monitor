from django.db import models
from django_countries.fields import CountryField


class Client(models.Model):
    ip = models.GenericIPAddressField()
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    isp = models.CharField(max_length=300)
    country = CountryField()

    def __str__(self):
        return '{0} ({1}) from {2}.'.format(self.isp, self.ip, self.country.name)


class Server(models.Model):
    id = models.IntegerField()
    url = models.CharField(max_length=500)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    name = models.CharField(max_length=500)
    country = CountryField()
    sponsor = models.CharField(max_length=500)
    host = models.CharField(max_length=500)
    distance = models.FloatField()
    latency = models.FloatField()


class Result(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    download = models.FloatField()
    upload = models.FloatField()
    ping = models.FloatField()
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    bytes_sent = models.IntegerField()
    bytes_received = models.IntegerField()


class Results(models.Model):
    results = models.ManyToManyField(Result)


class IgnoreServers(models.Model):
    servers = models.ManyToManyField(Server)
