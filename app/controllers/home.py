from django.shortcuts import render

# Create your views here.


def example(request):
    return render(request, 'example.html')

def index(request):
    return render(request, 'home/index.html')
