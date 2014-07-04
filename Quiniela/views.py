import json
import requests

from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.db.models import Sum
from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import FormView, UpdateView, TemplateView, DetailView, ListView, CreateView

from Quiniela.forms import *


class ResultadosEnVivo(TemplateView):
    template_name = "Quiniela/en_vivo.html"

    def get_context_data(self, **kwargs):
        global r
        context = super(ResultadosEnVivo, self).get_context_data(**kwargs)
        url = "http://worldcup.sfg.io/matches/today"
        headers = {'content-type': 'application/json'}
        try:
            r = requests.get(url, headers=headers)
        except Exception, ex:
            messages.add_message(self.request, messages.ERROR, 'Ha ocurrido un error al procesar los resultados.' + ex)
        if r.status_code == 200:
            partidos = []
            json_content = json.loads(r.content)
            for partido in json_content:
                try:
                    if partido['match_number'] in range(49, 57):
                        tipo_partido = tipo_partido_opciones[1]
                    elif partido['match_number'] in range(57, 61):
                        tipo_partido = tipo_partido_opciones[2]
                    elif partido["match_number"] in range(61, 63):
                        tipo_partido = tipo_partido_opciones[3]
                    elif partido["match_number"] == 63:
                        tipo_partido = tipo_partido_opciones[5]
                    elif partido["match_number"] == 64:
                        tipo_partido = tipo_partido_opciones[4]
                    else:
                        tipo_partido = tipo_partido_opciones[0]

                    partido_db, creado = Partido.objects.get_or_create(equipo_a__codigo=partido['home_team']['code'],
                                                                       equipo_b__codigo=partido['away_team']['code'],
                                                                       defaults={
                                                                           "equipo_a": Equipo.objects.get(
                                                                               codigo=partido['home_team']['code']),
                                                                           "equipo_b": Equipo.objects.get(
                                                                               codigo=partido['away_team']['code']),
                                                                           "tipo_partido": tipo_partido
                                                                       })
                    partido_db.goles_equipo_a = partido["home_team"]["goals"]
                    partido_db.goles_equipo_b = partido["away_team"]["goals"]
                    if partido["status"] == "completed" and not partido_db.partido_jugado:
                        partido_db.partido_jugado = True
                        partido_db.save()

                    partidos.append(partido_db)
                except Exception, e:
                    messages.add_message(self.request, messages.ERROR,
                                         "Error al cargar partido: " + partido_db + e.message)

            context["partidos"] = partidos
            context['json'] = json_content
        else:
            context["partidos"] = "no hay datos disponibles" + r.status_code
        return context


class CargarPronosticoInlne(CreateView):
    def get(self, request, *args, **kwargs):
        usuario_pronostico_set = inlineformset_factory(Usuario, Pronostico)
        usuario = request.user
        formset = usuario_pronostico_set(instance=usuario)
        self.form_class = formset
        return super(CargarPronosticoInlne, self).get(request, *args, **kwargs)


