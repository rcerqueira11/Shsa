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
        r'^gestion_ticket/(?P<sol_id>.+)?$',
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
        views.SolicitarInspeccion.as_view(),
        name="crear_solicitud"
    ),

    url(
        r'^bandeja_solicitudes',
        views.BandejaSolicitudes.as_view(),
        name="bandeja_solicitudes"
    ),
    url(
        r'^filtro_busqueda_solicitudes',
        views.FiltroBusqueda.as_view(),
        name="filtro_busqueda_solicitudes"
    ),
    
    url(
        r'^verficiar_codigo_detalle_existe/',
        views.verificar_codigo_detalle,
        name="verficiar_codigo_detalle_existe"
    ),
    url(
        r'^verificar_cedula_titular_existe/',
        views.verificar_titular_cedula,
        name="verificar_cedula_titular_existe"
    ),
    url(
        r'^verificar_placa_carro_existe/',
        views.verificar_placa_carro,
        name="verificar_placa_carro_existe"
    ),
    url(
        r'^verificar_cedula_trajo_existe/',
        views.verificar_trajo_cedula,
        name="verificar_cedula_trajo_existe"
    ),
    
]