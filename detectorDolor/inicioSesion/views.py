from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
# from django.http import HttpResponse

# Create your views here.
def login(request):
    if request.method == 'POST':
        return render(request, 'login.html')
    else:
        print("Hola")

