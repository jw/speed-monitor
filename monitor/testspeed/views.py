from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from testspeed.models import Result, Client, Server
from testspeed.serializers import ResultSerializer, ClientSerializer, ServerSerializer


@csrf_exempt
def client(request):
    if request.method == 'GET':
        result = Client.objects.all()
        serializer = ClientSerializer(result, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ClientSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            return JsonResponse({'pk': instance.pk}, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def server(request):
    if request.method == 'GET':
        result = Server.objects.all()
        serializer = ServerSerializer(result, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ServerSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            return JsonResponse({'pk': instance.pk}, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def results_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        result = Result.objects.all()
        serializer = ResultSerializer(result, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ResultSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
