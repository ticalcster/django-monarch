import json
from django.shortcuts import render
from django.http import JsonResponse


def json_auth_view(request):
    return render(request, 'testfile.json', {}, content_type='application/json')


def json_view(request):
    if request.method == 'GET':
        return JsonResponse(request.GET, content_type='application/json')
    else:
        return JsonResponse(request.POST, content_type='application/json')

