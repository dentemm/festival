# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-22 16:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_auto_20160506_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='festivalpage',
            name='end_date',
            field=models.DateField(null=True, verbose_name='Eind datum'),
        ),
    ]
