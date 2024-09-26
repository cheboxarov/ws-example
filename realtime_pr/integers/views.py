from django.shortcuts import render


def index(request):
    context = {
        "text": "text"
    }
    return render(request, 'index.html', context=context)
