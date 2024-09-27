from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        "text": "Real-Time Graph"
    }
    return render(request, 'index.html', context=context)