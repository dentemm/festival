# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 18:41
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailimages.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_auto_20160602_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customrendition',
            name='file',
            field=models.ImageField(height_field='height', upload_to=wagtail.wagtailimages.models.get_rendition_upload_to, width_field='width'),
        ),
    ]