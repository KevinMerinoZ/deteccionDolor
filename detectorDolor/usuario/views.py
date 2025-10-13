from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def inicio(request):
    return HttpResponse("<h1>Hola Mundo</h1>")

def pgPrincipal(request):
    return render(request, 'paginas/principal.html')

def pgUsuariosIndex(request):
    return render(request, 'usuarios/index.html')
def pgUsuariosCrear(request):
    return render(request, 'usuarios/crear.html')
def pgUsuariosEditar(request):
    return render(request, 'usuarios/editar.html')