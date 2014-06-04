from django.contrib import admin
from Quiniela.models import *


class EquiposInline(admin.StackedInline):
    model = Equipo
    fields = ["nombre", "url_bandera"]


class AdminPartido(admin.ModelAdmin):
    fields = ["equipo_a", "equipo_b", "fecha"]


class AdminEquipo(admin.ModelAdmin):
    list_display = ['nombre', 'grupo']
    fields = ["nombre", "grupo", "url_bandera"]
    list_filter = ["grupo"]


class AdminGrupo(admin.ModelAdmin):
    list_display = ["nombre", "equipos"]
    inlines = [EquiposInline]


class AdminUsuario(admin.ModelAdmin):
    fields = ["nombre", "apellido", "correo", "pago_realizado"]


class AdminPronostico(admin.ModelAdmin):
    fields = ["usuario", "partido", "goles_equipo_a", "goles_equipo_b"]
    list_filter = ["usuario", "partido"]


admin.site.register(Grupo, AdminGrupo)
admin.site.register(Equipo, AdminEquipo)
admin.site.register(Partido, AdminPartido)
# admin.site.register(Usuario, AdminUsuario)
admin.site.register(Pronostico, AdminPronostico)
admin.site.register(Perfil)
