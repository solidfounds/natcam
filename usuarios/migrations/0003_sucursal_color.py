# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-16 03:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_auto_20160213_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='sucursal',
            name='color',
            field=models.CharField(default='#2FCC71', max_length=6),
        ),
    ]
