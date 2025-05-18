from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Make sure this template exists
