from django.conf.urls import include, url

# print "=============================================="
# import sys
# print sys.path
# print "=============================================="
# export PYTHONPATH='.'
import views
from django.views.generic import TemplateView


urlpatterns = [

    url(
        r'^planilla_seguro_carro',
        views.VerPlanillaSeguroCarro.as_view(),
        name="planilla_seguro_carro"
    ),
    
]