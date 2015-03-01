# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cars',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('brand', models.CharField(max_length=b'255', null=b'True', verbose_name=b'Brand', blank=b'True')),
                ('price', models.IntegerField(null=b'True', verbose_name=b'Price', blank=b'True')),
                ('description', models.CharField(max_length=b'255', null=b'True', verbose_name=b'Description', blank=b'True')),
                ('release_date', models.DateField(null=b'True', verbose_name=b'Release_date', blank=b'True')),
            ],
            options={
                'verbose_name': 'Cars',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='rooms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('department', models.CharField(max_length=b'255', null=b'True', verbose_name='\u041e\u0442\u0434\u0435\u043b', blank=b'True')),
                ('spots', models.IntegerField(null=b'True', verbose_name='\u0412\u043c\u0435\u0441\u0442\u0438\u043c\u043e\u0441\u0442\u044c', blank=b'True')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043c\u043d\u0430\u0442\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=b'255', null=b'True', verbose_name='\u0418\u043c\u044f', blank=b'True')),
                ('paycheck', models.IntegerField(null=b'True', verbose_name='\u0417\u0430\u0440\u043f\u043b\u0430\u0442\u0430', blank=b'True')),
                ('date_joined', models.DateField(null=b'True', verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0441\u0442\u0443\u043f\u043b\u0435\u043d\u0438\u044f \u043d\u0430 \u0440\u0430\u0431\u043e\u0442\u0443', blank=b'True')),
            ],
            options={
                'verbose_name': '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438',
            },
            bases=(models.Model,),
        ),
    ]
