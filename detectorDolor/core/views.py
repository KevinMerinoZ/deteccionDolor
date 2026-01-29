from django.shortcuts import render

# Create your views here.
def interfazPrincipal(request):
    return render(request, 'core/interfaz_principal.html')