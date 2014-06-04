# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Equipo'
        db.create_table(u'Quiniela_equipo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('grupo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Quiniela.Grupo'])),
            ('partidos_jugados', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('partidos_ganados', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('partidos_perdidos', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('partidos_empatados', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('goles_a_favor', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('goles_en_contra', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('puntos', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('url_bandera', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'Quiniela', ['Equipo'])

        # Adding model 'Grupo'
        db.create_table(u'Quiniela_grupo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'Quiniela', ['Grupo'])

        # Adding model 'Partido'
        db.create_table(u'Quiniela_partido', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('equipo_a', self.gf('django.db.models.fields.related.ForeignKey')(related_name='equipo_a', to=orm['Quiniela.Equipo'])),
            ('equipo_b', self.gf('django.db.models.fields.related.ForeignKey')(related_name='equipo_b', to=orm['Quiniela.Equipo'])),
            ('goles_equipo_a', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('goles_equipo_b', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('equipo_ganador', self.gf('django.db.models.fields.related.ForeignKey')(related_name='equipo_ganador', to=orm['Quiniela.Equipo'])),
            ('fecha', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'Quiniela', ['Partido'])


    def backwards(self, orm):
        # Deleting model 'Equipo'
        db.delete_table(u'Quiniela_equipo')

        # Deleting model 'Grupo'
        db.delete_table(u'Quiniela_grupo')

        # Deleting model 'Partido'
        db.delete_table(u'Quiniela_partido')


    models = {
        u'Quiniela.equipo': {
            'Meta': {'object_name': 'Equipo'},
            'goles_a_favor': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'goles_en_contra': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'grupo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Quiniela.Grupo']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'partidos_empatados': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'partidos_ganados': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'partidos_jugados': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'partidos_perdidos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'puntos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url_bandera': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'Quiniela.grupo': {
            'Meta': {'object_name': 'Grupo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'Quiniela.partido': {
            'Meta': {'object_name': 'Partido'},
            'equipo_a': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'equipo_a'", 'to': u"orm['Quiniela.Equipo']"}),
            'equipo_b': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'equipo_b'", 'to': u"orm['Quiniela.Equipo']"}),
            'equipo_ganador': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'equipo_ganador'", 'to': u"orm['Quiniela.Equipo']"}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'goles_equipo_a': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'goles_equipo_b': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['Quiniela']