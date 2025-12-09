from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
# from django.http import HttpResponse

# Create your views here.
def login_vista(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
        else:
            login(request, user)
            return redirect('usuario:indexUsuario')
        
    return render(request, 'login.html')

