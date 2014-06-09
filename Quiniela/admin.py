from django.contrib import admin
from Quiniela.models import *


class EquiposInline(admin.StackedInline):
    model = Equipo
    fields = ["nombre", "url_bandera"]


class AdminPartido(admin.ModelAdmin):
    # fields = ["equipo_a", "equipo_b", "fecha", "goles_equipo_a", "goles_equipo_b", "tipo_partido", "partido_jugado"]
    fieldsets = (
        ("Partido", {
            "fields": ("fecha", "equipo_a", "equipo_b", "tipo_partido")
        }),
        ("Resultado", {
            "fields": ("goles_equipo_a", "goles_equipo_b", "partido_jugado")
        })
    )
    list_display = ["id", "titulo", "goles_equipo_a", "goles_equipo_b", "fecha", "partido_jugado"]
    list_editable = ["goles_equipo_a", "goles_equipo_b", "partido_jugado"]
    list_display_links = ["titulo"]
    list_filter = ["equipo_a__grupo", "tipo_partido"]


class AdminEquipo(admin.ModelAdmin):
    list_display = ['nombre', 'grupo', "puntos"]
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
