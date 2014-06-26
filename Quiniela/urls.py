__author__ = 'anyul'
from django.conf.urls import patterns, url

from Quiniela.views import *

urlpatterns = patterns('',
                       url(r'^usuarios/$', ListadoUsuarios.as_view(), name="listado_usuarios"),
                       url(r'^usuarios/(?P<pk>\d+)$', DetalleUsuario.as_view(), name="detalle_usuario"),

                       url(r'^grupos/$', ListadoGrupos.as_view(), name="listado_grupos"),
                       url(r'^grupos/(?P<pk>\d+)$', DetalleGrupo.as_view(), name="detalle_grupo"),

                       url(r'^partidos/$', ListadoPartidos.as_view(), name="listado_partidos"),
                       url(r'^partidos/(?P<pk>\d+)/$', DetallePartido.as_view(), name="detalle_partido"),
                       url(r'^partidos/(?P<pk>\d+)/editar/$', EditarPartido.as_view(), name="editar_partido"),

                       url(r'^$', ListadoEquipos.as_view(), name="listado_equipos"),
                       url(r'^equipos/(?P<pk>\d+)$', DetalleEquipo.as_view(), name="detalle_equipo"),

                       url(r'^pronosticos/actualizar_pronostico/(?P<pk>\d+)$', ActualizarPronostico.as_view(),
                           name="actualizar_pronostico"),
                       url(r'^pronosticos/pronostico_usuario$', CargarPronosticoInlne.as_view(),
                           name="cargar_pronostico_usuario"),
                       url(r'^pronosticos/cargar_pronostico/$', CargarPronostico.as_view(), name="cargar_pronostico"),
                       url(r'^pronosticos/pronostico_cargado/$', PronosticoCargado.as_view(),
                           name="pronostico_cargado"),

                       url('^en_vivo/$', ResultadosEnVivo.as_view(), name="en_vivo"),
                       url(r'^simular_quiniela/', SimularQuiniela.as_view(), name="simular_quiniela")
)
