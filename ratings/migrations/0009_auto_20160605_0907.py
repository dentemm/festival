# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-05 07:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0008_auto_20160602_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='average',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='bad',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='excellent',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='score',
            name='good',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]