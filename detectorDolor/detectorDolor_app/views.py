from django.http import JsonResponse
from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from .services.predictor import predecir_imagen
from decimal import Decimal, ROUND_DOWN
from sesionExperimental.models import SesionExperimental, ResultadoMedicion
from PIL import Image
from django.contrib import messages



# Create your views here.

def index(request, idSesion, accion=None):
    cantidadRatones = 10
    sesionExp = get_object_or_404(SesionExperimental, idsesionExperimental=idSesion)
    resultadosMediciones = ResultadoMedicion.objects.filter(sesion_experimental=sesionExp)
    noMedicionAct = (resultadosMediciones.order_by('numero_medicion').last().numero_medicion) if resultadosMediciones.order_by('numero_medicion').exists() else 1
    numRatones = range(1, cantidadRatones + 1)
    flagFinMediciones = False

    resultadosMedicionAct = resultadosMediciones.filter(numero_medicion=noMedicionAct)

    if accion == 'siguiente':
        ratonesAnalizados = resultadosMediciones.filter(numero_medicion=noMedicionAct).count()
        if ratonesAnalizados < cantidadRatones:
            messages.error(request, f"Faltan {cantidadRatones - ratonesAnalizados} ratones por analizar en la medición actual.", extra_tags="danger")
        else:
            noMedicionAct += 1

        if resultadosMediciones.count() >= ((sesionExp.noMediciones1*cantidadRatones)-10):
            flagFinMediciones = True

    if request.method == 'POST' and request.FILES.get('inputImgRaton'):
        imgRaton = Image.open(request.FILES["inputImgRaton"])
        resultado = predecir_imagen(imgRaton)
        noRaton = request.POST.get('noRaton')
        numero_medicion = request.POST.get('noMedicionActual')

        if(resultado['clase'] == '0 Sanas'):
            nivelDolor = 1
        else:
            nivelDolor = 2

        confianza = Decimal(resultado['confianza']*100).quantize(Decimal('0.000'), rounding=ROUND_DOWN)

        resultadoMedExists = ResultadoMedicion.objects.filter(noRaton = noRaton, numero_medicion = numero_medicion, sesion_experimental = sesionExp).first()

        if resultadoMedExists:
            resultadoMedExists.nivelDolor = nivelDolor
            resultadoMedExists.confianza = confianza
            resultadoMedExists.save()

        else:
            resultadoMed = ResultadoMedicion(
                noRaton = request.POST.get('noRaton'),
                nivelDolor = nivelDolor,
                confianza = confianza,
                numero_medicion = numero_medicion,
                sesion_experimental = sesionExp
            )
            resultadoMed.save()

        return JsonResponse({
            'nivel_dolor': resultado['clase'],
            'confianza': confianza
        })
    
    context = {
        'numRatones': numRatones,
        'noMedicionAct': noMedicionAct,
        'idSesion': idSesion,
        'resultadosMedicionAct': resultadosMedicionAct,
        'flagFinMediciones': flagFinMediciones
    }
    
    return render(request, 'detectorDolor/index.html', context)