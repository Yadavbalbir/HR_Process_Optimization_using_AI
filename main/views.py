from django.shortcuts import render


def index(request):
    return render(request, "index.html")

def jdeval(request):
    return render(request, "jobdesc.html")


def cvranker(request):
    return render(request, "cvranker.html")
