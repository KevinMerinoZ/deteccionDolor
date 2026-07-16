import datetime

from django.http import JsonResponse
from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from .services.predictor import predecir_imagen
from decimal import Decimal, ROUND_DOWN
from sesionExperimental.models import SesionExperimental, ResultadoMedicion
from PIL import Image
from django.contrib import messages

from django.http import HttpResponse
from collections import defaultdict
import io
import xlsxwriter



# Create your views here.

def index(request, idSesion, accion=None):
    cantidadRatones = 10
    sesionExp = get_object_or_404(SesionExperimental, idsesionExperimental=idSesion)
    resultadosMediciones = ResultadoMedicion.objects.filter(sesion_experimental=sesionExp)

    if resultadosMediciones.filter(estado_medicion=True).order_by('numero_medicion').exists():
        noMedicionAct = (resultadosMediciones.filter(estado_medicion=True).order_by('numero_medicion').last().numero_medicion) 
        
    elif resultadosMediciones.filter(estado_medicion=False).order_by('numero_medicion').exists():
        
        noMedicionAct = (resultadosMediciones.filter(estado_medicion=False).order_by('numero_medicion').last().numero_medicion) + 1 
        if noMedicionAct > sesionExp.noMediciones1:
            noMedicionAct = sesionExp.noMediciones1
    
    else:
        noMedicionAct = 1

    numRatones = range(1, cantidadRatones + 1)
    flagFinMediciones = False

    resultadosMedicionAct = None

    if accion == 'siguiente':
        ratonesAnalizados = resultadosMediciones.filter(numero_medicion=noMedicionAct).count() if resultadosMediciones.filter(numero_medicion=noMedicionAct).exists() else 0
        if ratonesAnalizados < cantidadRatones:
            messages.error(request, f"Faltan {cantidadRatones - ratonesAnalizados} ratones por analizar en la medición actual.", extra_tags="danger")
        else:
            resultadosMediciones.filter(numero_medicion=noMedicionAct).update(estado_medicion=False)
            noMedicionAct += 1

        if resultadosMediciones.count() >= ((sesionExp.noMediciones1*cantidadRatones)-10):
            flagFinMediciones = True
    
    if resultadosMediciones.count() >= ((sesionExp.noMediciones1*cantidadRatones)-10):
            flagFinMediciones = True
    
    resultadosMedicionAct = resultadosMediciones.filter(numero_medicion=noMedicionAct)

    if request.method == 'POST' and request.FILES.get('inputImgRaton'):
        imgRaton = Image.open(request.FILES["inputImgRaton"])
        resultado = predecir_imagen(imgRaton)
        noRaton = request.POST.get('noRaton')
        numero_medicion = request.POST.get('noMedicionActual')

        if(resultado['clase'] == 0):
            nivelDolor = 1
        else:
            nivelDolor = 2

        confianza = Decimal(resultado['confianza']*100).quantize(Decimal('0.000'), rounding=ROUND_DOWN)
        confianza_orejas = Decimal(resultado['confianza_orejas']*100).quantize(Decimal('0.000'), rounding=ROUND_DOWN)
        confianza_ojos = Decimal(resultado['confianza_ojos']*100).quantize(Decimal('0.000'), rounding=ROUND_DOWN)
        confianza_nariz = Decimal(resultado['confianza_nariz']*100).quantize(Decimal('0.000'), rounding=ROUND_DOWN)
        confianza_cachetes = Decimal(resultado['confianza_cachetes']*100).quantize(Decimal('0.000'), rounding=ROUND_DOWN)

        # ************* Proceso de guardado o actualización de resultados de medición *************
        resultadoMedExists = ResultadoMedicion.objects.filter(noRaton = noRaton, numero_medicion = numero_medicion, sesion_experimental = sesionExp).first()

        promedio_nivel = (resultado['clase_orejas'] + resultado['clase_ojos'] + resultado['clase_nariz'] + resultado['clase_cachetes']) / 4
        promedio_confianza = (confianza_orejas + confianza_ojos + confianza_nariz + confianza_cachetes) / 4
        # Si existe un resultado de medición para el ratón y la medición actual, se actualiza; de lo contrario, se crea uno nuevo.
        if resultadoMedExists:
            resultadoMedExists.nivelDolor = nivelDolor
            resultadoMedExists.confianza = confianza
            resultadoMedExists.orejas_nivel = resultado['clase_orejas']
            resultadoMedExists.ojos_nivel = resultado['clase_ojos']
            resultadoMedExists.nariz_nivel = resultado['clase_nariz']
            resultadoMedExists.cachetes_nivel = resultado['clase_cachetes']

            resultadoMedExists.confianza_orejas = confianza_orejas
            resultadoMedExists.confianza_ojos = confianza_ojos
            resultadoMedExists.confianza_nariz = confianza_nariz
            resultadoMedExists.confianza_cachetes = confianza_cachetes

            resultadoMedExists.promedio_nivel = promedio_nivel
            resultadoMedExists.promedio_confianza = promedio_confianza
            resultadoMedExists.save()

        else:
            resultadoMed = ResultadoMedicion(
                noRaton = request.POST.get('noRaton'),
                nivelDolor = nivelDolor,
                confianza = confianza,
                orejas_nivel = resultado['clase_orejas'],
                ojos_nivel = resultado['clase_ojos'],
                nariz_nivel = resultado['clase_nariz'],
                cachetes_nivel = resultado['clase_cachetes'],

                confianza_orejas = confianza_orejas,
                confianza_ojos = confianza_ojos,
                confianza_nariz = confianza_nariz,
                confianza_cachetes = confianza_cachetes,

                numero_medicion = numero_medicion,
                sesion_experimental = sesionExp,

                promedio_nivel = promedio_nivel,
                promedio_confianza = promedio_confianza
            )
            resultadoMed.save()
        
        print("Nivel de dolor predicho:", nivelDolor)
        print("Resultado de clase: ", resultado['clase'])
        print("Confianza:", confianza)

        # Devolver respuesta JSON para mostrarlos en la interfaz de usuario
        return JsonResponse({
            'nivel_dolor': int(resultado['clase']),
            'confianza': float(confianza),
            'nivel_dolor_orejas': int(resultado['clase_orejas']),
            'confianza_orejas': float(confianza_orejas),
            'nivel_dolor_ojos': int(resultado['clase_ojos']),
            'confianza_ojos': float(confianza_ojos),
            'nivel_dolor_nariz': int(resultado['clase_nariz']),
            'confianza_nariz': float(confianza_nariz),
            'nivel_dolor_cachetes': int(resultado['clase_cachetes']),
            'confianza_cachetes': float(confianza_cachetes),
            'promedio_confianza': float(promedio_confianza),
            'promedio_nivel': float(promedio_nivel),
        })
    
    context = {
        'numRatones': numRatones,
        'noMedicionAct': noMedicionAct,
        'noMediciones1': sesionExp.noMediciones1,
        'idSesion': idSesion,
        'resultadosMedicionAct': resultadosMedicionAct,
        'flagFinMediciones': flagFinMediciones
    }
    
    return render(request, 'detectorDolor/index.html', context)


