# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-13 08:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('festivaluser', '0005_auto_20160713_1052'),
    ]

    operations = [
        migrations.RenameField(
            model_name='festivaladvisoruser',
            old_name='sex',
            new_name='gender',
        ),
    ]
