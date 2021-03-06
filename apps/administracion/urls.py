from django.conf.urls import include, url
import views
from django.views.generic import TemplateView


urlpatterns = [

    url(
        r'^editar_titular/(?P<titular_id>.+)?$',
        views.EditarTitular.as_view(),
        name="editar_titular"
    ),
    url(
        r'^editar_trajo_vehiculo/(?P<trajo_vehi_id>.+)?$',
        views.EditarTrajoVehiculo.as_view(),
        name="editar_trajo_vehiculo"
    ),
    url(
        r'^inactivar_usuario/(?P<usuario_id>.+)?$',
        views.InactivarUsuario.as_view(),
        name="inactivar_usuario"
    ),
    url(
        r'^editar_usuario/(?P<usuario_id>.+)?$',
        views.EditarUsuario.as_view(),
        name="editar_usuario"
    ),
    url(
        r'^eliminar_usuario/(?P<usuario_id>.+)?$',
        views.EliminarUsuario.as_view(),
        name="eliminar_usuario"
    ),
    url(
        r'^bandeja_titulares',
        views.BandejaTitulares.as_view(),
        name="bandeja_titulares"
    ),
    url(
        r'^bandeja_trajo_vehiculo',
        views.BandejaTrajoVehiculo.as_view(),
        name="bandeja_trajo_vehiculo"
    ),
    url(
        r'^bandeja_usuarios',
        views.BandejaUsuarios.as_view(),
        name="bandeja_usuarios"
    ),
]