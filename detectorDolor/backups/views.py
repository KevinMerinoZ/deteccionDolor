from django.shortcuts import render

# Create your views here.
import os
import subprocess
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required


def backup_database(request):
    db = settings.DATABASES['default']

    fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'backup_{fecha}.sql'
    filepath = os.path.join(settings.BASE_DIR, filename)

    command = (
        f"mysqldump "
        f"-u {db['USER']} "        
        f"{db['NAME']} > \"{filepath}\""
    )

    subprocess.call(command, shell=True)

    with open(filepath, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/sql')
        response['Content-Disposition'] = f'attachment; filename={filename}'

    os.remove(filepath)
    return response
from django.shortcuts import render
from .forms import RestoreDatabaseForm


def restore_database(request):
    mensaje = None

    if request.method == 'POST':
        form = RestoreDatabaseForm(request.POST, request.FILES)
        if form.is_valid():
            sql_file = request.FILES['archivo_sql']

            temp_path = os.path.join(settings.BASE_DIR, 'restore_temp.sql')

            with open(temp_path, 'wb+') as destination:
                for chunk in sql_file.chunks():
                    destination.write(chunk)

            db = settings.DATABASES['default']

            command = (
                f"mysql "
                f"-u {db['USER']} "                
                f"{db['NAME']} < \"{temp_path}\""
            )

            subprocess.call(command, shell=True)
            os.remove(temp_path)

            mensaje = "Base de datos restaurada correctamente"

    else:
        form = RestoreDatabaseForm()

    return render(request, 'backups/restore.html', {
        'form': form,
        'mensaje': mensaje
    })
def backup_panel(request):
    return render(request, 'backups/index.html')

