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
        name="registro_logout"
    ),
    
]