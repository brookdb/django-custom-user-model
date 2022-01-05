from django.http import HttpResponse
from django.shortcuts import render


def landing(request):
    #return HttpResponse("landing")
    return render(request, 'pages/landing.html')
