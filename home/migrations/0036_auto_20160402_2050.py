# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-02 18:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0035_auto_20160401_1100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='festivalpagerateableattribute',
            options={'ordering': ['name'], 'verbose_name': 'Beoordeelbaar kenmerk', 'verbose_name_plural': 'Beoordeelbare kenmerken'},
        ),
        migrations.RemoveField(
            model_name='festivalpage',
            name='description',
        ),
        migrations.AlterField(
            model_name='festivalpage',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='festivals', to='home.Location'),
        ),
        migrations.AlterUniqueTogether(
            name='festivalpageratebleattributevalue',
            unique_together=set([('page', 'rateable_attribute')]),
        ),
    ]
