import random
import user
from django.core.urlresolvers import reverse_lazy
from django.forms import Field
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from django.views.generic import FormView, UpdateView, TemplateView, DetailView, ListView

from Quiniela.forms import PronosticoForm, UsuarioForm
from Quiniela.models import *


class CargarPronostico(FormView):
    partidos = Partido.objects.all()
    data_inicial = []
    pronostico_form_set = formset_factory(PronosticoForm, extra=0)
    mensaje = "seleccione un usuario"
    form_class = pronostico_form_set

    def get(self, request, data_inicial=data_inicial, form_set=pronostico_form_set, *args, **kwargs):
        pronostico_set = form_set()
        usuario_seleccionado = user
        for partido in Partido.objects.all():
            pron_usu_partido, creado = Pronostico.objects.get_or_create(partido=partido,
                                                                        usuario=usuario_seleccionado,
                                                                        defaults={"goles_equipo_a": 0,
                                                                                  "goles_equipo_b": 0
                                                                        })
            data_inicial.append({"pk": pron_usu_partido.pk,
                                 "partido": pron_usu_partido.partido,
                                 "usuario": pron_usu_partido.usuario,
                                 "goles_equipo_a": pron_usu_partido.goles_equipo_a,
                                 "goles_equipo_b": pron_usu_partido.goles_equipo_b})
            pronostico_set = form_set(initial=data_inicial)
        return render_to_response("Quiniela/cargar_pronostico.html", {"pronostico": pronostico_set})

    def post(self, request, pronostico_form_set=pronostico_form_set, *args, **kwargs):
        pronostico_set = pronostico_form_set(request.POST)
        for pronostico in pronostico_set:
            pronostico_db, creado = Pronostico.objects.get_or_create(partido=pronostico.partido,
                                                                     usuario=pronostico.usuario,
                                                                     defaults={
                                                                         "goles_equipo_a": pronostico.goles_equipo_a,
                                                                         "goles_equipo_b": pronostico.goles_equipo_b
                                                                     })
            if creado:
                pronostico_db.save()
            else:
                pronostico.pk = pronostico.pk
                pronostico.save()
        pass


class ListadoGrupos(ListView):
    model = Grupo

    def get_queryset(self):
        return Grupo.objects.all().order_by("nombre").distinct()


class ListadoEquipos(ListView):
    model = Equipo

    def get_queryset(self):
        return Equipo.objects.all().extra(select={"goles_diferencia": "goles_a_favor - goles_en_contra"},
                                          order_by=["grupo", "-puntos", "-goles_diferencia", "goles_a_favor"])


class ListadoUsuarios(ListView):
    model = User

    def get_queryset(self):
        return User.objects.all().order_by("-perfil__puntos")


class ListadoPartidos(ListView):
    model = Partido

    def get_queryset(self):
        return Partido.objects.all().order_by("fecha")


class DetalleUsuario(DetailView):
    model = User
    context_object_name = "usuario"


class DetallePartido(DetailView):
    model = Partido

    def get_context_data(self, **kwargs):
        context = super(DetallePartido, self).get_context_data(**kwargs)
        partido = kwargs.get('object')
        usuario = context['view'].request.user
        context['pronostico'], creado = Pronostico.objects.get_or_create(partido=partido, usuario_id=usuario.id,
                                                                         defaults={
                                                                             "goles_equipo_a": 0,
                                                                             "goles_equipo_b": 0
                                                                         })
        return context


class DetalleEquipo(DetailView):
    model = Equipo

    def get_context_data(self, **kwargs):
        context = super(DetalleEquipo, self).get_context_data(**kwargs)
        context['partidos'] = Partido.objects.filter(
            Q(equipo_a=kwargs.get("object")) | Q(equipo_b=kwargs.get("object")))
        return context


class Registro(FormView):
    template_name = "registration/registro.html"
    form_class = UsuarioForm
    success_url = reverse_lazy("usuario_registrado")

    def form_valid(self, form):
        print form.errors
        usuario = form.save()
        usuario.first_name = form.data["first_name"]
        usuario.last_name = form.data["last_name"]
        usuario.email = form.data["email"]
        usuario.save()

        perfil = Perfil(usuario=usuario)
        perfil.save()
        return super(Registro, self).form_valid(form)


class PronosticoCargado(TemplateView):
    template_name = "Quiniela/pronostico_cargado.html"


class UsuarioRegistrado(TemplateView):
    template_name = "registration/registro_completado.html"


class ActualizarPronostico(UpdateView):
    model = Pronostico
    form_class = PronosticoForm
    success_url = "/pronosticoCargado"

    def get_context_data(self, **kwargs):
        context = super(ActualizarPronostico, self).get_context_data(**kwargs)
        context["partido"] = self.object.partido
        return context


class SimularQuiniela(TemplateView):
    template_name = "Quiniela/simulacion_finalizada.html"

    def get(self, request, *args, **kwargs):
        for equipo in Equipo.objects.all():
            equipo.partidos_jugados = 0
            equipo.partidos_ganados = 0
            equipo.partidos_empatados = 0
            equipo.partidos_perdidos = 0
            equipo.puntos = 0
            equipo.save()
        for partido in Partido.objects.all():
            partido.equipo_ganador = None
            # partido.partido_jugado = False
            # partido.goles_equipo_a = 0
            # partido.goles_equipo_b = 0

            # for partido in Partido.objects.all():
            # partido.partido_jugado = True
            #     partido.goles_equipo_a = random.randint(0, 4)
            #     partido.goles_equipo_b = random.randint(0, 4)
            partido.save()
            calcular_puntaje_pronosticos(partido)
        calcular_puntos_usuario()
        return render_to_response(self.template_name)