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
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CronLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('line', models.IntegerField()),
                ('body', models.CharField(max_length=1024, null=True)),
                ('command', models.CharField(max_length=1024, null=True)),
                ('month', models.CharField(max_length=1024, null=True)),
                ('day', models.CharField(max_length=1024, null=True)),
                ('week', models.CharField(max_length=1024, null=True)),
                ('hour', models.CharField(max_length=1024, null=True)),
                ('minute', models.CharField(max_length=1024, null=True)),
                ('cron', models.ForeignKey(to='cron_table.Cron')),
            ],
            options={
                'db_table': 'cron_table_cron_line',
            },
        ),
    ]
