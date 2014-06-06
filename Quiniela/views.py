from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, request
from django.shortcuts import render
from django.views import generic
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.views.generic import FormView, UpdateView, TemplateView
from Quiniela.forms import PronosticoForm, UsuarioForm
from Quiniela.models import *


def cargar_pronostico(request, pk):
    partidos = Partido.objects.all()
    data_inicial = []
    PronosticoFormSet = formset_factory(PronosticoForm, extra=0)
    mensaje = "seleccione un usuario"
    if request.method == 'GET':
        mensaje = ""
        usuario_seleccionado = pk
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
            pronosticoSet = PronosticoFormSet(initial=data_inicial)
    if request.method == 'POST':
        pronosticoSet = PronosticoFormSet(request.POST)
        for pronostico in pronosticoSet:
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
        return HttpResponseRedirect(reverse("pronostico_cargado"))
    else:
        return render(request, "Quiniela/cargar_pronostico.html", locals())
    return render(request, "Quiniela/cargar_pronostico.html", locals())


class ListadoGrupos(generic.ListView):
    model = Grupo

    def get_queryset(self):
        return Grupo.objects.all().order_by("nombre", "equipo__puntos").distinct()


class ListadoUsuarios(generic.ListView):
    model = User

    def get_queryset(self):
        return User.objects.all().order_by("-perfil__puntos")


class ListadoPartidos(generic.ListView):
    model = Partido

    def get_queryset(self):
        return Partido.objects.all().order_by("fecha")


class DetalleUsuario(generic.DetailView):
    model = User
    context_object_name = "usuario"


class DetallePartido(generic.DetailView):
    model = Partido

    def get_context_data(self, **kwargs):
        context = super(DetallePartido, self).get_context_data(**kwargs)
        partido = kwargs.get('object')
        usuario = context['view'].request.user
        context['pronostico'], creado = Pronostico.objects.get_or_create(partido=partido, usuario_id=usuario.id, defaults={
            "goles_equipo_a": 0,
            "goles_equipo_b": 0
        })
        return context


class DetalleEquipo(generic.DetailView):
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
        user = form.save()
        user.first_name = form.data["first_name"]
        user.last_name = form.data["last_name"]
        user.email = form.data["email"]
        user.save()

        perfil = Perfil(usuario=user)
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