from django.shortcuts import redirect
from django.urls import resolve, Resolver404

class RestringirAppMiddleware:
    """
    Middleware para restringir el acceso a ciertas aplicaciones
    solo a usuarios autenticados y con roles específicos.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        #Puedes agregar más apps o más roles en estas listas
        self.apps_restringidas = {
            'usuario': ['administrador'],       # solo admin
            'lotesAnimales': ['administrador', 'tecnicoAcademico'],  
            'provedor': ['administrador','tecnicoAcademico'],  
            'material': ['administrador','tecnicoAcademico'],
            'farmaco': ['administrador','tecnicoAcademico','estudianteLicenciatura'],
            'sustanciaExperimental': ['administrador','tecnicoAcademico','estudianteLicenciatura'],
            'protocoloExperimental': ['administrador'],
            'cita': ['administrador','tecnicoAcademico','estudianteLicenciatura'],
            'gestionIncidencias': ['administrador','tecnicoAcademico','estudianteLicenciatura'],
            'core':['administrador','tecnicoAcademico','estudianteLicenciatura'],
        }

    def __call__(self, request):

        try:
            app_actual = resolve(request.path).app_name
        except Resolver404:
            return self.get_response(request)

        # Si la app no está restringida → dejar pasar
        if app_actual not in self.apps_restringidas:
            return self.get_response(request)

        # Si requiere autenticación y el usuario no ha iniciado sesión
        if not request.user.is_authenticated:
            return redirect('inicioSesion:login')

        # Roles permitidos para esta app
        roles_permitidos = self.apps_restringidas[app_actual]

        # Validar roles del usuario
        if not request.user.groups.filter(name__in=roles_permitidos).exists():
            return redirect('inicioSesion:login')

        return self.get_response(request)

