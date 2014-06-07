#-*- coding: utf-8 -*-
from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models import F
from django.utils import timezone


def calcular_puntos_equipo(partidos_ganados, partidos_empatados):
    return (partidos_ganados * 3) + partidos_empatados


def calcular_partidos_ganados(equipo):
    """
    cuenta el numero de partidos ganados
    :rtype : Integer
    :param equipo: equipo
    :return: numero de partidos ganados
    """
    return Partido.objects.filter(fecha__lte=timezone.now().date(), equipo_ganador=equipo).count()


def calcular_partidos_empatados(equipo):
    """
    Cuenta el numero de partidos culminados en empate
    :param equipo: equipo
    :return: numero de partidos empatados
    """
    return Partido.objects \
        .filter(Q(equipo_a=equipo) | Q(equipo_b=equipo)) \
        .filter(fecha__lte=timezone.now().date(),
                equipo_ganador__isnull=True,
                goles_equipo_a=F('goles_equipo_b')).count()


def calcular_partidos_perdidos(equipo):
    """
     Realiza el conteo de los partidos perdidos de un equipo
    :param equipo: equipo perdedor
    :return: numero de partidos perdidos
    """
    return Partido.objects.filter((Q(equipo_a=equipo) | Q(equipo_b=equipo)) & ~Q(equipo_ganador=equipo)).count()


def calcular_puntaje_pronosticos(partido):
    """
     Realiza el calculo de los puntos de los pronosticos de un partido jugado
    :param partido: partido jugado
    """
    pronosticos = Pronostico.objects.filter(partido=partido)
    for pronostico in pronosticos:
        if (pronostico.goles_equipo_a == pronostico.partido.goles_equipo_a) & (
                pronostico.goles_equipo_b == pronostico.partido.goles_equipo_b):  # si acierta el resultado
            pronostico.puntos = 5
        elif (pronostico.goles_equipo_a == pronostico.goles_equipo_b) & (
                pronostico.partido.goles_equipo_a == pronostico.partido.goles_equipo_b):  # si acierta empate
            pronostico.puntos = 3
        elif (pronostico.goles_equipo_a > pronostico.goles_equipo_b) & (
                pronostico.partido.goles_equipo_a > pronostico.partido.goles_equipo_b):  # si acierta ganador a
            pronostico.puntos = 3
        elif (pronostico.goles_equipo_b > pronostico.goles_equipo_a) & (
                pronostico.partido.goles_equipo_b > pronostico.partido.goles_equipo_a):  # si acierta ganador a
            pronostico.puntos = 3
        else:
            pronostico.puntos = 0
        pronostico.save()
    calcular_puntos_usuario()


def calcular_puntos_usuario():
    usuarios = User.objects.all()
    for usuario in usuarios:
        pronosticos_usuario = Pronostico.objects.all().filter(usuario=usuario)
        usuario.perfil.puntos = 0
        for pronostico in pronosticos_usuario:
            usuario.perfil.puntos += pronostico.puntos
        usuario.perfil.save()


class Equipo(models.Model):
    nombre = models.CharField(max_length=200)
    grupo = models.ForeignKey("Grupo")
    partidos_jugados = models.IntegerField(default=0)
    partidos_ganados = models.IntegerField(default=0)
    partidos_perdidos = models.IntegerField(default=0)
    partidos_empatados = models.IntegerField(default=0)
    goles_a_favor = models.IntegerField(default=0)
    goles_en_contra = models.IntegerField(default=0)
    puntos = models.IntegerField(default=0)
    url_bandera = models.CharField(max_length=500)

    class Meta:
        ordering = ["grupo__nombre", "puntos", "nombre"]

    def __unicode__(self):
        return self.nombre

    def goles_diferencia(self):
        return self.goles_a_favor - self.goles_en_contra


class Grupo(models.Model):
    nombre = models.CharField(max_length=1)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return 'Grupo %s' % self.nombre

    def equipos(self):
        return self.equipo_set.all().count()

    def equipos_clasificados(self):
        return self.equipo_set.all().order_by("puntos")[0:2]


