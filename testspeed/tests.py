from datetime import datetime

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase

from testspeed.models import Client, Server, Result


class ModelTestCase(TestCase):
    """This class defines the test suite for the model."""

    def setUp(self):
        """Define the test client, a test server and a test result."""
        self.user = User.objects.create(username="nerd")

        self.client = Client(ip='127.0.0.1', lon=3.200000, lat=50.916700,
                             isp='Skynet Belgium', country='BE',
                             owner=self.user)
        self.other_client = Client(ip='127.0.0.1', lon=6.200000, lat=54.916700,
                                   isp='Skynet Belgium', country='NL',
                                   owner=self.user)

        url = 'http://speedtest.valentin-deville.eu/speedtest/upload.php'
        host = 'speedtest.valentin-deville.eu:8080'
        self.server = Server(identifier=11458,
                             url=url,
                             lon=3.170000,
                             lat=50.700000,
                             name='Roubaix',
                             country='FR',
                             sponsor='MyTheValentinus',
                             host=host,
                             d=24.1879699540931,
                             latency=79.381,
                             owner=self.user)
        self.other_server = Server(identifier=11422,
                                   url=url,
                                   lon=4.170000,
                                   lat=53.700000,
                                   name='Paris',
                                   country='FR',
                                   sponsor='L\'Ille de France',
                                   host=host,
                                   d=43.1879699540931,
                                   latency=100.381,
                                   owner=self.user)

        self.result = Result(client=self.client,
                             download=10458751.0878227,
                             upload=8537310.7933532,
                             ping=79.381,
                             server=self.server,
                             timestamp=datetime.now(),
                             bytes_sent=10985472,
                             bytes_received=13247432)

    def test_model_can_create_a_client(self):
        """Test the client model can create a client."""
        old_count = Client.objects.count()
        self.client.save()
        new_count = Client.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_cannot_create_a_client_with_same_ip_and_isp(self):
        """
        Test the ip and isp uniqueness.
        """
        self.assertRaises(IntegrityError, self.other_client.save())

    def test_model_returns_readable_client(self):
        """Test a readable string is returned for the model instance."""
        self.assertEqual(str(self.client),
                         '{0} ({1}) from {2}.'.format(
                             self.client.isp,
                             self.client.ip,
                             self.client.country.name))

    def test_model_can_create_a_server(self):
        """Test the server model can create a server."""
        old_count = Server.objects.count()
        self.server.save()
        new_count = Server.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_cannot_create_a_server_with_same_host(self):
        """
        Test the host uniqueness.
        """
        self.assertRaises(IntegrityError, self.other_server.save())
