from django.conf.urls import patterns, include, url
from django.contrib import admin
from Quiniela.views import *

admin.autodiscover()


urlpatterns = patterns('',
                       url(r'^$', ListadoGrupos.as_view(), name="listado_grupos"),
                       url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
                       url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),
                       url(r'^registro/$', Registro.as_view(), name="registro"),
                       url(r'^usuarioRegistrado/$', UsuarioRegistrado.as_view(), name="usuario_registrado"),

                       url(r'^usuarios/$', ListadoUsuarios.as_view(), name="listado_usuarios"),
                       url(r'^usuarios/(?P<pk>\d+)$', DetalleUsuario.as_view(), name="detalle_usuario"),

                       url(r'^partidos/$', ListadoPartidos.as_view(), name="listado_partidos"),
                       url(r'^partidos/(?P<pk>\d+)$', DetallePartido.as_view(), name="detalle_partido"),

                       url(r'^equipos/(?P<pk>\d+)$', DetalleEquipo.as_view(), name="detalle_equipo"),

                       url(r'^actualizar_pronostico/(?P<pk>\d+)$', ActualizarPronostico.as_view(),
                           name="actualizar_pronostico"),

                       url(r'^cargarPronostico/(?P<pk>\d+)$', cargar_pronostico, name="cargar_pronostico"),
                       url(r'^pronosticoCargado/$', pronostico_cargado, name="pronostico_cargado"),

                       url(r'^admin/', include(admin.site.urls)),
                       )
