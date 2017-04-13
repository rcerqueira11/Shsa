from django.conf.urls import include, url
from apps.registro import views
from django.views.generic import TemplateView

urlpatterns = [

    url(
        r'^login',
        views.Login.as_view(),
        name="registro_login"
    ),
    
    url(
        r'^logout',
        views.Logout.as_view(),
        name="logout"
    ),
    url(
        r'^registro',
        views.RegistroUsuario.as_view(),
        name="registro_usuario"
    ),
    url(
        r'^restaurar_cuenta',
        views.RestaurarCuenta.as_view(),
        name="restaurar_cuenta"
    ),
    
    url(
        r'^verificar_nombre_usuario$',
        views.consulta_nombre_usuario,
        name="verificar_nombre_usuario"
    ),
    url(
        r'^verificar_correo_usuario$',
        views.consulta_correo_usuario,
        name="verificar_correo_usuario"
    ),
    url(
        r'^verificar_cedula_usuario$',
        views.consulta_cedula_usuario,
        name="verificar_cedula_usuario"
    ),

    
]