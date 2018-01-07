from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('testspeed.urls')),
    path('chart/', include('chart.urls')),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]
