# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-11 19:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('festivaluser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='festivaladvisoruser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='loser', to=settings.AUTH_USER_MODEL),
        ),
    ]