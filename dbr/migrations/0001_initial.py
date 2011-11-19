# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Report'
        db.create_table('dbr_report', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=180)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, unique=True, max_length=50, blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('dbr', ['Report'])

        # Adding model 'Column'
        db.create_table('dbr_column', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbr.Report'])),
            ('field', self.gf('dbr.models.DbrModelAttrField')(max_length=250)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('width', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('dbr', ['Column'])

        # Adding model 'CustomColumn'
        db.create_table('dbr_customcolumn', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbr.Report'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('width', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('aggregation', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal('dbr', ['CustomColumn'])

        # Adding model 'Annotate'
        db.create_table('dbr_annotate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbr.Report'])),
            ('field', self.gf('dbr.models.DbrModelAttrField')(max_length=250)),
            ('function', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('dbr', ['Annotate'])

        # Adding model 'Aggregate'
        db.create_table('dbr_aggregate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbr.Report'])),
            ('field', self.gf('dbr.models.DbrModelAttrField')(max_length=250)),
            ('function', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('dbr', ['Aggregate'])

        # Adding model 'Filter'
        db.create_table('dbr_filter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbr.Report'])),
            ('column', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('operator', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('operator_short', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('dbr', ['Filter'])

        # Adding model 'GroupBy'
        db.create_table('dbr_groupby', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(related_name='groupby', to=orm['dbr.Report'])),
            ('field', self.gf('dbr.models.DbrModelAttrField')(max_length=250)),
        ))
        db.send_create_signal('dbr', ['GroupBy'])

        # Adding model 'Chart'
        db.create_table('dbr_chart', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbr.Report'])),
            ('chart_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('field', self.gf('dbr.models.DbrModelAttrField')(max_length=250)),
            ('color', self.gf('django.db.models.fields.CharField')(default='#000000', max_length=20)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=160, blank=True)),
            ('element_tag', self.gf('dbr.models.DbrModelAttrField')(max_length=250, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('dbr', ['Chart'])


    def backwards(self, orm):
        
        # Deleting model 'Report'
        db.delete_table('dbr_report')

        # Deleting model 'Column'
        db.delete_table('dbr_column')

        # Deleting model 'CustomColumn'
        db.delete_table('dbr_customcolumn')

        # Deleting model 'Annotate'
        db.delete_table('dbr_annotate')

        # Deleting model 'Aggregate'
        db.delete_table('dbr_aggregate')

        # Deleting model 'Filter'
        db.delete_table('dbr_filter')

        # Deleting model 'GroupBy'
        db.delete_table('dbr_groupby')

        # Deleting model 'Chart'
        db.delete_table('dbr_chart')


    models = {
        'dbr.aggregate': {
            'Meta': {'object_name': 'Aggregate'},
            'field': ('dbr.models.DbrModelAttrField', [], {'max_length': '250'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbr.Report']"})
        },
        'dbr.annotate': {
            'Meta': {'object_name': 'Annotate'},
            'field': ('dbr.models.DbrModelAttrField', [], {'max_length': '250'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbr.Report']"})
        },
        'dbr.chart': {
            'Meta': {'object_name': 'Chart'},
            'chart_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'#000000'", 'max_length': '20'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'element_tag': ('dbr.models.DbrModelAttrField', [], {'max_length': '250', 'blank': 'True'}),
            'field': ('dbr.models.DbrModelAttrField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbr.Report']"})
        },
        'dbr.column': {
            'Meta': {'object_name': 'Column'},
            'field': ('dbr.models.DbrModelAttrField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbr.Report']"}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'dbr.customcolumn': {
            'Meta': {'object_name': 'CustomColumn'},
            'aggregation': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbr.Report']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'dbr.filter': {
            'Meta': {'object_name': 'Filter'},
            'column': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'operator_short': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbr.Report']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'dbr.groupby': {
            'Meta': {'object_name': 'GroupBy'},
            'field': ('dbr.models.DbrModelAttrField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'groupby'", 'to': "orm['dbr.Report']"})
        },
        'dbr.report': {
            'Meta': {'object_name': 'Report'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '180'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['dbr']
