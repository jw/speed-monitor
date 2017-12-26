from django.urls import path
from . import views

urlpatterns = [
    path('client', views.client, name='client'),
    path('result', views.results_list, name='results'),
    path('result', views.results_list, name='results'),
    path('result', views.results_list, name='results'),
]
