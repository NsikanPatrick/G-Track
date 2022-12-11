from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    # return HttpResponse('Halo')
    return render(request, 'index.html', {})

def admins(request):
    return render(request, 'admins.html', {})
