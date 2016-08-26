from django.conf.urls import include, url
from django.contrib import admin
from apps.registro import views
from django.conf import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'Shsa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(
        r'^$',
        views.DetectarUsuario.as_view(),
        name='registro_detectar_usuario'
    ),
    url(r'^admin/', include(admin.site.urls)),

    url(
        r'^registro/',
        include('apps.registro.urls')
    ),
    url(
    	r'^rcs/',
    	include('apps.rcs.urls')
    ),
]
