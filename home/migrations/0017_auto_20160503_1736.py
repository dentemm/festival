# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-03 15:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20160503_1643'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='festivalpage',
            options={'ordering': ['date'], 'verbose_name': 'Festival'},
        ),
    ]
