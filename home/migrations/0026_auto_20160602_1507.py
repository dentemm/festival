# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-02 13:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_auto_20160601_2110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='festivalpage',
            name='general_rating',
        ),
        migrations.RemoveField(
            model_name='festivalpage',
            name='num_votes',
        ),
    ]