# from django.shortcuts import redirect
# from django.urls import resolve

# class RestringirAppMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.app_restringida = 'usuario'

#     def __call__(self, request):
#         app_actual = resolve(request.path).app_name

#         if app_actual == self.app_restringida:
#             if not request.user.is_authenticated:
#                 return redirect('login')

#             if not request.user.groups.filter(name='administrador').exists():
#                 return redirect('login')

#         return self.get_response(request)