class Partido(models.Model):
    equipo_a = models.ForeignKey(Equipo, related_name="equipo_a")
    equipo_b = models.ForeignKey(Equipo, related_name="equipo_b")
    goles_equipo_a = models.IntegerField(default=0)
    goles_equipo_b = models.IntegerField(default=0)
    equipo_ganador = models.ForeignKey(Equipo, related_name="equipo_ganador", null=True)
    fecha = models.DateField()

    class Meta:
        ordering = ["fecha"]

    def titulo(self):
        return Partido.__unicode__(self)

    titulo.admin_order_field = "equipo_a"
    titulo.boolean = False
    titulo.short_description = "Partido"

    def __unicode__(self):
        return '%s vs %s' % (unicode(self.equipo_a), unicode(self.equipo_b))

    def es_pasado(self):
        return self.fecha < date.today()

    es_pasado.admin_order_field = 'fecha'
    es_pasado.boolean = True
    es_pasado.short_description = 'Partido Culminado?'

    def save(self, *args, **kwargs):
        super(Partido, self).save(*args, **kwargs)
        if self.goles_equipo_a == self.goles_equipo_b:  # Empate
            self.equipo_a.partidos_empatados = calcular_partidos_empatados(self.equipo_a)
            self.equipo_b.partidos_empatados = calcular_partidos_empatados(self.equipo_b)
            self.equipo_a.puntos = calcular_puntos_equipo(self.equipo_a.partidos_ganados,
                                                          self.equipo_a.partidos_empatados)
            self.equipo_b.puntos = calcular_puntos_equipo(self.equipo_b.partidos_ganados,
                                                          self.equipo_b.partidos_empatados)
        elif self.goles_equipo_a > self.goles_equipo_b:  # Ganador A
            self.equipo_ganador = self.equipo_a
            self.equipo_a.partidos_ganados = calcular_partidos_ganados(self.equipo_a)
            self.equipo_b.partidos_perdidos = calcular_partidos_perdidos(self.equipo_b)
            self.equipo_a.puntos = calcular_puntos_equipo(self.equipo_a.partidos_ganados,
                                                          self.equipo_a.partidos_empatados)
        else:  # Ganador B
            self.equipo_ganador = self.equipo_b
            self.equipo_b.partidos_ganados = calcular_partidos_ganados(self.equipo_b)
            self.equipo_a.partidos_perdidos = calcular_partidos_perdidos(self.equipo_a)
            self.equipo_b.puntos = calcular_puntos_equipo(self.equipo_b.partidos_ganados,
                                                          self.equipo_b.partidos_empatados)
        partido_guardado = super(Partido, self).save(*args, **kwargs)
        calcular_puntaje_pronosticos(self)
        return partido_guardado


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    pago_realizado = models.BooleanField(default=False)
    correo = models.EmailField(default="usuario@tcs.com.ve")
    puntos = models.IntegerField(default=0)

    class Meta:
        ordering = ["nombre"]

    def __unicode__(self):
        return "%s %s" % (self.nombre.capitalize(), self.apellido.capitalize())


class Perfil(models.Model):
    usuario = models.OneToOneField(User)
    puntos = models.IntegerField(default=0)


class Pronostico(models.Model):
    partido = models.ForeignKey(Partido)
    usuario = models.ForeignKey(User)
    goles_equipo_a = models.IntegerField(null=False)
    goles_equipo_b = models.IntegerField(null=False)
    puntos = models.IntegerField(default=0)

    class Meta:
        unique_together = ("partido", "usuario")
        ordering = ["partido"]

    def __unicode__(self):
        return "%s | %s:%s - %s:%s" % (self.usuario,
                                       unicode(self.partido.equipo_a),
                                       self.goles_equipo_a,
                                       unicode(self.partido.equipo_b),
                                       self.goles_equipo_b)