# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-20 09:47
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20160319_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='festivalpage',
            name='descr',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True, default=''),
        ),
    ]
