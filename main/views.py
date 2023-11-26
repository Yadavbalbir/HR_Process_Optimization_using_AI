from django.shortcuts import render


def index(request):
    return render(request, "index.html")

def demo(request):
    return render(request, "demo.html")
