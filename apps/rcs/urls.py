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
    
]