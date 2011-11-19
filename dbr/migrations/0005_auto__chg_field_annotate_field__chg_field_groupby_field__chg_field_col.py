# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Annotate.field'
        db.alter_column('dbr_annotate', 'field', self.gf('dbr.fields.DbrSimpleModelFieldField')(max_length=250))

        # Changing field 'GroupBy.field'
        db.alter_column('dbr_groupby', 'field', self.gf('dbr.fields.DbrSimpleModelFieldField')(max_length=250))

        # Changing field 'Column.field'
        db.alter_column('dbr_column', 'field', self.gf('dbr.fields.DbrSimpleModelFieldField')(max_length=250))

        # Changing field 'Aggregate.field'
        db.alter_column('dbr_aggregate', 'field', self.gf('dbr.fields.DbrSimpleModelFieldField')(max_length=250))

        # Changing field 'Chart.element_tag'
        db.alter_column('dbr_chart', 'element_tag', self.gf('dbr.fields.DbrSimpleModelFieldField')(max_length=250))

        # Changing field 'Chart.field'
        db.alter_column('dbr_chart', 'field', self.gf('dbr.fields.DbrSimpleModelFieldField')(max_length=250))

        # Changing field 'Filter.column'
        db.alter_column('dbr_filter', 'column', self.gf('dbr.fields.DbrSimpleModelFieldField')(max_length=250))


    def backwards(self, orm):
        
        # Changing field 'Annotate.field'
        db.alter_column('dbr_annotate', 'field', self.gf('dbr.fields.DbrModelAttrField')(max_length=250))

        # Changing field 'GroupBy.field'
        db.alter_column('dbr_groupby', 'field', self.gf('dbr.fields.DbrModelAttrField')(max_length=250))

        # Changing field 'Column.field'
        db.alter_column('dbr_column', 'field', self.gf('dbr.fields.DbrModelAttrField')(max_length=250))

        # Changing field 'Aggregate.field'
        db.alter_column('dbr_aggregate', 'field', self.gf('dbr.fields.DbrModelAttrField')(max_length=250))

        # Changing field 'Chart.element_tag'
        db.alter_column('dbr_chart', 'element_tag', self.gf('dbr.fields.DbrModelAttrField')(max_length=250))

        # Changing field 'Chart.field'
        db.alter_column('dbr_chart', 'field', self.gf('dbr.fields.DbrModelAttrField')(max_length=250))

        # Changing field 'Filter.column'
        db.alter_column('dbr_filter', 'column', self.gf('dbr.fields.DbrModelAttrField')(max_length=250))


    models = {
        'dbr.aggregate': {
            'Meta': {'object_name': 'Aggregate'},
            'field': ('dbr.fields.DbrSimpleModelFieldField', [], {'max_length': '250'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbr.Report']"})
        },
        'dbr.annotate': {
            'Meta': {'object_name': 'Annotate'},
            'field': ('dbr.fields.DbrSimpleModelFieldField', [], {'max_length': '250'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbr.Report']"})
        },
        'dbr.chart': {
            'Meta': {'object_name': 'Chart'},
            'chart_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'#000000'", 'max_length': '20'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'element_tag': ('dbr.fields.DbrSimpleModelFieldField', [], {'max_length': '250', 'blank': 'True'}),
            'field': ('dbr.fields.DbrSimpleModelFieldField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbr.Report']"})
        },
        'dbr.column': {
            'Meta': {'object_name': 'Column'},
            'field': ('dbr.fields.DbrSimpleModelFieldField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbr.Report']"}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'dbr.customcolumn': {
            'Meta': {'object_name': 'CustomColumn'},
            'aggregation': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbr.Report']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'dbr.filter': {
            'Meta': {'object_name': 'Filter'},
            'column': ('dbr.fields.DbrSimpleModelFieldField', [], {'max_length': '250'}),
            'exclude': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'operator_short': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbr.Report']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'dbr.groupby': {
            'Meta': {'object_name': 'GroupBy'},
            'field': ('dbr.fields.DbrSimpleModelFieldField', [], {'max_length': '250'}),
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
