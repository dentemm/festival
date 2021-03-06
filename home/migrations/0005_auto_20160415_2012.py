# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-15 18:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_person_page'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentsnippet',
            name='commentwithtitle_ptr',
        ),
        migrations.AlterField(
            model_name='festivalpage',
            name='main_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.CustomImage'),
        ),
        migrations.AlterField(
            model_name='person',
            name='page',
            field=modelcluster.fields.ParentalKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_person', to='home.FestivalPage'),
        ),
        migrations.DeleteModel(
            name='CommentSnippet',
        ),
    ]
