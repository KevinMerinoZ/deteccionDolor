def grupos_usuario(request):
    if request.user.is_authenticated:
        return{
            'es_administrador': request.user.groups.filter(name='administrador').exists()
        }
    return {}