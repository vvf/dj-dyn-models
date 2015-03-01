# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dynmodels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cars',
            name='model',
            field=models.CharField(max_length=b'255', null=b'True', verbose_name=b'Model', blank=b'True'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rooms',
            name='floor',
            field=models.IntegerField(null=b'True', verbose_name='\u042d\u0442\u0430\u0436', blank=b'True'),
            preserve_default=True,
        ),
    ]
