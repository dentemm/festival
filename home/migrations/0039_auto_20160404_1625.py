# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-04 14:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0038_auto_20160404_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location', to='home.Address', verbose_name='adres'),
        ),
    ]
