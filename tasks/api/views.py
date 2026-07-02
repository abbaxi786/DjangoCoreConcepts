from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def Home(request):
    return JsonResponse({
        "message": "Welcome to the API Home Page"
    })