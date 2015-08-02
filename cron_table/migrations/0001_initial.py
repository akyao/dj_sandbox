# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cron',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.CharField(max_length=16384)),
                ('hash', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='CronLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.CharField(max_length=1024)),
                ('command', models.CharField(max_length=1024)),
                ('month', models.CharField(max_length=1024)),
                ('day', models.CharField(max_length=1024)),
                ('week', models.CharField(max_length=1024)),
                ('hour', models.CharField(max_length=1024)),
                ('minute', models.CharField(max_length=1024)),
            ],
        ),
    ]
