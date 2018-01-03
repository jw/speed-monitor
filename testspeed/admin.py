from django.contrib import admin

from .models import Client, Server, Result

admin.site.register(Client)
admin.site.register(Server)
admin.site.register(Result)
