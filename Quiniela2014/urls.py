from django.conf.urls import patterns, include, url
from django.contrib import admin

from Quiniela.views import Registro, UsuarioRegistrado


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
                       url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),
                       url(r'^registro/$', Registro.as_view(), name="registro"),
                       url(r'^usuarioRegistrado/$', UsuarioRegistrado.as_view(), name="usuario_registrado"),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^quiniela/', include("Quiniela.urls")),
)