class CargarPronostico(FormView):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        data_inicial = []
        pronostico_form_set = formset_factory(PronosticoForm, extra=0)
        # formularios = pronostico_form_set()
        for partido in Partido.objects.all():
            pron_usu_partido, creado = Pronostico.objects.get_or_create(partido=partido,
                                                                        usuario=request.user,
                                                                        defaults={"goles_equipo_a": 0,
                                                                                  "goles_equipo_b": 0
                                                                        })
            data_inicial.append({"pk": pron_usu_partido.pk,
                                 "partido": pron_usu_partido.partido,
                                 "usuario": pron_usu_partido.usuario,
                                 "goles_equipo_a": pron_usu_partido.goles_equipo_a,
                                 "goles_equipo_b": pron_usu_partido.goles_equipo_b})
            formularios = pronostico_form_set(initial=data_inicial)
        return render_to_response("Quiniela/cargar_pronostico.html",
                                  {"request": request,
                                   "formularios": formularios,
                                   "datos": formularios.initial},
                                  context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        pronostico_form_set = formset_factory(PronosticoForm)
        pronostico_set = pronostico_form_set(request.POST)
        for i in range(0, 47, 1):
            partido_form = pronostico_set.data["form-" + str(i) + "-partido"]
            usuario_form = request.user
            goles_equipo_a_form = pronostico_set.data["form-" + str(i) + "-goles_equipo_a"]
            goles_equipo_b_form = pronostico_set.data["form-" + str(i) + "-goles_equipo_b"]
            pronostico, creado = Pronostico.objects.get_or_create(
                partido=partido_form,
                usuario=usuario_form,
                defaults={
                    "goles_equipo_a": goles_equipo_a_form,
                    "goles_equipo_b": goles_equipo_b_form
                }
            )
            if not creado:
                pronostico.goles_equipo_a = goles_equipo_a_form
                pronostico.goles_equipo_b = goles_equipo_b_form
            pronostico.save()

        return HttpResponseRedirect(reverse_lazy("simular_quiniela"))


class ListadoGrupos(ListView):
    model = Grupo

    def get_context_data(self, **kwargs):
        context = super(ListadoGrupos, self).get_context_data(**kwargs)
        context["partidos_octavos_de_final"] = Partido.objects.filter(tipo_partido="O")
        context["partidos_cuartos_de_final"] = Partido.objects.filter(tipo_partido="CU")
        context["partidos_semifinal"] = Partido.objects.filter(tipo_partido="SF")
        context["partido_final"] = Partido.objects.filter(tipo_partido="F")
        context["partido_tercer_lugar"] = Partido.objects.filter(tipo_partido="TL")
        return context

    def get_queryset(self):
        return Grupo.objects.all().order_by("nombre").distinct()


class ListadoEquipos(ListView):
    model = Equipo

    def get_queryset(self):
        return Equipo.objects.all().extra(select={"goles_diferencia": "goles_a_favor - goles_en_contra"},
                                          order_by=["grupo", "-puntos", "-goles_diferencia", "goles_a_favor"])


class ListadoUsuarios(ListView):
    model = User

    def get_context_data(self, **kwargs):
        contexto = super(ListadoUsuarios, self).get_context_data(**kwargs)
        truncate_date = connection.ops.date_trunc_sql('day', 'Quiniela_partido.fecha')
        contexto['progreso'] = Pronostico.objects.all().extra({'fecha_str': truncate_date}). \
            values('usuario__username', "fecha_str").annotate(Sum('puntos'))
        return contexto

    def get_queryset(self):
        return User.objects.all().order_by("-perfil__puntos")


class ListadoPartidos(ListView):
    model = Partido

    def get_queryset(self):
        return Partido.objects.all().order_by("fecha")


class DetalleGrupo(DetailView):
    model = Grupo
    context_object_name = "grupo"

    def get_context_data(self, **kwargs):
        context = super(DetalleGrupo, self).get_context_data(**kwargs)
        context['partidos'] = Partido.objects.filter(equipo_a__grupo=self.object, tipo_partido="C")
        return context


class DetalleUsuario(DetailView):
    model = User
    context_object_name = "usuario"

    def get_context_data(self, **kwargs):
        truncate_date = connection.ops.date_trunc_sql('day', 'Quiniela_partido.fecha')
        context = super(DetalleUsuario, self).get_context_data(**kwargs)
        context['progreso'] = self.object.pronostico_set.extra({'fecha_str': truncate_date}) \
            .values("fecha_str").annotate(Sum("puntos"))
        return context


class DetallePartido(DetailView):
    model = Partido

    def get_context_data(self, **kwargs):
        context = super(DetallePartido, self).get_context_data(**kwargs)
        partido = kwargs.get('object')
        if self.request.user.is_authenticated():
            usuario = self.request.user
            context['pronostico'], creado = Pronostico.objects.get_or_create(partido=partido,
                                                                             usuario_id=usuario.id,
                                                                             defaults={
                                                                                 "goles_equipo_a": 0,
                                                                                 "goles_equipo_b": 0
                                                                             })
        return context


class EditarPartido(UpdateView):
    model = Partido
    form_class = PartidoForm

    def get_success_url(self):
        return reverse_lazy("detalle_partido", args=[self.object.pk])


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
            equipo.goles_a_favor = 0
            equipo.goles_en_contra = 0
            equipo.save()
        for partido in Partido.objects.all():
            partido.equipo_ganador = None
            # partido.partido_jugado = False
            # partido.goles_equipo_a = 0
            # partido.goles_equipo_b = 0

            # for partido in Partido.objects.all():
            # partido.partido_jugado = True
            # partido.goles_equipo_a = random.randint(0, 4)
            # partido.goles_equipo_b = random.randint(0, 4)
            partido.save()
            calcular_puntaje_pronosticos(partido)
        calcular_puntos_usuario()
        return render_to_response(self.template_name)