# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-05 17:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0012_copy_image_permissions_to_collections'),
        ('home', '0051_auto_20160405_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='festivalpage',
            name='main_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
        migrations.AlterField(
            model_name='festivalimage',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.Image', verbose_name='afbeelding'),
        ),
        migrations.AlterField(
            model_name='festivalpage',
            name='website',
            field=models.URLField(blank=True, max_length=120, null=True),
        ),
    ]