def reporte_resultados_dolor(request, idSesion):
    if not idSesion:
        return HttpResponse("Debe proporcionar una sesión experimental")

    try:
        sesion = SesionExperimental.objects.get(
            idsesionExperimental=idSesion
        )
    except SesionExperimental.DoesNotExist:
        return HttpResponse("Sesión no encontrada")

    resultados = ResultadoMedicion.objects.filter(
        sesion_experimental=sesion,
        is_active=True
    ).order_by('numero_medicion')

    # Agrupar resultados
    datos = defaultdict(lambda: {
        'sin_dolor': 0,
        'dolor_leve': 0,
        'dolor_intenso': 0
    })

    for resultado in resultados:

        medicion = resultado.numero_medicion

        if resultado.nivelDolor == ResultadoMedicion.NIVEL_DOLOR_1:
            datos[medicion]['sin_dolor'] += 1

        elif resultado.nivelDolor == ResultadoMedicion.NIVEL_DOLOR_2:
            datos[medicion]['dolor_leve'] += 1

        elif resultado.nivelDolor == ResultadoMedicion.NIVEL_DOLOR_3:
            datos[medicion]['dolor_intenso'] += 1

    # Crear Excel
    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet("Reporte")

    # FORMATOS
    titulo = workbook.add_format({
        'bold': True,
        'font_size': 16,
        'align': 'center',
        'valign': 'vcenter'
    })

    encabezado = workbook.add_format({
        'bold': True,
        'border': 1,
        'align': 'center',
        'bg_color': '#D9EAD3'
    })

    celda = workbook.add_format({
        'border': 1,
        'align': 'center'
    })

    # Ajustar columnas
    worksheet.set_column('A:A', 25)
    worksheet.set_column('B:D', 18)

    # Título
    worksheet.merge_range(
        'A1:D1',
        'Reporte de Resultados de Detección de Dolor',
        titulo
    )

    # Información sesión
    worksheet.write('A3', 'Sesión Experimental:', encabezado)
    worksheet.write('B3', sesion.nombre_experimento, celda)

    worksheet.write('A4', 'Fecha:', encabezado)
    worksheet.write('B4', str(sesion.fecha), celda)

    # Encabezados
    worksheet.write('A6', 'Número de medición', encabezado)
    worksheet.write('B6', 'Sin dolor', encabezado)
    worksheet.write('C6', 'Dolor leve', encabezado)
    worksheet.write('D6', 'Dolor intenso', encabezado)

    # Llenar datos
    row = 6

    for numero_medicion, valores in datos.items():

        worksheet.write(row, 0, f"Medición {numero_medicion}", celda)

        worksheet.write(row, 1, valores['sin_dolor'], celda)
        worksheet.write(row, 2, valores['dolor_leve'], celda)
        worksheet.write(row, 3, valores['dolor_intenso'], celda)

        row += 1

    # Crear gráfica
    chart = workbook.add_chart({'type': 'column'})

    chart.add_series({
        'name': '=Reporte!$B$6',
        'categories': f'=Reporte!$A$7:$A${row}',
        'values': f'=Reporte!$B$7:$B${row}',
    })

    chart.add_series({
        'name': '=Reporte!$C$6',
        'categories': f'=Reporte!$A$7:$A${row}',
        'values': f'=Reporte!$C$7:$C${row}',
    })

    chart.add_series({
        'name': '=Reporte!$D$6',
        'categories': f'=Reporte!$A$7:$A${row}',
        'values': f'=Reporte!$D$7:$D${row}',
    })

    chart.set_title({
        'name': 'Resultados por Nivel de Dolor'
    })

    chart.set_x_axis({
        'name': 'Número de medición'
    })

    chart.set_y_axis({
        'name': 'Cantidad de ratones'
    })

    worksheet.insert_chart('F6', chart)

    workbook.close()

    output.seek(0)

    # Descargar automáticamente
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    nombreArchivo = f"reporte_resultados_dolor_sesion_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    
    response['Content-Disposition'] = (
        f'attachment; filename="{nombreArchivo}"'
    )

    sesion.estado = False
    sesion.save()    

    return response