# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-19 12:35
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_remove_festivalpage_rateable_attribute'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='festivalpagerateableattribute',
            name='attribute',
        ),
        migrations.RemoveField(
            model_name='festivalpagerateableattribute',
            name='rateable_attribute',
        ),
        migrations.AlterField(
            model_name='festivalpageratebleattributevalue',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='rate', to='home.FestivalPage'),
        ),
    ]
