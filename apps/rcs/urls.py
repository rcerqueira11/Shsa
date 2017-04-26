from django.conf.urls import include, url
import views
from django.views.generic import TemplateView


urlpatterns = [

    url(
        r'^planilla_seguro_carro',
        views.VerPlanillaSeguroCarro.as_view(),
        name="planilla_seguro_carro"
    ),
    url(
        r'^dashboard',
        views.Dashboard.as_view(),
        name="dashboard"
    ),

    url(
        r'^gestion_ticket',
        views.GestionSolicitudAbierta.as_view(),
        name="gestion_ticket"
    ),
    url(
        r'^condiciones_vehiculo',
        views.CondicionVehiculoSolicitud.as_view(),
        name="condiciones_vehiculo"
    ),
    url(
        r'^mecanica_vehiculo',
        views.MecanicaVehiculoSolicitud.as_view(),
        name="mecanica_vehiculo"
    ),
    url(
        r'^accesorios_vehiculo',
        views.AccesoriosVehiculoSolicitud.as_view(),
        name="accesorios_vehiculo"
    ),
    url(
        r'^detalles_vehiculo',
        views.DetallesVehiculoSolicitud.as_view(),
        name="detalles_vehiculo"
    ),
    url(
        r'^documentos_vehiculo',
        views.DocumentosVehiculoSolicitud.as_view(),
        name="documentos_vehiculo"
    ),
    url(
        r'^crear_solicitud',
        views.SolicitudInspeccion.as_view(),
        name="crear_solicitud"
    ),
    
]