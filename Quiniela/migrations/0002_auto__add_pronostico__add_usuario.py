# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Pronostico'
        db.create_table(u'Quiniela_pronostico', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('partido', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Quiniela.Partido'])),
            ('goles_equipo_a', self.gf('django.db.models.fields.IntegerField')()),
            ('goles_equipo_b', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'Quiniela', ['Pronostico'])

        # Adding model 'Usuario'
        db.create_table(u'Quiniela_usuario', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('apellido', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('pago_realizado', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('correo', self.gf('django.db.models.fields.EmailField')(default='usuario@tcs.com.ve', max_length=75)),
            ('puntos', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'Quiniela', ['Usuario'])


    def backwards(self, orm):
        # Deleting model 'Pronostico'
        db.delete_table(u'Quiniela_pronostico')

        # Deleting model 'Usuario'
        db.delete_table(u'Quiniela_usuario')


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
            'equipo_a': ('django.db.models.fields.related.ForeignKey', [],
                         {'related_name': "'equipo_a'", 'to': u"orm['Quiniela.Equipo']"}),
            'equipo_b': ('django.db.models.fields.related.ForeignKey', [],
                         {'related_name': "'equipo_b'", 'to': u"orm['Quiniela.Equipo']"}),
            'equipo_ganador': ('django.db.models.fields.related.ForeignKey', [],
                               {'related_name': "'equipo_ganador'", 'to': u"orm['Quiniela.Equipo']"}),
            'fecha': ('django.db.models.fields.DateField', [], {}),
            'goles_equipo_a': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'goles_equipo_b': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'Quiniela.pronostico': {
            'Meta': {'object_name': 'Pronostico'},
            'goles_equipo_a': ('django.db.models.fields.IntegerField', [], {}),
            'goles_equipo_b': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partido': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Quiniela.Partido']"})
        },
        u'Quiniela.usuario': {
            'Meta': {'object_name': 'Usuario'},
            'apellido': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'correo': (
            'django.db.models.fields.EmailField', [], {'default': "'usuario@tcs.com.ve'", 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pago_realizado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'puntos': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['Quiniela']