# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClimbingArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('country', models.TextField()),
                ('province', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Crag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('climbing_area', models.ForeignKey(blank=True, to='ClimbQueryService.ClimbingArea', null=True)),
                ('parent_crag', models.ForeignKey(blank=True, to='ClimbQueryService.Crag', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('pitch', models.IntegerField()),
                ('crag_location', models.FloatField()),
                ('grade', models.IntegerField()),
                ('stars', models.IntegerField()),
                ('draws', models.IntegerField()),
                ('climbing_style', models.TextField()),
                ('description', models.TextField()),
                ('crag', models.ForeignKey(to='ClimbQueryService.Crag')),
            ],
        ),
    ]
