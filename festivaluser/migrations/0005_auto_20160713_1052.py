# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-13 08:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festivaluser', '0004_auto_20160527_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='festivaladvisoruser',
            name='age_max',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='festivaladvisoruser',
            name='age_min',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='festivaladvisoruser',
            name='sex',
            field=models.CharField(blank=True, max_length=27, null=True),
        ),
    ]
