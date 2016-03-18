# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-18 16:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20160318_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='festivalpage',
            name='attribute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.FestivalPageRatebleAttributeValue'),
        ),
        migrations.AlterField(
            model_name='festivalpageratebleattributevalue',
            name='attribute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='home.FestivalPageRateableAttribute'),
        ),
    ]
