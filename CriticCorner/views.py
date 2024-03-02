from django.shortcuts import render

def about(request):
    return render(request, 'CriticCorner/about.html')
