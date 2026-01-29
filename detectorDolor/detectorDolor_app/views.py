from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .services.predictor import predecir_imagen
from decimal import Decimal, ROUND_DOWN
from sesionExperimental.models import SesionExperimental, ResultadoMedicion
from PIL import Image


# Create your views here.

def index(request, idSesion):
    sesionExp = get_object_or_404(SesionExperimental, idsesionExperimental=idSesion)
    resultadosMediciones = ResultadoMedicion.objects.filter(sesion_experimental=sesionExp)
    noMedicionAct = (resultadosMediciones.order_by('numero_medicion').last().numero_medicion) if resultadosMediciones.order_by('numero_medicion').exists() else 1
    numRatones = range(1,11)
    mensaje = ""

    if request.GET.get('siguiente'):
        if resultadosMediciones.filter(numero_medicion=noMedicionAct).count() < 10:
            mensaje = "No. de medición {} no se ha completado.".format(noMedicionAct)
        else:
            noMedicionAct += 1

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
    
    return render(request, 'detectorDolor/index.html', {'numRatones': numRatones, 'noMedicionAct': noMedicionAct, 'idSesion': idSesion, 'mensaje': mensaje})